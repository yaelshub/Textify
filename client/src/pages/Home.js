import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import '.././css/home.css';

function HomePage() {
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch("http://127.0.0.1:5000/add_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    setName("");
  };

  return (
    <div>
      
      <div className="container">
      <h1>welcome</h1>
        <Link to="/Login">
          <button>Login</button>
        </Link>
        <Link to="/Register">
          <button>Register</button>
        </Link>
      </div>


    </div>
  );
}

export default HomePage;
