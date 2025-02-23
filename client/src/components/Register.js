const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = { fullName, password, phone, email };

    try {
        const response = await fetch("http://localhost:5000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            alert("ההרשמה בוצעה בהצלחה!");
            setFullName("");
            setPassword("");
            setPhone("");
            setEmail("");
        } else {
            alert("הייתה בעיה בהרשמה.");
        }
    } catch (error) {
        console.error("שגיאה בשליחת הבקשה:", error);
        alert("שגיאה בחיבור לשרת.");
    }
};
