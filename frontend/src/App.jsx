import React, { useState } from "react";

export default function App() {
  const [q, setQ] = useState("");
  const [chat, setChat] = useState([]);
  const [strategy, setStrategy] = useState("cot");

  const send = async () => {
    if (!q) return;
    setChat(prev => [...prev, { role: "user", text: q }]);
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q, strategy })
    });
    const data = await res.json();
    setChat(prev => [...prev, { role: "bot", text: data.answer, retrieved: data.retrieved, evaluation: data.evaluation }]);
    setQ("");
  };

  return (
    <div className="container">
      <h1>LLM Knowledge Copilot</h1>
      <div className="controls">
        <select value={strategy} onChange={e => setStrategy(e.target.value)}>
          <option value="cot">Chain-of-Thought</option>
          <option value="tot">Tree-of-Thought</option>
          <option value="cod">Chain-of-Density</option>
          <option value="react">ReAct</option>
          <option value="few_shot">Few-Shot</option>
          <option value="zero_shot">Zero-Shot</option>
        </select>
      </div>

      <div className="chat">
        {chat.map((m, i) => (
          <div key={i} className={m.role === "user" ? "msg user" : "msg bot"}>
            <div style={{ whiteSpace: "pre-wrap" }}>{m.text}</div>
            {m.retrieved && m.retrieved.length > 0 && (
              <details>
                <summary>Retrieved</summary>
                <ul>
                  {m.retrieved.map((r, idx) => (
                    <li key={idx}>{r.id} — {r.topic}</li>
                  ))}
                </ul>
              </details>
            )}
            {m.evaluation && (
              <div className="eval">
                <small>Eval: BLEU {m.evaluation?.bleu ?? "-"} ROUGE1 {m.evaluation?.rouge1_f ?? "-"} MSE {m.evaluation?.mse_length ?? "-"}</small>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="composer">
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="Ask something from your notes..." />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
