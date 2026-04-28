export default function MessageBubble({ msg }: any) {
  return (
    <div style={{
      background: msg.role === "user" ? "#0b93f6" : "#444654",
      padding: "10px",
      margin: "10px",
      borderRadius: "10px"
    }}>
      {msg.text}
    </div>
  );
}