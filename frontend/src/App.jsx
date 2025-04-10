// frontend/src/App.jsx
import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [fileId, setFileId] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setFileId(data.file_id);
  };

  const submitQuestion = async () => {
    if (!question || !fileId) return;
    const formData = new FormData();
    formData.append("question", question);
    formData.append("file_id", fileId);
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div>
      <h1>CSV LLM Reasoning App</h1>
      <div>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button onClick={uploadFile}>Upload CSV</button>
      </div>
      {fileId && (
        <div>
          <p>Uploaded File ID: {fileId}</p>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask your reasoning question..."
          />
          <button onClick={submitQuestion}>Submit Question</button>
        </div>
      )}
      {answer && (
        <div>
          <h2>Answer:</h2>
          <pre>{answer}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
