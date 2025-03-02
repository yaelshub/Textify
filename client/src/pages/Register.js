import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import '../css/Register.css';

export default function Register() {
    const [formData, setFormData] = useState({ fullName: "", email: "" });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleClick = () => 
    {
        navigate("/Text"); // ניווט לדף "Text"
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });
    
            if (response.ok) {
                alert("Registration successful!");
                setFormData({ fullName: "", email: "" });
                navigate("/Text");
            } else {
                alert("There was a problem registering.");
            }
        } catch (error) {
            console.error("Error sending request:", error);
            alert("Error connecting to server.");
        }
    };

    return (
        <div>
            <h1>Welcome</h1>
            <h2>sign up to get started:</h2>
            <form onSubmit={handleSubmit}>
                <label htmlFor="fullName">fullName</label>
                <input
                    type="text"
                    id="fullName"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleChange}
                    required
                />
                <br />
                <label htmlFor="email">email</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
                <br />
                <button type="submit">submit</button>
            </form>
            <p>Already have an account? <Link to="/login">Login here</Link></p>
        </div>
    );
}
