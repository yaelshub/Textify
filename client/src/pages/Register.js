import React, { useState } from 'react';
import { Link } from "react-router-dom"; 

export default function Register() {
    const [fullName, setFullName] = useState(""); 
    const [password, setPassword] = useState(""); 
    const [phone, setPhone] = useState(""); 
    const [email, setEmail] = useState(""); 

    const handleSubmit = (e) => {
        e.preventDefault(); // למנוע רענון הדף
        // כאן תוסיפי לוגיקה לשליחת הנתונים לשרת
        console.log({ fullName, password, phone, email });
        alert("ההרשמה בוצעה בהצלחה!"); 
    };

    return (
        <div>
            <h1>ברוכים הבאים</h1>
            <h2>:הרשמו כדי להתחיל</h2>
            <form onSubmit={handleSubmit}>
                <label>:שם מלא</label>
                <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)} 
                />
                <br />
                <label>:סיסמא</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <br />
                <label>:טלפון</label>
                <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)} 
                />
                <br />
                <label>:מייל</label>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)} 
                />
                <br />
                <button type="submit"><Link to="/Text">הירשם</Link>
                </button>
            </form>
        </div>
    );
}