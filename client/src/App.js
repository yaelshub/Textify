import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login"; 
import Register from "./pages/Register"; 
import Text from "./pages/Text";
import UsersPage from "./users";



function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/users" element={<UsersPage />} />
                <Route path="/Login" element={<Login />} />
                <Route path="/Register" element={<Register />} />
                <Route path="/Text" element={<Text />} />
            </Routes>
        </Router>
    );
}

export default App;
