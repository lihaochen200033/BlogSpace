SIGNUP_QUERY = '''
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
'''

GET_USER_QUERY = '''
    query {
        userDetails {
            id
            username
        }
    }
'''

LOGIN_MUTATION = '''
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
'''

CREATE_POST_MUTATION = '''
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
'''
  
GET_POST_QUERY = '''
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
'''

UPDATE_POST_MUTATION = '''
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
'''

GET_ALL_POST = '''
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
'''

GET_COMMENTS_QUERY = '''
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
'''

CREATE_COMMENT_MUTATION = '''
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
'''

DELETE_COMMENT_MUTATION = '''
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
'''

DELETE_POST_MUTATION = '''
    mutation DeletePostMutation(
        $id: ID!
    ) {
        deletePost(id: $id) {
            post{
                id
            }
        }
    }
'''