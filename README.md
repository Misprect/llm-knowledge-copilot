#LLM Knowledge Copilot
A complete **Retrieval-Augmented Generation (RAG)** application that integrates **prompting techniques** like CoT, CoD, ToT, ReAct, Few-Shot, and Zero-Shot with a custom corpus built from my own notes.  
It includes both a **FastAPI backend** and a **React frontend**, communicating seamlessly.
##Features
- **RAG-powered reasoning** with context retrieval.
- **Prompting strategies**:
  - **Chain-of-Thought (CoT)** – Step-by-step reasoning.
  - **Chain-of-Decision (CoD)** – Logical decision-making path.
  - **Tree-of-Thought (ToT)** – Parallel reasoning branches.
  - **ReAct** – Reason + Act framework.
  - **Few-Shot & Zero-Shot** – Learning from examples vs. none.
- **FAISS-based vector search** for document retrieval.
- **Custom evaluation metrics** (BLEU, ROUGE).
- **Frontend:** React + Vite
- **Backend:** FastAPI + Gemini API

