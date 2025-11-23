import React, { useState } from "react";
import axios from "axios";
import JsonViewer from "./components/JsonViewer";
import ScoreChart from "./components/ScoreChart";

export default function App() {
  const [question, setQuestion] = useState("");
  const [reference, setReference] = useState("");
  const [answer, setAnswer] = useState("");
  const [strategy, setStrategy] = useState("cot");
  const [useModel, setUseModel] = useState("gemini-2.5-flash-lite");
  const [evaluation, setEvaluation] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rawJson, setRawJson] = useState(null);

  const handleSubmit = async () => {
    if (!question.trim()) return alert("Enter a question!");
    setLoading(true);
    setAnswer("");
    setEvaluation(null);
    setRawJson(null);

    try {
      // 🔥 FIXED: send directly to backend port 8000
      const res = await axios.post("http://localhost:8000/query", {
        question,
        strategy,
        k: 4,
        reference_answer: reference || null,
        use_model: useModel,
      });

      setAnswer(res.data.answer || "");
      setEvaluation(res.data.evaluation || null);
      setRawJson(res.data || null);
    } catch (err) {
      console.error(err);
      const msg = err?.response?.data?.detail || err.message;
      alert("Error: " + msg);
    } finally {
      setLoading(false);
    }
  };

  const loadDashboard = async () => {
    try {
      // 🔥 FIXED: backend dashboard endpoint on port 8000
      const res = await axios.get("http://localhost:8000/dashboard");
      setDashboard(res.data);
    } catch (err) {
      console.error(err);
      alert("No results found yet or dashboard error.");
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto text-gray-800 space-y-6">
      <h1 className="text-3xl font-bold text-center mb-6">🧠 LLM Knowledge Copilot</h1>

      <textarea
        className="w-full p-3 border rounded-lg"
        rows="3"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <textarea
        className="w-full p-3 border rounded-lg"
        rows="2"
        placeholder="(Optional) Reference answer for evaluation..."
        value={reference}
        onChange={(e) => setReference(e.target.value)}
      />

      <div className="flex flex-wrap gap-3">
        <select
          className="border p-2 rounded"
          value={strategy}
          onChange={(e) => setStrategy(e.target.value)}
        >
          <option value="cot">Chain-of-Thought</option>
          <option value="cod">Chain-of-Decision</option>
          <option value="tot">Tree-of-Thought</option>
          <option value="react">ReAct</option>
          <option value="few_shot">Few-Shot</option>
          <option value="zero_shot">Zero-Shot</option>
        </select>

        <select
          className="border p-2 rounded"
          value={useModel}
          onChange={(e) => setUseModel(e.target.value)}
        >
          <option value="gemini-2.5-flash-lite">Gemini 2.5 Flash Lite</option>
          <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
          <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
        </select>

        <button
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Generating..." : "Ask"}
        </button>

        <button
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          onClick={loadDashboard}
        >
          View Dashboard
        </button>
      </div>

      {answer && (
        <div className="p-4 bg-gray-100 rounded-lg border">
          <h3 className="font-semibold mb-2">💬 Answer:</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>{answer}</pre>
        </div>
      )}

      {evaluation && (
        <div className="p-4 bg-yellow-50 rounded-lg border">
          <h3 className="font-semibold mb-2">📊 Evaluation Metrics:</h3>
          <pre>{JSON.stringify(evaluation, null, 2)}</pre>
        </div>
      )}

      {rawJson && <JsonViewer data={rawJson} />}

      {dashboard && (
        <div className="p-4 bg-gray-50 rounded-lg border mt-4">
          <h3 className="font-semibold mb-2">📈 Dashboard Summary</h3>
          <p>Total Results: {dashboard.total_files}</p>
          <p>Avg BLEU: {dashboard.average_bleu}</p>
          <p>Avg ROUGE-1: {dashboard.average_rouge1}</p>
          <p>Avg ROUGE-L: {dashboard.average_rougeL}</p>

          <ScoreChart
            bleu={dashboard.average_bleu}
            rouge1={dashboard.average_rouge1}
            rougeL={dashboard.average_rougeL}
          />
        </div>
      )}
    </div>
  );
}
