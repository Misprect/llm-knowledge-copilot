import os, json, logging, datetime, sys
from pathlib import Path
from collections import defaultdict, deque
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

# Local imports
from rag_utils import retrieve, PROMPTS
from tot_orchestrator import choose_best_two
from evaluation import evaluate_metrics

# ------------------------------
# 0️⃣ Encoding fix
# ------------------------------
sys.stdout.reconfigure(encoding="utf-8")

# ------------------------------
# 1️⃣ Config setup
# ------------------------------
load_dotenv()
app = FastAPI(title="LLM Knowledge Copilot (Gemini Edition)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
if not GEMINI_API_KEY:
    raise ValueError("Set GEMINI_API_KEY in backend/.env")

genai.configure(api_key=GEMINI_API_KEY)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("backend.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ],
)

# ------------------------------
# 2️⃣ Conversation memory (short-term)
# ------------------------------
CONVERSATION_MEMORY = defaultdict(lambda: deque(maxlen=6))
DEFAULT_SESSION_ID = "default_user"

# ------------------------------
# 3️⃣ Request model
# ------------------------------
class QueryRequest(BaseModel):
    question: str
    strategy: str = "cot"
    k: int = 4
    reference_answer: Optional[str] = None
    use_model: Optional[str] = None

# ------------------------------
# 4️⃣ Gemini helper
# ------------------------------
def call_gemini(prompt: str, temperature=0.3, max_output_tokens=512, model_name: Optional[str] = None):
    model_to_use = model_name or GЕМINI_MODEL if 'GЕМINI_MODEL' in globals() else model_name or GEMINI_MODEL
    try:
        model = genai.GenerativeModel(model_to_use)
        logging.info(f"[Gemini] Model={model_to_use} | Prompt: {prompt[:150]}...")
        resp = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature, max_output_tokens=max_output_tokens
            ),
        )
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()
        # fallback to candidates
        if hasattr(resp, "candidates") and resp.candidates:
            try:
                return resp.candidates[0].content.parts[0].text.strip()
            except Exception:
                return str(resp.candidates[0])
        return str(resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")

# ------------------------------
# health
@app.get("/ping")
def ping():
    return {"ok": True, "time": datetime.datetime.utcnow().isoformat()}

# ------------------------------
# 5️⃣ Query endpoint (main logic)
# ------------------------------
@app.post("/query")
def query(req: QueryRequest):
    session_id = DEFAULT_SESSION_ID
    q = req.question.strip()
    strat = req.strategy if req.strategy in PROMPTS else "zero_shot"
    logging.info(f"📘 New Query | Strategy={strat} | Question={q}")

    # Step 1️⃣ Retrieve context
    try:
        retrieved = retrieve(q, k=req.k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Retrieval failed: {e}")

    context_text = "\n\n".join([
        r.get("enterprise") or r.get("educational") or r.get("topic", "")
        for r in retrieved
    ])

    # Store conversation
    CONVERSATION_MEMORY[session_id].append({"role": "user", "content": q})

    # Step 2️⃣ Build prompt
    history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in CONVERSATION_MEMORY[session_id]])
    combined_context = context_text + "\n\nChat History:\n" + history if history else context_text
    prompt = PROMPTS[strat].format(context=combined_context, question=q)
    model_name = req.use_model or GEMINI_MODEL

    # Step 3️⃣ Model call
    if strat == "tot":
        raw = call_gemini(prompt + "\n\nGenerate 5 candidate reasoning paths (1-5).", model_name=model_name)
        # parse lines with numbers (1.,2., etc.)
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
        candidates = []
        for ln in lines:
            # try to strip leading numbering
            if ln[0].isdigit() and "." in ln:
                cleaned = ln.split(".", 1)[1].strip()
            else:
                cleaned = ln
            candidates.append({"text": cleaned})
        # fallback ensure at least 2 candidates
        if len(candidates) < 2:
            candidates = [{"text": f"Fallback reasoning path for: {q} - {i}"} for i in range(1,6)]

        top2, scored_all = choose_best_two(candidates, q)
        best = top2[0][1]  # top candidate dict
        final_prompt = f"Use the chosen path:\n{best['text']}\n\nNow answer: {q}"
        final_answer = call_gemini(final_prompt, model_name=model_name)
    else:
        final_answer = call_gemini(prompt, model_name=model_name)

    # Step 4️⃣ Evaluate
    reference = (req.reference_answer or "").strip()
    evaluation = evaluate_metrics(final_answer, reference) if reference else None

    result = {
        "answer": final_answer,
        "strategy": strat,
        "retrieved": retrieved,
        "evaluation": evaluation,
    }

    # Save assistant response
    CONVERSATION_MEMORY[session_id].append({"role": "assistant", "content": final_answer})

    # Step 5️⃣ Save Results
    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = results_dir / f"{strat}_{timestamp}.json"
    txt_path = results_dir / f"{strat}_{timestamp}.txt"

    def make_json_safe(obj):
        if isinstance(obj, dict):
            return {k: make_json_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_json_safe(i) for i in obj]
        elif isinstance(obj, (set, tuple)):
            return list(obj)
        else:
            try:
                json.dumps(obj)
                return obj
            except TypeError:
                return str(obj)

    safe_result = make_json_safe(result)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(safe_result, f, ensure_ascii=False, indent=4)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"🧠 Question:\n{q}\n\n🎯 Strategy: {strat}\n\n💬 Final Answer:\n{final_answer}\n\n")
        if evaluation:
            f.write(f"📊 Evaluation:\n{json.dumps(evaluation, indent=4, ensure_ascii=False)}\n")

    return result

# ------------------------------
# 6️⃣ Dashboard endpoint
# ------------------------------
@app.get("/dashboard")
def dashboard():
    results_dir = Path(__file__).resolve().parent.parent / "results"
    if not results_dir.exists():
        raise HTTPException(status_code=404, detail="No results found")

    summaries = []
    for file in results_dir.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logging.warning(f"⚠️ Skipping {file.name}: {e}")
            continue

        evals = data.get("evaluation")
        if evals and isinstance(evals, dict):
            summaries.append({
                "file": file.name,
                "strategy": data.get("strategy"),
                "bleu": evals.get("bleu"),
                "rouge1": evals.get("rouge1_f"),
                "rougeL": evals.get("rougeL_f"),
            })

    if not summaries:
        raise HTTPException(status_code=404, detail="No valid evaluated results found")

    avg_bleu = sum((s["bleu"] or 0) for s in summaries) / len(summaries)
    avg_rouge1 = sum((s["rouge1"] or 0) for s in summaries) / len(summaries)
    avg_rougeL = sum((s["rougeL"] or 0) for s in summaries) / len(summaries)

    return {
        "total_files": len(summaries),
        "average_bleu": round(avg_bleu, 4),
        "average_rouge1": round(avg_rouge1, 4),
        "average_rougeL": round(avg_rougeL, 4),
        "evaluations": summaries,
    }
