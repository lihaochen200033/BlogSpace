import { Formik, Form, Field, ErrorMessage } from 'formik';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import Navbar from '../../components/Navbar';
import { useMutation, useQuery } from '@apollo/client';
import { AUTH_TOKEN } from '../../constants';
import { GET_USER, CREATE_POST_MUTATION } from "../../Helpers/graphql"

function CreatePost() {
    const token = localStorage.getItem(AUTH_TOKEN);
    useEffect(() => {
        if (!token) {
            alert("User not logged In!");
            navigate("/login");
        }
    }, [])
    const navigate = useNavigate();

    const initialValues = {
        title: "",
        content: "",
    };

    const { data: userData } = useQuery(GET_USER, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache"
    })

    const userId = userData?.userDetails?.id;

    const [ createPost ] = useMutation(CREATE_POST_MUTATION, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    });

    const onSubmit = (data) => {
        createPost({ 
            variables: {
                author: userId,
                content: data.content,
                title: data.title,
            },
            onCompleted: (data) => {
                navigate("/home");
            },
        })
    }

    return (
        <div className='createPostPage'>
            <Navbar />
            <h1 className='title'>Post your thoughts!</h1>

            <Formik initialValues={initialValues} onSubmit={onSubmit}>
                <Form className='formContainer'>
                <label>Title : </label>
                    <Field id="inputUpdatePostTitle" name="title" placeholder="Enter post title" />
                    <ErrorMessage name="title" component="div" />

                    <label>Post : </label>
                    <Field id="inputUpdatePostContent" name="content" placeholder="Enter post content" />
                    <ErrorMessage name="content" component="div" />

                    <button type='submit' className='createPost'>Create Post</button>
                </Form>
            </Formik>
        </div>
    )
}

export default CreatePost;