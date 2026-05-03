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
    try {
      const res = await API.get("/threads/");
      setThreads(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const createThread = async () => {
    try {
      const res = await API.post("/threads/", { 
        title: "New Chat" 
      });
      const id = res.data.thread_id || res.data.id;

      setCurrentThread(id);
      setMessages([]);
      loadThreads();
    } catch (err) {
      console.error("THREAD ERROR");
    }
  };

  const loadMessages = async (id: number) => {
    try {
      const res = await API.get(`/messages/${id}`);
      setMessages(res.data);
      setCurrentThread(id);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteThread = async (id: number) => {
    try {
      await API.delete(`/threads/${id}`);
      loadThreads();

      if (id === currentThread) {
        setMessages([]);
        setCurrentThread(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const renameThread = async (id: number) => {
    const newTitle = prompt("Enter new title");
    if (!newTitle) return;

    try {
      await API.put(`/threads/${id}`, { title: newTitle });
      loadThreads();
    } catch (err) {
      console.error(err);
    }
  };

  // ✅ FINAL FIXED FUNCTION
  const sendMessage = async () => {
    if (!input.trim() || !currentThread) return;

    const question = input;

    // show user msg instantly
    setMessages(prev => [...prev, { role: "user", content: question }]);
    setInput("");
    setLoading(true);

    try {
      const res = await API.post("/messages/", {
        thread_id: currentThread,
        question: question,
        message: question // ✅ correct key
      });

      // show bot reply
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: res.data.answer || res.data.reply || "No response"
        }
      ]);

      // auto rename
      const thread = threads.find(
        t => (t.thread_id || t.id) === currentThread
      );

      if (thread && thread.title === "New Chat") {
        await API.put(`/threads/${currentThread}`, {
          title: question.slice(0, 40)
        });
      }

      loadThreads();
    } catch (err: any) {
      console.log("ERROR 👉", err.response?.data);
      alert("Message failed ❌");
    }

    setLoading(false);
  };

  // DATE FILTER
  const today = new Date();
  const yesterday = new Date();
  yesterday.setDate(today.getDate() - 1);

  const isSameDay = (d1: Date, d2: Date) =>
    d1.toDateString() === d2.toDateString();

  const parseDate = (dateStr: string) => new Date(dateStr);

  const todayChats = threads.filter(t =>
    isSameDay(parseDate(t.created_at), today)
  );

  const yesterdayChats = threads.filter(t =>
    isSameDay(parseDate(t.created_at), yesterday)
  );

  const olderChats = threads.filter(t => {
    const d = parseDate(t.created_at);
    return !isSameDay(d, today) && !isSameDay(d, yesterday);
  });

  const renderThreads = (list: any[]) =>
    list.map(t => {
      const id = t.thread_id || t.id;

      return (
        <div key={id} className="thread-row">
          <div className="thread" onClick={() => loadMessages(id)}>
            {t.title}
          </div>

          <div className="thread-actions">
            <span onClick={() => renameThread(id)}>✏️</span>
            <span onClick={() => deleteThread(id)}>❌</span>
          </div>
        </div>
      );
    });

  return (
    <div className="chat-container">
      {/* SIDEBAR */}
      <div className="sidebar">
        <button onClick={createThread}>+ New Chat</button>

        <h4>Today</h4>
        {todayChats.length ? renderThreads(todayChats) : <p>No chats</p>}

        <h4>Yesterday</h4>
        {yesterdayChats.length ? renderThreads(yesterdayChats) : <p>No chats</p>}

        <h4>Older</h4>
        {olderChats.length ? renderThreads(olderChats) : <p>No chats</p>}
      </div>

      {/* MAIN */}
      <div className="chat-area">
        <div className="chat-header">
          <div>🤖 JuzServ AI</div>
          <div>{email}</div>
        </div>

        <div className="messages">
          {messages.map((m, i) => (
            <div
              key={i}
              className={m.role === "user" ? "msg-right" : "msg-left"}
            >
              {m.content}
            </div>
          ))}
          {loading && <p>Loading...</p>}
        </div>

        <div className="input-area">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask something..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}