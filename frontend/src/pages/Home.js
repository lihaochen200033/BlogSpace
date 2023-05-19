import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from 'react-router-dom';
import Navbar from "../components/Navbar";
import { useMutation, useQuery, gql } from '@apollo/client';
import { AUTH_TOKEN } from '../constants';

const GET_USER = gql`
    query {
        userDetails {
            id
            username
        }
    }
`;

const GET_ALL_POST = gql`
    query {
        allPosts {
            id
            title
            content
            author {
                id
                username
            }
            createdOn
            updatedOn
        }
    }
`;

function Home() {
    const token = localStorage.getItem(AUTH_TOKEN);
    console.log(token);
    useEffect(() => {
        if (!token) {
            alert("User not logged In!");
            navigate("/login");
        }
    }, [])
    const [listOfPosts, setListOfPosts] = useState([]);
    const navigate = useNavigate();

    const { data: userData } = useQuery(GET_USER, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache"
    })

    console.log(userData);
    const userId = userData?.userDetails?.id;
    const username = userData?.userDetails?.username;
    console.log(userId);

    const { data: postData } = useQuery(GET_ALL_POST, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache"
    })

    console.log(postData);

    useEffect(()=>{
        if (postData?.allPosts) {
            setListOfPosts(postData.allPosts)
        }
    }, [postData])

    console.log(listOfPosts);

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