import { useEffect, useState } from "react";
import API from "../api/axios";

export default function Sidebar({ setThreadId }: any) {
  const [threads, setThreads] = useState<any[]>([]);

  useEffect(() => {
    loadThreads();
  }, []);

  const loadThreads = async () => {
    const res = await API.get("/threads/1");
    setThreads(res.data);
  };

  return (
    <div className="sidebar">
      <h3>Chats</h3>
      {threads.map((t) => (
        <div key={t.id} onClick={() => setThreadId(t.id)}>
          {t.title}
        </div>
      ))}
    </div>
  );
}