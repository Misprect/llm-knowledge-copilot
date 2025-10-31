import json, os
from pathlib import Path 
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

BASE= Path(__file__).parent
DATA_PATH= BASE/"data"/ "genai_knowledge_base.json"
INDEX_PATH= BASE/ "index.faiss"
META_PATH= BASE/ "metadata.npy"

#load knowledge json
with open(DATA_PATH, "r", encoding="utf-8") as f:
    KB= json.load(f)
EMBED_MODEL= SentenceTransformer("all-MiniLM-L6-v2")

#These are prompting styles that control how Gemini answers:
#cot → Chain-of-Thought: reasoning steps + final answer
#cod → Compact reasoning (4 short steps)
#react → Reason + Act style prompt
#tot → Tree-of-Thought: compares reasoning paths
#few_shot → Shows examples to guide Gemini
#zero_shot → No examples, just answer from context
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

#load index and metadata helpers
#explaination of Code-
#Loads the vector index (FAISS) and metadata array from disk.
#If missing, it reminds you to run your indexing script first.
def load_index_and_meta():
    if not INDEX_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError("Index or Metadata not found. run build_index.py first")
    idx= faiss.read_index(str(INDEX_PATH))
    metas= np.load(str(META_PATH), allow_pickle=True)
    return idx, metas 

#Converts a sentence into a normalized embedding vector, which will be used to search the FAISS index.
def embed_text(text):
    vec= EMBED_MODEL.encode([text], convert_to_numpy=True)
    faiss.normalize_L2(vec)
    return vec[0]

#Explanation
#Embeds the user’s query.
#Searches the FAISS index to get the top-k most similar vectors.
#Retrieves those corresponding chunks from your knowledge base.
#Returns them as a list of context documents.
def retrieve(query, k=4):
    idx, metas= load_index_and_meta()
    qv= embed_text(query).reshape(1, -1)
    D, I= idx.search(qv, k)
    results= []
    for i in I[0]:
        m = metas[i].items()
        #include full KB text for context
        kb_item= KB[i]

        results.append({
            "id": kb_item.get("id"),
            "topic": kb_item.get("topic"),
            "educational": kb_item.get("educational_version"),
            "enterprise": kb_item.get("enterprise_version"),
            "meta": m
        })
    return results

#explaination
#Step-by-Step:
#Retrieve the top-3 relevant text chunks (retrieve(query, k=3)).
#Combine their text into one big context string.
#Format the chosen prompt (based on mode) with your context + question.
#Send that prompt to Gemini 2.5 Flash Lite.
#Return the model’s generated text.
def generate_answer(query, mode="cot", k=3):
    """Retrieve context and ask Gemini using selected prompting technique."""
    if mode not in PROMPTS:
        mode = "zero_shot"

    # Step 1: Retrieve relevant chunks
    results = retrieve(query, k=k)
    context_parts = [r.get("educational") or r.get("enterprise") or r.get("topic") for r in results]
    context = "\n".join(filter(None, context_parts))

    # Step 2: Choose the right prompt
    prompt_template = PROMPTS[mode]
    prompt = prompt_template.format(context=context, question=query)

    # Step 3: Ask Gemini
    model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
    response = model.generate_content(prompt)

    return response.text