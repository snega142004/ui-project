import { useEffect, useState } from "react";
import API from "../api/axios";

export default function Chat() {
  const [threads, setThreads] = useState<any[]>([]);
  const [currentThread, setCurrentThread] = useState<number | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const email = localStorage.getItem("email");

  useEffect(() => {
    loadThreads();
  }, []);

  const loadThreads = async () => {
    const res = await API.get("/threads/");
    setThreads(res.data);
  };

  const createThread = async () => {
    const res = await API.post("/threads/?title=New Chat");
    setCurrentThread(res.data.thread_id);
    setMessages([]);
    loadThreads();
  };

  const loadMessages = async (id: number) => {
    const res = await API.get(`/messages/${id}`);
    setMessages(res.data);
    setCurrentThread(id);
  };

  const deleteThread = async (id: number) => {
    await API.delete(`/threads/${id}`);
    loadThreads();
    if (id === currentThread) {
      setMessages([]);
      setCurrentThread(null);
    }
  };

  const renameThread = async (id: number) => {
    const newTitle = prompt("Enter new title");
    if (!newTitle) return;

    await API.put(`/threads/${id}`, { title: newTitle });
    loadThreads();
  };

  const sendMessage = async () => {
    if (!input || !currentThread) return;

    const question = input;

    setMessages(prev => [...prev, { role: "user", message: question }]);
    setInput("");
    setLoading(true);

    const res = await API.post("/messages/", {
      thread_id: currentThread,
      message: question
    });

    setMessages(prev => [
      ...prev,
      { role: "assistant", message: res.data.reply }
    ]);

    setLoading(false);

    // 🔥 AUTO TITLE
    const thread = threads.find(t => t.id === currentThread);
    if (thread && thread.title === "New Chat") {
      await API.put(`/threads/${currentThread}`, {
        title: question.slice(0, 40)
      });
      loadThreads();
    }
  };

  // 🔥 DATE GROUPING
  const today = new Date();
  const yesterday = new Date();
  yesterday.setDate(today.getDate() - 1);

  const isSameDay = (d1: Date, d2: Date) =>
    d1.toDateString() === d2.toDateString();

  const todayChats = threads.filter((t: any) =>
    isSameDay(new Date(t.created_at), today)
  );

  const yesterdayChats = threads.filter((t: any) =>
    isSameDay(new Date(t.created_at), yesterday)
  );

  const olderChats = threads.filter((t: any) => {
    const d = new Date(t.created_at);
    return (
      !isSameDay(d, today) &&
      !isSameDay(d, yesterday)
    );
  });

  const renderThreads = (list: any[]) =>
    list.map((t: any) => (
      <div key={t.id} className="thread-row">
        <div className="thread" onClick={() => loadMessages(t.id)}>
          {t.title}
        </div>

        <div className="thread-actions">
          <span onClick={() => renameThread(t.id)}>✏️</span>
          <span onClick={() => deleteThread(t.id)}>❌</span>
        </div>
      </div>
    ));

  return (
    <div className="chat-container">

      {/* SIDEBAR */}
      <div className="sidebar">
        <button className="new-chat-btn" onClick={createThread}>
          + New Chat
        </button>

        <h4>Today</h4>
        {todayChats.length === 0 ? <p>No chats</p> : renderThreads(todayChats)}

        <h4>Yesterday</h4>
        {yesterdayChats.length === 0 ? <p>No chats</p> : renderThreads(yesterdayChats)}

        <h4>Older</h4>
        {olderChats.length === 0 ? <p>No chats</p> : renderThreads(olderChats)}

        <button
          className="logout-btn"
          onClick={() => {
            localStorage.clear();
            window.location.href = "/login";
          }}
        >
          Logout
        </button>
      </div>

      {/* MAIN */}
      <div className="chat-area">
        {/* HEADER */}
      <div className="chat-header">
        <div className="logo">🤖 JuzServ AI</div>
        <div className="user-email">{email}</div>
      </div>

      {/* ✅ UPLOAD BAR (DON’T REMOVE THIS) */}
<div className="upload-bar">
    <input type="file" id="fileInput" />
    <button
      onClick={async () => {
        const fileInput: any = document.getElementById("fileInput");
        const file = fileInput.files[0];

        if (!file) return alert("Select file ❌");

        const formData = new FormData();
        formData.append("file", file);

        await API.post("/upload/", formData);
        alert("Uploaded ✅");
      }}
    >
      Upload PDF
    </button>
  </div>
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={m.role === "user" ? "msg-right" : "msg-left"}>
              {m.message}
            </div>
          ))}

          {loading && (
            <div className="loading-container">
              <div className="loading-bar"></div>
            </div>
          )}
        </div>

        <div className="input-area">
          <span className="mic-icon">🎤</span>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask from PDF..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>

      </div>
    </div>
  );
}