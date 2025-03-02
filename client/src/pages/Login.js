import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import '../css/login.css';


export default function Login() {
  const [username, setUsername] = useState('');
  const [userMail, setUserMail] = useState('');
  const navigate = useNavigate();

  const loginClicked = async () => {    
    try {
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fullName: username, email: userMail }),
        });

        if (response.ok) {
            alert(`Hi ${username}!`);
            navigate("/Text");
        } else {
            alert("we could not find this user in our system.");
        }
    } catch (error) {
        console.error("An error has occured:", error);
        alert("An error has occured.");
    }
};
  return (
    <div>
      <h1 className='h1'>Login</h1>
      <label >user name: </label>
      <input
          type="text"
          value={username}
          onChange={(e)=>setUsername(e.target.value)}
          className="textField"
          required
      />
      <br />
      <label htmlFor="email">email: </label>
      <input
          type="email"
          id="email"
          name="email"
          value={userMail}
          onChange={(e)=>setUserMail(e.target.value)}
          className="textField"
          required
      />   
       <br />
      <button className="button" onClick={()=> loginClicked()}>Login</button>
       </div>
  );
}
