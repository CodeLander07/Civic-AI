"use client";

import { useState } from "react";
import api from "../lib/axios";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {
    try {
      const res = await api.post("/api/query", {
        question: question,
        language: "en",
      });

      setAnswer(res.data.answer);
    } catch (error) {
      console.error(error);
      alert("Backend error");
    }
  };

  return (
    <div className="p-6">
      <input
        className="border p-2"
        placeholder="Ask something..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        onClick={askQuestion}
        className="ml-2 px-4 py-2 bg-black text-white"
      >
        Ask
      </button>

      {answer && <p className="mt-4">{answer}</p>}
    </div>
  );
}
