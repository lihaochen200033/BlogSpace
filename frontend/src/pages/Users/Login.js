import LoginImg from "../../Images/Login.jpg";
import { Link, useNavigate } from "react-router-dom";
import React, { Component, useState } from 'react'
import { useMutation, gql } from '@apollo/client';
import { AUTH_TOKEN } from '../../constants';
import Navbar from "../../components/Navbar";

const LOGIN_MUTATION = gql`
  mutation LoginMutation(
    $email: String!
    $password: String!
  ) {
    tokenAuth(email: $email, password: $password) {
        success
        token
        refreshToken
    }
  }
`;

function Login() {
    const navigate = useNavigate();
    const [formState, setFormState] = useState({
        email: '',
        password: '',
    });


    const [login, {data, error, loading}] = useMutation(LOGIN_MUTATION, {
        variables: {
          email: formState.email,
          password: formState.password
        },
        onCompleted: (data) => {
            if (data.tokenAuth.success) {
                localStorage.setItem(AUTH_TOKEN, data.tokenAuth.token);
                navigate('/home');
            } else {
                alert("Login Failed! Invalid credential!");
            }
        }
    });

    const handleLogin = (e) => {
        e.preventDefault();
        login();
    }

    return (
        <div>
            <Navbar />
            <div className="Login">
                <div className='LogImg'>
                    <img src={LoginImg} alt="Login"/>
                </div>
                <div className="LoginContent">
                    <h1>Login Page</h1>
                    <form className="LoginContainer">
                        <label>Email : </label>
                        <input 
                            type="email" 
                            placeholder="Enter Email" 
                            onChange={(e) =>
                                setFormState({
                                    ...formState,
                                    email: e.target.value
                                })
                        }
                        autoComplete="on" />

                        <label>Password : </label>
                        <input
                        type="password"
                        placeholder="Enter password"
                        onChange={(e) =>
                            setFormState({
                                ...formState,
                                password: e.target.value
                            })
                        }
                        autoComplete="on" />

                        <button type='submit' className='loginUser' onClick={handleLogin}>Login</button>
                        <div>New User ? <Link to="/register">Register here!</Link></div>
                    </form>
                </div>
            </div>
        </div>
        
    )
}

export default Login;