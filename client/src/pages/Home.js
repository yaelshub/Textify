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
            <h2>הוספת משתמש</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="שם משתמש"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <button type="submit">הוסף</button>
            </form>
            <button onClick={() => navigate("/users")}>צפה בכל המשתמשים</button>
            <h1>ברוך הבא!</h1>
            <div className="container">
                <button>
                    <Link to="/Login">כניסה</Link>
                </button>
                <button>
                    <Link to="/Register">הרשמה</Link>
                </button>
            </div>
        </div>
    );
}

export default HomePage;
