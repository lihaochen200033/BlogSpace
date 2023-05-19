import { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import { useMutation, useQuery, gql } from '@apollo/client';
import { AUTH_TOKEN } from '../../constants';
import { BsFillTrashFill } from 'react-icons/bs';
import { IconContext } from "react-icons";

const GET_COMMENTS_QUERY = gql`
  query GET_COMMENTS_QUERY(
    $postId: ID!
  ) {
    commentByPostId(
        postId: $postId
    ) {
        id
        content
        author {
            id
            username
        }
    }
  }
`;

const GET_POST_QUERY = gql`
  query GET_POST_QUERY(
    $postId: ID!
  ) {
    postById(
        postId: $postId
    ) {
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
    const { id } = useParams();
    const [postObject, setPostObject] = useState({});
    const [commentObject, setCommentObject] = useState([]);
    const [newComment, setNewComment] = useState("");
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

    const { data: postsData } = useQuery(GET_ALL_POST, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache"
    })

    console.log(postsData);

    const { data: commentsData } = useQuery(GET_COMMENTS_QUERY, {
        variables: {
            postId: id
        },
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    })

    console.log(commentsData);

    const { data: postData } = useQuery(GET_POST_QUERY, {
        variables: {
            postId: id
        },
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    })

    console.log(postData);

    useEffect(()=>{
        if (commentsData?.commentByPostId) {
            setCommentObject(commentsData.commentByPostId)
        }
        if (postData?.postById) {
            setPostObject(postData.postById)
        }
    }, [commentsData, postData])

    console.log(commentObject);
    console.log(postObject);

    const AddComment = (e) => {
        e.preventDefault();
    }

    const deleteComment = (id) => {
    }

    const deletePost = (id) => {
    }

    const EditPost = (Id) => {
        navigate(`/edit/${Id}`);
    }

    console.log(userId);
    console.log(commentObject);

    return (
        <div className='PostPage'>
            <Navbar />
            <div className='postContent'>
                <div className='icons'>
                    {userId === postObject.author?.id && <button onClick={() => deletePost(postObject.id)}><i className='bi bi-trash-fill'></i>Delete Post</button>}
                    {userId === postObject.author?.id && <button onClick={() => EditPost(postObject.id)} className='Edit'><i class="bi bi-pencil-square"></i>Update Post</button>}
                </div>
                <h3 className='PostTitle'>{postObject.title}</h3>
                <div className='PostAuthor'>By @{postObject.author?.username}</div>
                <hr />
                <div className='PostBody'>{postObject.content}</div>
                <hr />
            </div>
            <div className='Comments'>
                <h1>Comments</h1>
                <div className='AddComment'>
                    <form>
                        <textarea placeholder='Leave a constructive comment ...' value={newComment} autoCorrect='on' onChange={(e) => setNewComment(e.target.value)} />
                        <button onClick={AddComment}>Submit</button>
                    </form>
                </div>
                <div className='ShowComment'>
                    {commentObject.map((comment, key) => {
                        return (
                            <div className='Comment'>
                                <div className='Commentuser'>{comment.author?.username}</div>
                                <div className='Commentbody'>{comment.content}</div>
                                {userId === comment.author?.id && 
                                <IconContext.Provider value={{ color: "white", className: "contactIcon" }}>
                                    <BsFillTrashFill onClick={() => deleteComment(comment.id)} />
                                </IconContext.Provider>
                            }
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}

function Post() {
    const token = localStorage.getItem(AUTH_TOKEN);
    console.log(token);
    useEffect(() => {
        if (!token) {
            alert("User not logged In!");
            navigate("/login");
        }
    }, [])
    
    let { id } = useParams();
    const [postObject, setPostObject] = useState({});
    const [commentObject, setCommentObject] = useState([]);
    const [newComment, setNewComment] = useState("");
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

    const { data: commentsData } = useQuery(GET_COMMENTS_QUERY, {
        variables: {
            postId: id
        },
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    })

    const { data: postData } = useQuery(GET_POST_QUERY, {
        variables: {
            postId: id
        },
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    })

    useEffect(()=>{
        if (commentsData?.commentByPostId) {
            setCommentObject(commentsData.commentByPostId)
        }
        if (postData?.postById) {
            setPostObject(postData.postById)
        }
    }, [commentsData, postData])

    const AddComment = (e) => {
        e.preventDefault();
    }

    const deleteComment = (id) => {
    }

    const deletePost = (id) => {
    }

    const EditPost = (Id) => {
        navigate(`/edit/${Id}`);
    }

    console.log(commentObject);

    return (
        <div className='PostPage'>
            <Navbar />
            <div className='postContent'>
                <div className='icons'>
                    {userId === postObject.author.id && <button onClick={() => deletePost(postObject.id)}><i className='bi bi-trash-fill'></i>Delete Post</button>}
                    {userId === postObject.author.id && <button onClick={() => EditPost(postObject.id)} className='Edit'><i class="bi bi-pencil-square"></i>Update Post</button>}
                </div>
                <h3 className='PostTitle'>{postObject.title}</h3>
                <div className='PostAuthor'>By @{postObject.author.username}</div>
                <hr />
                <div className='PostBody'>{postObject.content}</div>
                <hr />
            </div>
            <div className='Comments'>
                <h1>Comments</h1>
                <div className='AddComment'>
                    <form>
                        <textarea placeholder='Leave a constructive comment ...' value={newComment} autoCorrect='on' onChange={(e) => setNewComment(e.target.value)} />
                        <button onClick={AddComment}>Submit</button>
                    </form>
                </div>
                <div className='ShowComment'>
                    {commentObject.map((comment, key) => {
                        return (
                            <div className='Comment'>
                                <div className='Commentuser'>{comment.id}</div>
                                <div className='Commentbody'>{comment.content}</div>
                                {username === comment.username && <i class="bi bi-trash-fill" onClick={() => deleteComment(comment.id)}></i>}
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}

export default Home;

// id -> exact parameter name used during routing 