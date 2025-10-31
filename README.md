---
title: "LLM Knowledge Copilot"
description: "A Retrieval-Augmented Generation (RAG) application integrating CoT, CoD, ToT, ReAct, Few-Shot, and Zero-Shot prompting."
author: "Aryaman Jain"
version: "1.0.0"
license: "MIT"
date: "2025-10-31"
tags: ["LLM", "RAG", "Prompt Engineering", "FastAPI", "React", "Gemini API"]
---

# LLM Knowledge Copilot

A complete **Retrieval-Augmented Generation (RAG)** application that combines multiple advanced prompting techniques — built fully from scratch with a **FastAPI backend** and **React frontend**.  
This project uses a **custom corpus (from personal notes)** and integrates **BLEU** and **ROUGE** metrics to evaluate the reasoning quality of large language models (LLMs).

---

## Features

### Core Capabilities

- **End-to-End RAG Pipeline** – Retrieves relevant context chunks from FAISS index before generation.
- **Contextual reasoning** powered by prompt engineering techniques and Gemini API.

---

### Dynamic Prompt Modes

- **Chain-of-Thought (CoT):** Step-by-step reasoning.
- **Chain-of-Decision (CoD):** Structured decision-making path.
- **Tree-of-Thought (ToT):** Parallel reasoning and scoring of multiple thought branches.
- **ReAct:** Interleaves reasoning and acting for more grounded responses.
- **Few-Shot:** Learns patterns from example prompts.
- **Zero-Shot:** Generalizes to unseen queries without examples.

---

## Data & Retrieval

- **FAISS-based Vector Search** for fast similarity lookups.
- **Custom Knowledge Base:** `genai_knowledge_base.json` built from personal notes.
- **SentenceTransformer Embeddings** used for semantic retrieval and ToT scoring.

---

## Evaluation & Metrics

- **BLEU** and **ROUGE** scores for evaluating generation quality.
- **Automatic evaluation** of model outputs stored in the `/results/` folder.
- Separate `.txt` and `.json` files for final answers and evaluations.

---

## Architecture

### Backend

- **Framework:** FastAPI
- **Integrations:** Gemini API, FAISS, SentenceTransformers
- **Modules:**
  - `rag_utils.py` – Handles retrieval logic
  - `tot_orchestrator.py` – Tree-of-Thought scoring and selection
  - `evaluation.py` – BLEU & ROUGE evaluation
  - `app.py` – Main API endpoint layer

---

### Frontend

- **Framework:** React (Vite)
- **Libraries:** Tailwind CSS, Axios
- **Tools & Concepts:**
  - Vite Dev Server for fast builds
  - React Hooks (`useState`, `useEffect`) for state management
  - Axios for backend communication via REST API

---

## Prompt Modes Implemented

**CoT**, **CoD**, **ToT**, **ReAct**, **Few-Shot**, and **Zero-Shot** — each mode dynamically formats prompts before sending them to Gemini for reasoning.

---

## Future Improvements & Learnings

### Next Enhancements

- Add a **dashboard** for visualizing evaluation metrics (BLEU/ROUGE trends).
- Integrate **LangChain or LlamaIndex** for flexible retrieval pipelines.
- Add **session-based chat memory** for multi-turn reasoning.
- Improve UI with **conversation history** and real-time feedback.
- Expand the corpus to support **multiple domains** (tech, law, medicine).

---

### Learnings

- Built a **complete RAG system from scratch**, integrating both backend + frontend.
- Gained hands-on understanding of **prompt engineering techniques** (CoT, CoD, ToT, ReAct).
- Learned how to evaluate **LLM reasoning quality** using BLEU/ROUGE.
- Understood how **React & FastAPI** can communicate for a full-stack AI project.
- Mastered **Git, versioning, and deployment** best practices.

---

## License

This project is licensed under the **MIT License** — feel free to use and modify it.
