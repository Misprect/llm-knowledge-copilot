import os
import json
import time
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai
# ---------------------------
# SETUP
# ---------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-lite"
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
# ---------------------------
# LLM CALL WITH TIMER
# ---------------------------
def ask_gemini_with_stats(prompt: str):
    start = time.time()

    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        answer = response.text.strip()
    except Exception as e:
        answer = f"[LLM ERROR: {e}]"

    end = time.time()
    latency = round(end - start, 4)

    # token count (approx because Gemini does not return tokens)
    token_count = len(answer.split())

    return answer, latency, token_count
# ---------------------------
# SCORE FUNCTION
# ---------------------------
def score_answer(question: str, answer: str):
    q_emb = embed_model.encode(question, convert_to_tensor=True)
    a_emb = embed_model.encode(answer, convert_to_tensor=True)
    score = float(util.cos_sim(q_emb, a_emb).item())
    return round(score, 4)
# ---------------------------
# EVALUATOR
# ---------------------------
def evaluate_answer(question: str, answer: str, score: float):
    # Define simple rule
    threshold = 0.50
    passed = score >= threshold
    return passed, threshold
# ---------------------------
# SAVE RESULTS
# ---------------------------
def save_stats(question, answer, latency, tokens, score, passed):
    result_dir = "results/week10_stats"
    os.makedirs(result_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(result_dir, f"stats_{timestamp}.json")
    txt_path = os.path.join(result_dir, f"stats_{timestamp}.txt")

    data = {
        "question": question,
        "answer": answer,
        "latency_seconds": latency,
        "token_count": tokens,
        "similarity_score": score,
        "passed_threshold": passed
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("📊 WEEK 10 LLM STATS REPORT\n\n")
        f.write(f"Question: {question}\n\n")
        f.write(f"Answer: {answer}\n\n")
        f.write(f"⏱ Latency: {latency} sec\n")
        f.write(f"🔢 Token Count: {tokens}\n")
        f.write(f"🔍 Similarity Score: {score}\n")
        f.write(f"✅ Passed: {passed}\n")

    print(f"Saved stats report in {result_dir}")
# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    question = input("Enter any question: ")

    answer, latency, tokens = ask_gemini_with_stats(question)
    score = score_answer(question, answer)
    passed, threshold = evaluate_answer(question, answer, score)

    print("\n📌 LLM Answer:", answer)
    print("⏱ Latency:", latency)
    print("🔢 Token Count:", tokens)
    print("🔍 Score:", score)
    print("✔ Passed:", passed)

    save_stats(question, answer, latency, tokens, score, passed)