import React, { useState } from "react";

export default function JsonViewer({ data }) {
  const [expanded, setExpanded] = useState(false);
  if (!data) return null;

  return (
    <div className="mt-4 p-4 bg-gray-50 border rounded-lg">
      <button
        className="bg-gray-800 text-white px-3 py-1 rounded text-sm mb-3"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? "Hide JSON" : "Show Raw JSON"}
      </button>

      {expanded && (
        <pre className="bg-black text-green-400 p-3 rounded max-h-96 overflow-auto text-sm">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  );
}
