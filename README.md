```markdown
---
title: "LLM Knowledge Copilot"
description: "A Retrieval-Augmented Generation (RAG) + Evaluation system integrating CoT, CoD, ToT, ReAct, Few-Shot, Zero-Shot, Multi-Agent, and Stats Dashboard."
author: "Aryaman Jain"
version: "2.2.0"
license: "MIT"
date: "2025-11-24"
tags:
  [
    "LLM",
    "RAG",
    "Prompt Engineering",
    "FastAPI",
    "React",
    "Gemini API",
    "FAISS",
    "SentenceTransformers",
    "Evaluation",
    "Dashboard",
    "Multi-Agent",
  ]
---

# LLM Knowledge Copilot

A full-stack Retrieval-Augmented Generation (RAG) system with advanced prompting strategies, multi-agent reasoning, automated evaluation (BLEU/ROUGE), stats dashboard, and session memory.  
Built using **FastAPI (backend)** and **React + Vite (frontend)**, this project demonstrates real-world AI reasoning, evaluation pipeline engineering, and frontend analytics.

---

## Features

### Core Capabilities

- **End-to-End RAG Pipeline**  
  Retrieves relevant context from FAISS + SentenceTransformer embeddings.

- **Advanced Prompt Engineering**  
  Six reasoning modes + Multi-Agent + ToT Orchestrator.

- **Automatic BLEU & ROUGE Evaluation**  
  All runs stored as JSON + TXT summaries in `/results`.

- **Dashboard & Stats**  
  Aggregates performance, accuracy, BLEU/ROUGE averages, and history.

- **Gemini API Integration**  
  Supports 2.5 Flash, 1.5 Flash, 1.5 Pro, and others.

- **Session Memory**  
  Short-term contextual memory for consistent responses.

---

## Prompt Modes

| Prompt Type             | Description                                        |
| ----------------------- | -------------------------------------------------- |
| Chain-of-Thought (CoT)  | Step-by-step reasoning before final answer         |
| Chain-of-Decision (CoD) | Decision-based logical reasoning chain             |
| Tree-of-Thought (ToT)   | Multi-branch reasoning with scoring via embeddings |
| ReAct                   | Interleaves reasoning + retrieval actions          |
| Few-Shot                | Learns from provided examples                      |
| Zero-Shot               | Answers without examples                           |
| Multi-Agent Reasoning   | Two agents collaborate + critique + finalize       |

---

## Data & Retrieval

- Uses **FAISS** (IndexFlatL2) for semantic vector search.
- Embeddings generated using **SentenceTransformer**.
- Custom knowledge base stored at:
```

backend/data/genai_knowledge_base.json

```
- Retrieval logic implemented inside `rag_utils.py`.

---

## Evaluation & Metrics

Each query produces a pair of result files:

- `/results/*.json` — raw structured reasoning + BLEU/ROUGE metrics
- `/results/*.txt` — human-readable report

Plus experiment folders:

```

results/week8_tot/
results/week9_multi_agent/
results/week10_stats/

```

### Metrics computed:

- **BLEU**
- **ROUGE-L**
- **ROUGE-F1**
- **Token analysis**
- **Strategy comparison**

Stats calculations handled in `backend/stats.py`.

---

## Memory Integration

- Stores the **last 6 interactions** in a lightweight in-memory buffer.
- Enhances reasoning and continuity.
- Upgradable to persistent long-term memory via:
  - JSON database
  - SQLite / Postgres
  - LangChain memory

---

## Architecture Overview

### Backend

- **Framework:** FastAPI
- **Modules:**
  - `app.py` — core controller, endpoints, routing
  - `rag_utils.py` — FAISS retrieval
  - `tot_orchestrator.py` — candidate scoring + optimal branch selection
  - `multi_agent.py` — debate/collaboration reasoning
  - `stats.py` — results aggregation & dashboard metrics
- **Integrations:**
  - Gemini API
  - FAISS
  - SentenceTransformers

### Frontend

- **Framework:** React + Vite
- **Files:**
```

src/App.jsx
src/components/JsonViewer.jsx
src/components/ScoreChart.jsx
src/main.jsx
src/style.css

```
- **Features:**
- Dropdowns for model + strategy
- Optional reference answer input
- Results viewer with JSON renderer
- Chart visualizations (Scores over time)
- Axios-based backend communication

---

## Project Structure

```

backend/
app.py
rag_utils.py
tot_orchestrator.py
multi_agent.py
stats.py
data/
genai_knowledge_base.json
results/
_.json / _.txt
week8_tot/
week9_multi_agent/
week10_stats/

src/
App.jsx
components/
JsonViewer.jsx
ScoreChart.jsx
main.jsx
style.css

index.html
package.json
.gitignore

````

---

## How to Run Locally

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
````

### 2. Start Frontend

```bash
npm install
npm run dev
```

---

## Future Improvements

### Planned Enhancements

- Larger, multi-domain knowledge base for stronger RAG.
- Persistent memory (SQLite or JSON).
- Multi-agent reasoning visualization.
- More advanced evaluation (METEOR, BERTScore).
- Real-time streaming responses in the UI.
- Uploadable documents → dynamic FAISS retraining.

---

## Learnings

- Built a production-ready full-stack RAG system.
- Deep understanding of CoT, CoD, ToT, ReAct, Few/Zero-Shot prompting.
- Implemented evaluation using BLEU/ROUGE + visualization.
- Gained experience with FastAPI–React architectures.
- Mastered Git workflows and clean project structuring.
- Learned multi-agent and tree-based reasoning design.

---
