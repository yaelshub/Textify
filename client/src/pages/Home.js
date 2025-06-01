import { useNavigate } from "react-router-dom";
import '../css/home.css';

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <h1>Welcome</h1>
      <button onClick={() => navigate("/Login")}>Login</button>
      <button onClick={() => navigate("/Register")}>Register</button>
    </div>
  );
}

export default HomePage;
