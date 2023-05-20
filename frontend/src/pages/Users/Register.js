import { Formik, Form, Field, ErrorMessage } from 'formik';
import RegisterImg from "../../Images/Register.webp";
import { Link, useNavigate } from 'react-router-dom';
import React from 'react'
import { useMutation } from '@apollo/client';
import { AUTH_TOKEN } from '../../constants';
import Navbar from "../../components/Navbar";
import { SIGNUP_MUTATION } from "../../Helpers/graphql"

function Register() {
    const navigate = useNavigate();
    const initialValues = {
        username: "",
        password: "",
        email: ""
    };
    
    const [signup] = useMutation(SIGNUP_MUTATION, {
        onCompleted: (data) => {
            if (data.register.success) {
                localStorage.setItem(AUTH_TOKEN, data.register.token);
                navigate('/');
            } else {
                alert("Register Failed! One of more fields entered are invalid!");
            }
        },
    });

    const onSubmit = (data) => {
        signup({ 
            variables: {
                username: data.username,
                email: data.email,
                password: data.password,
            }
        })
    }

    return (
        <div>
            <Navbar />
            <div className='Register'>
                <div className='RegImg'>
                    <img src={RegisterImg} alt="Registration"/>
                </div>

                <div className='RegContent'>
                    <h1>Registration Form</h1>
                    <Formik initialValues={initialValues} onSubmit={onSubmit}>
                        <Form className='RegContainer'>
                            <label>Username : </label>
                            <Field id="inputUsername" name="username" placeholder="User name" type="text" />
                            <ErrorMessage name="username" component="div" />

                            <label>Email : </label>
                            <Field id="inputEmail" name="email" placeholder="Enter email" type="email" />
                            <ErrorMessage name="email" component="div" />

                            <label>Password : </label>
                            <Field id="inputPassword" name="password" placeholder="Enter password" type="password" />
                            <ErrorMessage name="password" component="div" />

                            <button type='submit' className='createUser'>Create User</button>
                            <div>Already have an account ? <Link to="/login">Login here</Link></div>
                        </Form>
                    </Formik>
                </div>
            </div>
        </div>
    )
}

export default Register;