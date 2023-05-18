import React from 'react';
import { useQuery, gql } from '@apollo/client';
const QUERY_USERS = gql`
    query {
        users {
        edges {
            node {
            id
            username
            email
            }
        }
        }
    }
`;
export function UserInfo() {
  // Polling: provides near-real-time synchronization with
  // your server by causing a query to execute periodically
  // at a specified interval
  const { data, loading } = useQuery(
    QUERY_USERS, {
      pollInterval: 500 // refetch the result every 0.5 second
    }
  );
  
  // should handle loading status
  if (loading) return <p>Loading...</p>;
   
  return data.users.edges.map(({ node }) => (
    <div key={node.id}>
      <p>
        User - {node.id}: {node.username} {node.email}
      </p>
    </div>
  ));
}