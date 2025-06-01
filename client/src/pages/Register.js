import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import '../css/Register.css';

export default function Register() {
    const [formData, setFormData] = useState({ fullName: "", email: "" });
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage("");

        try {
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                setMessage("Registration successful!");
                setFormData({ fullName: "", email: "" });

                setTimeout(() => {
                    navigate("/Text");
                }, 1500);
            } else {
                setMessage("There was a problem registering.");
            }
        } catch (error) {
            console.error("Error sending request:", error);
            setMessage("Error connecting to server.");
        }
    };

    return (
        <div className="container">
            <h1>Welcome</h1>
            <h2>Sign up to get started:</h2>

            <form onSubmit={handleSubmit}>
                <label htmlFor="fullName">Full Name</label>
                <input
                    type="text"
                    id="fullName"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />

                <button type="submit">Submit</button>
            </form>

            {message && <p className="register-message">{message}</p>}

            <p>Already have an account? <Link to="/login">Login here</Link></p>
        </div>
    );
}
