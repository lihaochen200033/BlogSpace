import "./App.css";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from "./pages/Home";
import CreatePost from "./pages/AddPost/CreatePost";
import Post from "./pages/ViewPost/Post";
import CreateEditor from "./pages/AddPost/CreateEditor";
import Login from "./pages/Users/Login";
import Register from "./pages/Users/Register";
import { useState, useEffect } from "react";
import PageNotFound from "./pages/PageNotFound";
import Profile from "./pages/Users/Profile";
import LikedPosts from "./pages/ViewPost/LikedPosts";
import Details from "./pages/Users/Details";
import MarkdownEditor from "./pages/AddPost/CreateMarkdown";
import EditPost from "./pages/EditPost/EditPost";
import ChangePassword from "./pages/Users/ChangePassword";
import { AUTH_TOKEN } from './constants';
import { useNavigate } from 'react-router-dom';

function App() {
  const [LoggedIn, setLoggedIn] = useState(false);
  const navigate = useNavigate();

  const handle_logout = () => {
    localStorage.removeItem(AUTH_TOKEN);
    setLoggedIn(false);
    navigate('/login');
  };
  
  return (
    <div className="App">
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/home" element={<Home />} />
            <Route path="/createpost" element={<CreatePost />} />
            <Route path="/post/:id" element={<Post />} />
            <Route path="/createposteditor" element={<CreateEditor />} />
            <Route path="/markdown" element={<MarkdownEditor />} />
            <Route path="/edit/:id" element={<EditPost />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/details" element={<Details />} />
            <Route path="/profile/:id" element={<Profile />} />
            <Route path="/changepwd" element={<ChangePassword />} />
            <Route path="/liked" element={<LikedPosts />} />
            <Route path="*" element={<PageNotFound />} />
          </Routes>
    </div>
  )
}

export default App;
