import React, { Component, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery, gql } from '@apollo/client';
import { AUTH_TOKEN } from '../constants';
import { useLazyQuery } from '@apollo/client';

const GET_USER = gql`
    query {
        userDetails {
            id
            email
        }
    }
`;

const Homepage = (params) => {
    const token = localStorage.getItem(AUTH_TOKEN);
    console.log(token);

    const { loading, error, data, refetch} = useQuery(GET_USER, {
        context: {
            headers: {
                "authorization": "JWT " + token,
            }
        },
        fetchPolicy: "no-cache" 
    })

    console.log(data);
    const userId = data?.userDetails?.id;

    return (
        <div>
            <h3>Homepage</h3>
            <h3>{userId}</h3>
        </div>
        
    )
}

export default Homepage;
