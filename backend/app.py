import os, json, logging, datetime, sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.rag_utils import retrieve, PROMPTS
from backend.tot_orchestrator import choose_best
from backend.evaluation import evaluate_metrics
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------
# 0️⃣ Fix Windows encoding (emoji-safe logging)
# ------------------------------
sys.stdout.reconfigure(encoding='utf-8')

# ------------------------------
# 1️⃣ Setup and Config
# ------------------------------
load_dotenv()
app = FastAPI(title="LLM Knowledge Copilot (Gemini Edition)")

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

if not GEMINI_API_KEY:
    raise ValueError("Set GEMINI_API_KEY in backend/.env")

genai.configure(api_key=GEMINI_API_KEY)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("backend.log", encoding='utf-8'), logging.StreamHandler(sys.stdout)]
)

# ------------------------------
# 2️⃣ Request Model
# ------------------------------
class QueryRequest(BaseModel):
    question: str
    strategy: str = "cot"
    k: int = 4
    reference_answer: str | None = None

# ------------------------------
# 3️⃣ Gemini Call Helper
# ------------------------------
def call_gemini(prompt: str, temperature=0.3, max_output_tokens=512):
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        logging.info(f"[Gemini] Calling {GEMINI_MODEL} | Prompt: {prompt[:200]}...")
        resp = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens
            )
        )
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()
        if hasattr(resp, "candidates") and resp.candidates:
            return resp.candidates[0].content.parts[0].text.strip()
        return str(resp)
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")

# ------------------------------
# 4️⃣ Query Endpoint
# ------------------------------
@app.post("/query")
def query(req: QueryRequest):
    q = req.question.strip()
    strat = req.strategy if req.strategy in PROMPTS else "zero_shot"
    logging.info(f"📘 New Query | Strategy={strat} | Question={q}")

    # Step 1️⃣ Retrieve context
    try:
        retrieved = retrieve(q, k=req.k)
    except Exception as e:
        logging.error(f"RAG Retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"RAG Retrieval failed: {e}")

    context_text = "\n\n".join([
        r.get("enterprise") or r.get("educational") or r.get("topic", "")
        for r in retrieved
    ])
    logging.info(f"Retrieved {len(retrieved)} context chunks.")

    # Step 2️⃣ Build prompt
    prompt_template = PROMPTS[strat]
    prompt = prompt_template.format(context=context_text, question=q)

    # Step 3️⃣ Strategy logic
    if strat == "tot":
        candidate_prompt = prompt + "\n\nGenerate 3 candidate reasoning paths labeled Path A, Path B, Path C."
        raw = call_gemini(candidate_prompt)
        parts = [p.strip() for p in raw.split("Path") if p.strip()]
        candidates = [{"text": ("Path " + p)} for p in parts]

        # Safely call choose_best
        best, scored = choose_best(candidates, q)

        # ✅ Ensure scored is serializable (list of tuples)
        if isinstance(scored, dict):
            scored_pairs = [(k, v.get("text", "")[:120]) for k, v in scored.items()]
        elif isinstance(scored, list):
            scored_pairs = [(k, v.get("text", "")[:120]) for k, v in scored]
        else:
            scored_pairs = []

        final_prompt = f"Use the chosen path:\n{best['text']}\n\nNow answer: {q}"
        final_answer = call_gemini(final_prompt)
        evaluation = evaluate_metrics(final_answer, req.reference_answer) if req.reference_answer else None

        result = {
            "answer": final_answer,
            "strategy": strat,
            "retrieved": retrieved,
            "candidates_scored": scored_pairs,  # ✅ safe list
            "evaluation": evaluation,
        }

    elif strat in ["cot", "cod", "react", "few_shot"]:
        final_answer = call_gemini(prompt)
        evaluation = evaluate_metrics(final_answer, req.reference_answer) if req.reference_answer else None
        result = {
            "answer": final_answer,
            "strategy": strat,
            "retrieved": retrieved,
            "evaluation": evaluation,
        }

    else:
        zero_prompt = PROMPTS["zero_shot"].format(context=context_text, question=q)
        final_answer = call_gemini(zero_prompt)
        evaluation = evaluate_metrics(final_answer, req.reference_answer) if req.reference_answer else None
        result = {
            "answer": final_answer,
            "strategy": "zero_shot",
            "retrieved": retrieved,
            "evaluation": evaluation,
        }

    # Step 4️⃣ Convert everything to JSON-safe
    def make_json_safe(obj):
        if isinstance(obj, dict):
            return {k: make_json_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_json_safe(i) for i in obj]
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, tuple):
            return [make_json_safe(i) for i in obj]
        elif isinstance(obj, type({}.items())):
            return list(obj)
        else:
            try:
                json.dumps(obj)
                return obj
            except TypeError:
                return str(obj)

    result = make_json_safe(result)

    # Step 5️⃣ Save Results (JSON + TXT)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    json_path = results_dir / f"{strat}_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    txt_path = results_dir / f"{strat}_{timestamp}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"🧠 Question:\n{q}\n\n")
        f.write(f"🎯 Strategy: {strat}\n\n")
        f.write(f"💬 Final Answer:\n{result['answer']}\n\n")
        if result.get("evaluation"):
            f.write(f"📊 Evaluation:\n{json.dumps(result['evaluation'], indent=4)}\n")
        else:
            f.write("📊 Evaluation: None (No reference answer provided)\n")

    logging.info(f"✅ Saved files: {json_path.name}, {txt_path.name}")
    return result
