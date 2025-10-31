##LLM Knowledge Copilot
A complete Retrieval-Augmented Generation (RAG) application that combines multiple advanced prompting techniques — built fully from scratch with a FastAPI backend and React frontend.
This project uses a custom corpus (made from personal notes) and integrates evaluation metrics (BLEU, ROUGE) to assess the reasoning quality of large language models (LLMs).

##Features
#Core Capabilities
End-to-End RAG Pipeline – Retrieves relevant context chunks from FAISS index before generation.

##Dynamic Prompt Modes:
-Chain-of-Thought (CoT) – Step-by-step reasoning.
-Chain-of-Decision (CoD) – Structured decision-making path.
-Tree-of-Thought (ToT) – Parallel reasoning and scoring of multiple thought paths.
-ReAct – Interleaves reasoning and acting for more grounded responses.
-Few-Shot – Learns patterns from example prompts.
-Zero-Shot – Generalizes to unseen queries without examples.

##Data & Retrieval
-FAISS-based Vector Search for fast similarity lookups.
-Custom genai_knowledge_base.json built from personal notes.
-SentenceTransformer embeddings for document retrieval and reasoning evaluation.

##Evaluation & Metrics
-BLEU and ROUGE scores for output quality.
-Automatic reasoning evaluation stored in /results/.

##Architecture
-Backend: FastAPI + Gemini API + FAISS
-Frontend: React (Vite) + Tailwind + Axios
  -React(Vite)+ Tailwind CSS + Axios + Vit dev server
  -Axios- For making API calls to your FastAPI backend.
  -React(Vite)-Framework + bundler for building the user interface.
  -React Hooks (useState, useEffect)-For managing state and side-effects when interacting with backend endpoints.
  -Vite Dev Server-Super-fast development server used instead of Create React App (CRA).
Frontend: React (Vite) + Tailwind + Axios

##Prompt Modes: CoT, CoD, ToT, ReAct, Few-Shot, Zero-Shot
