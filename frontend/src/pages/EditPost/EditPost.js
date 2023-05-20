import { useEffect, useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { useNavigate, useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import { useMutation, useQuery } from '@apollo/client';
import { AUTH_TOKEN } from '../../constants';
import { GET_POST_QUERY, UPDATE_POST_MUTATION } from "../../Helpers/graphql"

function EditPost() {
    const token = localStorage.getItem(AUTH_TOKEN);
    useEffect(() => {
        if (!token) {
            alert("User not logged In!");
            navigate("/login");
        }
    }, [])
    const { id } = useParams();
    const [PostObject, setPostObject] = useState({});
    const navigate = useNavigate();

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
        if (postData?.postById) {
            setPostObject(postData.postById)
        }
    }, [postData])

    const initialValues = {
        title: PostObject.title,
        content: PostObject.content,
    };

    const [ updatePost ] = useMutation(UPDATE_POST_MUTATION, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache",
    });

    const onSubmit = (data) => {
        updatePost({ 
            variables: {
                id: id,
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
            <h1 className='title'>Update your Post</h1>
            <Formik initialValues={initialValues} enableReinitialize={true} onSubmit={onSubmit}>
                <Form className='formContainer'>
                    <label>Title : </label>
                    <Field id="inputUpdatePostTitle" name="title" placeholder="Books" />
                    <ErrorMessage name="title" component="div" />

                    <label>Post : </label>
                    <Field id="inputUpdatePostContent" name="content" placeholder="Enter post content" />
                    <ErrorMessage name="content" component="div" />

                    <button type='submit' className='updatePost'>Update Post</button>
                </Form>
            </Formik>
        </div>
    )
}

export default EditPost;