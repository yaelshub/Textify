import { useNavigate } from "react-router-dom";
import '../css/home.css';

function HomePage() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    const storedName = localStorage.getItem("username");
    if (!storedName) return;

    await fetch("http://127.0.0.1:5000/logout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: storedName }),
    });

    localStorage.removeItem("username");
    navigate("/Login");
  };

  return (
    <div className="container">
      <h1>Welcome</h1>

      <button onClick={() => navigate("/Login")}>Login</button>
      <button onClick={() => navigate("/Register")}>Register</button>

      <button className="logout-button" onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default HomePage;