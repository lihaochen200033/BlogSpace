import React, { Component, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery, gql } from '@apollo/client';
import { AUTH_TOKEN } from '../constants';
import Card from 'react-bootstrap/Card';

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

const Homepage = (params) => {
    const token = localStorage.getItem(AUTH_TOKEN);
    console.log(token);

    const [refresh, setRefresh] = useState(false);
    const [posts, setPosts] = useState([]);
    console.log(posts);

    const { data: userdata } = useQuery(GET_USER, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache"
    })

    console.log(userdata);
    const userId = userdata?.userDetails?.id;
    const username = userdata?.userDetails?.username;

    const { data: postdata } = useQuery(GET_ALL_POST, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
    })

    useEffect(()=>{
        if (postdata?.allPosts) {
            setPosts(postdata?.allPosts)
        }
    }, [postdata])
    
    console.log(posts);

    const [showAddModal, setShowAddModal] = useState(false);
    
    console.log(posts);
    return (
        <div>
            <h2>Welcome, { username } !</h2>
            <button className="btn btn-primary" style={{marginBottom: '8px'}}>test</button>
            <div className="post_container">
                {posts.map((post, index) =>
                    <Card style={{marginBottom: "4px"}}>
                        <Card.Body>
                            <Card.Title>{ post.title }</Card.Title>
                            <Card.Subtitle className="mb-2 text-muted">{ post.author.username }</Card.Subtitle>
                            <Card.Text>
                            { post.content }
                            </Card.Text>
                            <Card.Link href="#">Card Link</Card.Link>
                            <Card.Link href="#">Another Link</Card.Link>
                        </Card.Body>
                    </Card>
                )}
            </div>
        </div>
        
    )
}

export default Homepage;
