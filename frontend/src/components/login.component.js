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

const Login = (params) => {
    const navigate = useNavigate();
    const [formState, setFormState] = useState({
        email: '',
        password: '',
    });

    const [infoInvalid, setInfoInvalid] = useState(false);

    const [login, {data, error, loading}] = useMutation(LOGIN_MUTATION, {
        variables: {
          email: formState.email,
          password: formState.password
        },
        onCompleted: (data) => {
            if (data.tokenAuth.success) {
                setInfoInvalid(false);
                params.setLoggedIn(true);
                localStorage.setItem(AUTH_TOKEN, data.tokenAuth.token);
                navigate('/homepage');
            } else {
                setInfoInvalid(true);
            }
        }
    });

    console.log(localStorage.getItem(AUTH_TOKEN));
    return (
      <form>
        <h3>Sign In</h3>
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
        <div className="mb-3">
          <div className="custom-control custom-checkbox">
            <input
              type="checkbox"
              className="custom-control-input"
              id="customCheck1"
            />
            <label className="custom-control-label" htmlFor="customCheck1">
              Remember me
            </label>
          </div>
        </div>
        {infoInvalid && (
            <>
                <div style={{ color: 'red' }}>
                    Credentials are invalid!
                </div>
                <br></br>
            </>
        )}
        <div className="d-grid">
          <div type="submit" className="btn btn-primary" onClick={login}>
            Submit
          </div>
        </div>
        <p className="forgot-password text-right">
          Forgot <a href="#">password?</a>
        </p>
      </form>
    )
}

export default Login;
