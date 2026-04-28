import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard">
      <div className="dashboard-card">
        <h1>JuzServ AI</h1>
        <p>Upload PDFs & ask intelligent questions</p>

        <button onClick={()=>navigate("/chat")} className="go-chat-btn">
          Go to Chat →
        </button>
      </div>
    </div>
  );
}