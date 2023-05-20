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

const CREATE_COMMENT_MUTATION = gql`
  mutation CreateCommentMutation(
    $author: ID!
    $content: String!
    $post: ID!
  ) {
    createComment(
        author: $author
        content: $content
        post: $post
    ) {
        comment {
            id
            content
            author {
              id
              username
            }
        }
    }
  }
`;

const DELETE_COMMENT_MUTATION = gql`
  mutation DeleteCommentMutation(
    $id: ID!
  ) {
    deleteComment(id: $id) {
        comment {
            id
            content
        }
    }
  }
`;

const DELETE_POST_MUTATION = gql`
  mutation DeletePostMutation(
    $id: ID!
  ) {
    deletePost(id: $id) {
        post{
            id
        }
    }
  }
`;

function Post() {
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

    const [ createComment ] = useMutation(CREATE_COMMENT_MUTATION, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    })

    const handleCreateComment = (e) => {
        e.preventDefault();
        createComment({ 
            variables: {
                author: userId,
                content: newComment,
                post: id
            },
            onCompleted: (data) => {
                console.log("here")
                console.log(data);
                console.log("here")
                const newComment = {
                    content: data.createComment.comment.content,
                    author: {
                        id: data.createComment.comment.author.id,
                        username: data.createComment.comment.author.username
                    },
                    id: data.createComment.comment.id
                };
                setCommentObject([newComment, ...commentObject]);
                setNewComment("");
            }
        })
    }

    const [ deleteComment ] = useMutation(DELETE_COMMENT_MUTATION, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    })

    const handleDeleteComment = (id) => {
        deleteComment({ 
            variables: {
                id: id
            },
            onCompleted: (data) => {
                setCommentObject(commentObject.filter((val) => {
                    return val.id !== data.deleteComment.comment.id;
                }))
            }
        })
    }

    const [ deletePost ] = useMutation(DELETE_POST_MUTATION, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    })
    const handleDeletePost = (id) => {
        deletePost({ 
            variables: {
                id: id
            },
            onCompleted: (data) => {
                navigate("/home");
            }
        })
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
                    {userId === postObject.author?.id &&
                    <button onClick={() => handleDeletePost(postObject.id)}>
                        <IconContext.Provider value={{ color: "white", className: "contactIcon"}}>
                            <BsFillTrashFill/>
                        </IconContext.Provider>
                        Delete Post
                    </button>}
                    
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
                        <button onClick={handleCreateComment}>Submit</button>
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
                                    <BsFillTrashFill onClick={() => handleDeleteComment(comment.id)} />
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

export default Post;

// id -> exact parameter name used during routing 