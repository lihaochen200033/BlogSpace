import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import Navbar from "../components/Navbar";
import { useQuery } from '@apollo/client';
import { AUTH_TOKEN } from '../constants';
import { GET_ALL_POST } from "../Helpers/graphql"

function Home() {
    const token = localStorage.getItem(AUTH_TOKEN);
    useEffect(() => {
        if (!token) {
            alert("User not logged In!");
            navigate("/login");
        }
    }, [])
    const [listOfPosts, setListOfPosts] = useState([]);
    const navigate = useNavigate();

    const { data: postData } = useQuery(GET_ALL_POST, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache"
    })

    useEffect(()=>{
        if (postData?.allPosts) {
            setListOfPosts(postData.allPosts)
        }
    }, [postData])

    return (
        <div className="PostsPage">
            <Navbar />
            <h1 className="Title">The Author's Thoughts</h1>
            <div className="Posts">
                {listOfPosts.map((post, key) => {
                    return (
                        <div className="post" key={post.id}>
                            <div className="title">{post.title}</div>
                            <div className="footer">By @{post.author.username}</div>
                            <div className="body">{post.content}</div>
                            <div className="icons">
                                <button onClick={() => navigate(`/post/${post.id}`)}>View Post</button>
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default Home;