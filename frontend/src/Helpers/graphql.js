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

export const GET_POST_QUERY = gql`
  query GET_POST_QUERY(
    $postId: ID!
  ) {
    postById(
        postId: $postId
    ) {
        id
        title
        content
        author {
            id
            username
        }
        createdOn
        updatedOn
    }
  }
`;

export const UPDATE_POST_MUTATION = gql`
  mutation UpdatePostMutation(
    $id: ID!
    $title: String
    $content: String
  ) {
    updatePost(
        id: $id
        title: $title
        content: $content
    ) {
        post{
            id
        }
    }
  }
`;

export const GET_ALL_POST = gql`
    query {
        allPosts {
            id
            title
            content
            author {
                id
                username
            }
            createdOn
            updatedOn
        }
    }
`;

export const LOGIN_MUTATION = gql`
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

export const SIGNUP_MUTATION = gql`
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

export const GET_COMMENTS_QUERY = gql`
  query GET_COMMENTS_QUERY(
    $postId: ID!
  ) {
    commentByPostId(
        postId: $postId
    ) {
        id
        content
        author {
            id
            username
        }
    }
  }
`;

export const CREATE_COMMENT_MUTATION = gql`
  mutation CreateCommentMutation(
    $author: ID!
    $content: String!
    $post: ID!
  ) {
    createComment(
        author: $author
        content: $content
        post: $post
    ) {
        comment {
            id
            content
            author {
              id
              username
            }
        }
    }
  }
`;

export const DELETE_COMMENT_MUTATION = gql`
  mutation DeleteCommentMutation(
    $id: ID!
  ) {
    deleteComment(id: $id) {
        comment {
            id
            content
        }
    }
  }
`;

export const DELETE_POST_MUTATION = gql`
  mutation DeletePostMutation(
    $id: ID!
  ) {
    deletePost(id: $id) {
        post{
            id
        }
    }
  }
`;