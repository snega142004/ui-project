import { useState } from "react";
import API from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const signup = async () => {
    try {
      await API.post("/auth/signup", { name, email, password });
      alert("Signup success ✅");
      navigate("/login");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Signup failed ❌");
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Create Account</h2>

        <input placeholder="Name" value={name} onChange={(e)=>setName(e.target.value)} />
        <input placeholder="Email" value={email} onChange={(e)=>setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e)=>setPassword(e.target.value)} />

        <button onClick={signup}>Signup</button>

        {error && <p className="error">{error}</p>}

        <p onClick={()=>navigate("/login")}>Already have account?</p>
      </div>
    </div>
  );
}