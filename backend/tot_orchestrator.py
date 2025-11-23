import os
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai

# Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-lite"

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------------------------
# LLM CALL
# ---------------------------------------------
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[LLM ERROR: {e}]"

# ---------------------------------------------
# SCORE FUNCTION (same as before)
# ---------------------------------------------
def score_candidate(candidate_text: str, question: str):
    q_emb = embed_model.encode(question, convert_to_tensor=True)
    c_emb = embed_model.encode(candidate_text, convert_to_tensor=True)
    return float(util.cos_sim(q_emb, c_emb).item())
# ---------------------------------------------
# NEW: AUTO-GENERATE 5 ToT REASONING CANDIDATES
# ---------------------------------------------
def generate_candidates(question: str):
    prompt = f"""
Generate exactly 5 distinct Tree-of-Thought reasoning paths for this question:

Question: {question}

FORMAT STRICTLY LIKE THIS (one per line):

1. path text
2. path text
3. path text
4. path text
5. path text
"""
    output = ask_gemini(prompt)

    candidates = []
    for line in output.split("\n"):
        line = line.strip()

        # Only keep lines that start with "1.", "2.", ..., "5."
        if any(line.startswith(f"{i}.") for i in range(1, 6)):
            # remove numbering and clean bullets
            cleaned = line.split(".", 1)[1].strip()
            cleaned = cleaned.lstrip("*").strip()
            candidates.append(cleaned)

    # If fewer than 5 extracted, retry once
    if len(candidates) < 5:
        print("⚠️ LLM did not produce 5 reasoning paths. Regenerating...")
        return generate_candidates(question)

    return [{"path_id": i+1, "text": candidates[i]} for i in range(5)]

# ---------------------------------------------
# CHOOSE BEST TWO
# ---------------------------------------------
def choose_best_two(candidates, question):
    scored = []
    for cand in candidates:
        score = score_candidate(cand["text"], question)
        scored.append((score, cand))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:2], scored

# ---------------------------------------------
# SAVE RESULTS
# ---------------------------------------------
def save_results(question, top2, all_scored):
    result_dir = "results/week8_tot"
    os.makedirs(result_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(result_dir, f"tot_results_{timestamp}.json")
    txt_path = os.path.join(result_dir, f"tot_results_{timestamp}.txt")

    # Save JSON
    data = {
        "question": question,
        "top2": [{"score": s, "text": c["text"]} for s, c in top2],
        "all_candidates": [{"score": s, "text": c["text"]} for s, c in all_scored]
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # Save TXT
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Question: {question}\n\n")
        f.write("--- TOP 2 ANSWERS ---\n")
        for s, c in top2:
            f.write(f"{s:.3f} -> {c['text']}\n\n")

        f.write("--- ALL SCORES ---\n")
        for s, c in all_scored:
            f.write(f"{s:.3f} -> {c['text']}\n")

    print(f"Saved ToT results to {result_dir}")

# ---------------------------------------------
# MAIN
# ---------------------------------------------
if __name__ == "__main__":
    question = input("Ask any question: ")

    candidates = generate_candidates(question)
    top2, all_scored = choose_best_two(candidates, question)

    print("\n🧠 BEST TWO ANSWERS:")
    for s, c in top2:
        print(f"{s:.3f} -> {c['text']}")

    save_results(question, top2, all_scored)
