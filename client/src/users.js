import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function UsersPage() {
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    // טעינת רשימת המשתמשים מהשרת
    useEffect(() => {
        const fetchUsers = async () => {
            const response = await fetch("http://127.0.0.1:5000/get_users");
            const data = await response.json();
            setUsers(data.users);
        };

        fetchUsers();
    }, []);

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            <h1>📋 רשימת המשתמשים</h1>

            {users.length > 0 ? (
                <table border="1" style={{ margin: "20px auto", width: "50%" }}>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>שם משתמש</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map((user, index) => (
                            <tr key={index}>
                                <td>{index + 1}</td>
                                <td>{user}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>אין משתמשים עדיין.</p>
            )}

            <button onClick={() => navigate("/")} style={{ marginTop: "20px" }}>
                🔙 חזור לדף הבית
            </button>
        </div>
    );
}

export default UsersPage;
