import json, os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
# unify on GEMINI_API_KEY name
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

BASE = Path(__file__).parent
DATA_PATH = BASE / "data" / "genai_knowledge_base.json"
INDEX_PATH = BASE / "index.faiss"
META_PATH = BASE / "metadata.npy"

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

PROMPTS = {
    "cot": """You are an expert AI instructor. Use step-by-step chain-of-thought reasoning before presenting the final concise answer.
Context:
{context}
Question: {question}
Answer (show reasoning then final):""",
    "cod": """Provide a dense, information-rich 4-step chain. Keep each step under 20 words, then a 10-word summary.
Context:
{context}
Question: {question}
Answer:""",
    "react": """You are an AI agent.
THINK: Analyze the context and decide whether to use the retrieved context or answer from knowledge. Show your reasoning.
ACT: Provide the final answer for the user.
Context:
{context}
Question: {question}
""",
    "tot": """You are to propose 3 candidate reasoning paths for answering the question.
For each path: list 3 steps and a one-line rationale. Then compare pros/cons and pick the best.
Context:
{context}
Question: {question}
""",
    "few_shot": """Example 1:
Input: What is a neural network?
Output: A computational model inspired by the brain that learns patterns via layers.

Example 2:
Input: What is attention in NLP?
Output: Attention lets a model weigh token relevance across a sequence.

Now:
Input: {question}
Output:""",
    "zero_shot": """Answer concisely using the context.
Context:
{context}
Question: {question}
Answer:""",
}

def load_index_and_meta():
    if not INDEX_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError("Index or Metadata not found. run build_index.py first")
    idx = faiss.read_index(str(INDEX_PATH))
    metas = np.load(str(META_PATH), allow_pickle=True)
    return idx, metas

def embed_text(text):
    vec = EMBED_MODEL.encode([text], convert_to_numpy=True)
    faiss.normalize_L2(vec)
    return vec[0]

def retrieve(query, k=4):
    idx, metas = load_index_and_meta()
    qv = embed_text(query).reshape(1, -1)
    D, I = idx.search(qv, k)
    results = []
    from pathlib import Path
    # load original KB
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        KB = json.load(f)

    for i in I[0]:
        kb_item = KB[i]
        results.append({
            "id": kb_item.get("id"),
            "topic": kb_item.get("topic"),
            "educational": kb_item.get("educational_version"),
            "enterprise": kb_item.get("enterprise_version"),
            "meta": metas[i] if metas is not None else {}
        })
    return results

def generate_answer(query, mode="cot", k=3):
    if mode not in PROMPTS:
        mode = "zero_shot"
    results = retrieve(query, k=k)
    context_parts = [r.get("educational") or r.get("enterprise") or r.get("topic") for r in results]
    context = "\n".join(filter(None, context_parts))
    prompt_template = PROMPTS[mode]
    prompt = prompt_template.format(context=context, question=query)
    model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
    response = model.generate_content(prompt)
    return response.text
