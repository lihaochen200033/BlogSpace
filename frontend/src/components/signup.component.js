import React, { Component, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { useMutation, gql } from '@apollo/client';
import { AUTH_TOKEN } from '../constants';

const SIGNUP_MUTATION = gql`
  mutation SIGNUP_MUTATION(
    $email: String!
    $username: String!
    $password: String!
  ) {
    register(
        email: $email
        username: $username
        password1: $password
        password2: $password
    ) {
        success
        token
        refreshToken
    }
  }
`;

const SignUp = () => {
    const navigate = useNavigate();
    const [formState, setFormState] = useState({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
    });
    const [infoInvalid, setInfoInvalid] = useState(false);

    const [signup, {data, error, loading}] = useMutation(SIGNUP_MUTATION, {
        variables: {
          username: formState.first_name + formState.last_name,
          email: formState.email,
          password: formState.password,
        },
        onCompleted: (data) => {
            if (data.register.success) {
                setInfoInvalid(false);
                localStorage.setItem(AUTH_TOKEN, data.register.token);
                navigate('/');
            } else {
                setInfoInvalid(true);
            }
        },
    });

    return (
      <form>
        <h3>Sign Up</h3>
        <div className="mb-3">
          <label>First name</label>
          <input
            type="text"
            className="form-control"
            placeholder="First name"
            onChange={(e) =>
                setFormState({
                    ...formState,
                    first_name: e.target.value
                })
            }
          />
        </div>
        <div className="mb-3">
          <label>Last name</label>
          <input 
            type="text" 
            className="form-control" 
            placeholder="Last name" 
            onChange={(e) =>
                setFormState({
                    ...formState,
                    last_name: e.target.value
                })
            }
          />
        </div>
        <div className="mb-3">
          <label>Email address</label>
          <input
            type="email"
            className="form-control"
            placeholder="Enter email"
            onChange={(e) =>
                setFormState({
                    ...formState,
                    email: e.target.value
                })
            }
          />
        </div>
        <div className="mb-3">
          <label>Password</label>
          <input
            type="password"
            className="form-control"
            placeholder="Enter password"
            onChange={(e) =>
                setFormState({
                    ...formState,
                    password: e.target.value
                })
            }
          />
        </div>
        {infoInvalid && (
            <>
                <div style={{ color: 'red' }}>
                    One of more fields above is invalid!
                </div>
                <br></br>
            </>
        )}
        <div className="d-grid">
          <div type="submit" className="btn btn-primary" onClick={signup}>
            Sign Up
          </div>
        </div>
        <p className="forgot-password text-right">
          Already registered <a href="/sign-in">sign in?</a>
        </p>
      </form>
    )
}

export default SignUp;