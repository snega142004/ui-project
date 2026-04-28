import { useState } from "react";
import API from "../api/axios";

export default function InputBox({ threadId, refresh }: any) {
  const [input, setInput] = useState("");

  const send = async () => {
    if (!input) return;

    await API.post("/chat", {
      message: input,
      thread_id: threadId,
      user_id: 1
    });

    setInput("");
    refresh();
  };

  return (
    <div className="inputBox">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Send a message..."
      />
      <button onClick={send}>Send</button>
    </div>
  );
}