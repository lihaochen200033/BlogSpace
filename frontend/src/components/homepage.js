import React, { Component, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { useMutation, gql } from '@apollo/client';
import { AUTH_TOKEN } from '../constants';

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

const Homepage = (params) => {
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
            console.log(data);
            localStorage.setItem(AUTH_TOKEN, data.tokenAuth.token);
            navigate('/');
            console.log(localStorage.getItem(AUTH_TOKEN));
        }
    });

    return (
        <h3>Homepage</h3>
    )
}

export default Homepage;
