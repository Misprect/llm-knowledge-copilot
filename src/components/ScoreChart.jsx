import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function ScoreChart({ bleu = 0, rouge1 = 0, rougeL = 0 }) {
  const data = {
    labels: ["BLEU", "ROUGE-1", "ROUGE-L"],
    datasets: [
      {
        label: "Evaluation Scores",
        data: [bleu, rouge1, rougeL],
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      y: { beginAtZero: true, max: 1 },
    },
  };

  return (
    <div className="p-4 bg-white rounded shadow mt-4">
      <h3 className="font-semibold mb-2">📊 Score Bar Chart</h3>
      <div style={{ maxWidth: 600 }}>
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}
