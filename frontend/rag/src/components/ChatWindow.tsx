import { useEffect, useState } from "react";
import API from "../api/axios";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({ threadId }: any) {
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    if (threadId) loadMessages();
  }, [threadId]);

  const loadMessages = async () => {
    const res = await API.get(`/messages/${threadId}`);
    setMessages(res.data);
  };

  return (
    <div className="messages">
      {messages.map((m, i) => (
        <MessageBubble key={i} msg={{ text: m.message, role: m.role }} />
      ))}
    </div>
  );
}