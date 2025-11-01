---
title: "LLM Knowledge Copilot"
description: "A Retrieval-Augmented Generation (RAG) + Evaluation system integrating CoT, CoD, ToT, ReAct, Few-Shot, and Zero-Shot prompting."
author: "Aryaman Jain"
version: "2.0.0"
license: "MIT"
date: "2025-11-01"
tags:
  [
    "LLM",
    "RAG",
    "Prompt Engineering",
    "FastAPI",
    "React",
    "Gemini API",
    "LangChain",
    "Memory",
    "Dashboard",
  ]
---

# LLM Knowledge Copilot

A complete Retrieval-Augmented Generation (RAG) application combining advanced prompting strategies with BLEU/ROUGE evaluation, a dashboard, and persistent memory.  
Built entirely with FastAPI (backend) and React (frontend), this project demonstrates how to design, reason, evaluate, and visualize AI model performance in a full-stack production setup.

---

## Features

### Core Capabilities

- End-to-End RAG Pipeline – Retrieves relevant context chunks from FAISS before generation.
- Advanced Prompt Engineering – Integrates six reasoning modes.
- Automatic BLEU & ROUGE Evaluation – Each query’s result is analyzed and logged.
- Dashboard Summary – Aggregates scores and evaluation history.
- Multi-Model Support – Seamless switching between Gemini models (2.5, 1.5 Flash, and 1.5 Pro).
- Session Memory – Saves short-term chat context and conversation history.

---

## Prompt Modes

| Prompt Type             | Description                                 |
| ----------------------- | ------------------------------------------- |
| Chain-of-Thought (CoT)  | Step-by-step reasoning before final answer  |
| Chain-of-Decision (CoD) | Logical decision-chain formation            |
| Tree-of-Thought (ToT)   | Multi-branch reasoning and scoring          |
| ReAct                   | Combines reasoning and real-world retrieval |
| Few-Shot                | Learns from few examples                    |
| Zero-Shot               | Generalizes to unseen questions             |

---

## Data & Retrieval

- Uses FAISS for efficient vector search.
- Custom Knowledge Base: `genai_knowledge_base.json` derived from personal notes.
- SentenceTransformer Embeddings for retrieval and ToT candidate scoring.

---

## Evaluation & Metrics

- Automatic scoring via BLEU and ROUGE-L/F.
- Each generation stores:
  - `/results/*.json` — structured evaluation data.
  - `/results/*.txt` — readable summaries.
- Dashboard endpoint (`/dashboard`) computes average scores and totals.

---

## Memory Integration

- Uses in-memory short-term conversation storage.
- Can be extended to persistent memory using a `.json` file or external database.
- Keeps up to 6 recent interactions per session for coherent reasoning.

---

## Architecture Overview

### Backend

- **Framework:** FastAPI
- **Modules:**
  - `rag_utils.py` – Handles context retrieval.
  - `tot_orchestrator.py` – Tree-of-Thought path selection.
  - `evaluation.py` – BLEU/ROUGE scoring.
  - `app.py` – Main logic (Gemini integration, memory, evaluation, dashboard).
- **Integrations:** Gemini API, SentenceTransformers, FAISS.

### Frontend

- **Framework:** React (Vite)
- **Libraries:** Tailwind CSS, Axios
- **Features:**
  - Strategy and model dropdowns.
  - Optional reference answer field for evaluation.
  - Dashboard visualization via REST API.

---

## How to Run Locally

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Future Improvements

### Next Enhancements

-Add a dashboard for visualizing evaluation trends with charts.
-Integrate LangChain or LlamaIndex for modular RAG pipelines.
-Expand session-based memory with persistent storage.
-Improve frontend with conversation history and real-time response visualization.
-Expand corpus for multi-domain reasoning (tech, law, medicine).

---

### Learnings

-Built a complete end-to-end RAG system integrating both backend and frontend.
-Mastered Prompt Engineering (CoT, CoD, ToT, ReAct, Few-Shot, Zero-Shot).
-Gained hands-on experience in BLEU/ROUGE-based evaluation.
-Understood FastAPI–React integration for real-world AI deployment.
-Learned version control, Git workflows, and project organization.
