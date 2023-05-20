import { gql } from "@apollo/client";

export const GET_USER = gql`
query {
    userDetails {
        id
        username
    }
}
`;

export const CREATE_POST_MUTATION = gql`
  mutation CreatePostMutation(
    $author: ID!
    $title: String!
    $content: String!
  ) {
    createPost(
        author: $author
        title: $title
        content: $content
    ) {
        post{
            id
        }
    }
  }
`;
