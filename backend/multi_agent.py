# use your previously posted multi_agent code but ensure call_llm exists
# I provide a safe version here — replace your multi_agent.py with this:

import os, json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-lite"

def call_llm(prompt: str):
    try:
        model = genai.GenerativeModel(MODEL)
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"[LLM Error: {e}]"

def researcher_agent(question):
    prompt = f"""ROLE: Researcher
TASK: Search for relevant knowledge and brainstorm multiple facts.

Question: {question}

Researcher's Output:
"""
    return call_llm(prompt)

def critic_agent(research_output: str):
    prompt = f"""ROLE: Critic
TASK: Check facts and correct the researcher's answer.
Researcher's Output:
{research_output}

Critic's Verified Output:
"""
    return call_llm(prompt)

def summarizer_agent(verified_output: str):
    prompt = f"""ROLE: Summarizer
TASK: Produce a short, clear summary.

Input to summarize:
{verified_output}

Final Summary:
"""
    return call_llm(prompt)

def save_results(question, researcher, critic, summary):
    result_dir = "results/week9_multi_agent"
    os.makedirs(result_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(result_dir, f"agent_run_{timestamp}.json")
    txt_path = os.path.join(result_dir, f"agent_run_{timestamp}.txt")
    data = {"question": question, "researcher_output": researcher, "critic_output": critic, "final_summary": summary}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("🧩 Multi-Agent Reasoning\n\n")
        f.write(f"Question: {question}\n\n")
        f.write("--- Researcher Output ---\n")
        f.write(researcher + "\n\n")
        f.write("--- Critic Output ---\n")
        f.write(critic + "\n\n")
        f.write("--- Final Summary ---\n")
        f.write(summary + "\n")
    print(f"Saved multi-agent results in {result_dir}")

def run_agents(question: str):
    researcher = researcher_agent(question)
    critic = critic_agent(researcher)
    summary = summarizer_agent(critic)
    save_results(question, researcher, critic, summary)
    return {"researcher": researcher, "critic": critic, "summary": summary}

if __name__ == "__main__":
    q = "Explain why self-attention scales better than RNNs for long sequences."
    print(run_agents(q))
