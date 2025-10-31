---
title: "LLM Knowledge Copilot"
description: "A Retrieval-Augmented Generation (RAG) application integrating CoT, CoD, ToT, ReAct, Few-Shot, and Zero-Shot prompting."
author: "Aryaman Jain"
version: "1.0.0"
license: "MIT"
date: "2025-10-31"
tags: ["LLM", "RAG", "Prompt Engineering", "FastAPI", "React", "Gemini API"]
---

# 🧠 LLM Knowledge Copilot

A complete **Retrieval-Augmented Generation (RAG)** application that combines multiple advanced prompting techniques — built fully from scratch with a **FastAPI backend** and **React frontend**.

This project uses a **custom corpus (made from personal notes)** and integrates **evaluation metrics (BLEU, ROUGE)** to assess the reasoning quality of large language models (LLMs).

---

## 🚀 Features

### 🧩 Core Capabilities

- **End-to-End RAG Pipeline** – Retrieves relevant context chunks from FAISS index before generation.

---

### 🔮 Dynamic Prompt Modes

- **Chain-of-Thought (CoT)** – Step-by-step reasoning
- **Chain-of-Decision (CoD)** – Structured decision-making path
- **Tree-of-Thought (ToT)** – Parallel reasoning and scoring of multiple thought paths
- **ReAct** – Interleaves reasoning and acting for more grounded responses
- **Few-Shot** – Learns patterns from example prompts
- **Zero-Shot** – Generalizes to unseen queries without examples

---

## 🧠 Data & Retrieval

- **FAISS-based Vector Search** for fast similarity lookups
- **Custom `genai_knowledge_base.json`** built from personal notes
- **SentenceTransformer embeddings** for document retrieval and reasoning evaluation

---

## 📊 Evaluation & Metrics

- **BLEU** and **ROUGE** scores for output quality
- Automatic reasoning evaluation stored in the `/results/` directory

---

## 🏗️ Architecture Overview

### 🔹 Backend

- **FastAPI** for serving RAG endpoints
- **Gemini API** for LLM generation
- **FAISS** for vector search and retrieval

### 🔹 Frontend

Built using:

- **React (Vite)** + **Tailwind CSS** + **Axios**
- **Axios** → For making API calls to the FastAPI backend
- **React Hooks** (`useState`, `useEffect`) → To manage state and side-effects
- **Vite Dev Server** → Lightning-fast frontend environment (instead of CRA)

---

## 🧩 Prompt Modes Implemented

- Chain-of-Thought (**CoT**)
- Chain-of-Decision (**CoD**)
- Tree-of-Thought (**ToT**)
- ReAct
- Few-Shot
- Zero-Shot

---

## ⚙️ How to Run Locally

### 1️⃣ Backend

```bash
cd backend
uvicorn app:app --reload --port 8000
```

### Front end

```cd frontend
npm install
npm run dev
```
