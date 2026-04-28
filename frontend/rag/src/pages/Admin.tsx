import { useNavigate } from "react-router-dom";

export default function Admin() {

  const navigate = useNavigate();

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Admin Panel</h2>

      <button onClick={() => navigate("/chat")}>
        Go to Chat
      </button>

      <br /><br />

      <button
        onClick={() => {
          localStorage.removeItem("token");
          navigate("/login");
        }}
      >
        Logout
      </button>
    </div>
  );
}