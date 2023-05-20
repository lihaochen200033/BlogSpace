import "./App.css";
import { Route, Routes } from 'react-router-dom';
import Home from "./pages/Home";
import CreatePost from "./pages/AddPost/CreatePost";
import Post from "./pages/ViewPost/Post";
import Login from "./pages/Users/Login";
import Register from "./pages/Users/Register";
import PageNotFound from "./pages/PageNotFound";
import EditPost from "./pages/EditPost/EditPost";

function App() {
  return (
    <div className="App">
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/home" element={<Home />} />
            <Route path="/createpost" element={<CreatePost />} />
            <Route path="/post/:id" element={<Post />} />
            <Route path="/edit/:id" element={<EditPost />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<PageNotFound />} />
          </Routes>
    </div>
  )
}

export default App;
