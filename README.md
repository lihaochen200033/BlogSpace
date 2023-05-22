# BlogSpace

## Introduction
BlogSpace is a demo purpose project for the assessment. It is a blog, post and comment website.

## General Structure and Tech Stacks
The project utilizes many different tools for various purpose. Generally, we used Python Django as our backend server, connected to a MySQL database, using GraphQL for APIs and React as frontend.

The entire project is containerized using Docker. There are three containers, namely:
 * django_container
 * mysql_db
 * react_frontend

As names indicate, the three containers hosts our django server, our MySQL database and our React frontend respectively.

For authorization and authentication, we utilize the package **graphql_auth** for JWT implementations.

Also, the project has unit tests and test data generating scripts enabled. We will explain the functionalities and codebase later.

## Codebase Explanation

We first explain some major useful files and scripts in our codebase. Our project is generated my django project, so we follow a general structure of django projects.

**requirements.txt** records all dependencies for our Django server.

**manage.py** is the Django project overall management script. Please check official Django documentation for more information.

**docker-compose.yml** is the configuration file for containerize process. As mentioned above, we have three separate containers to be run for deployement. Note that we added a memory limit of 1G for each container, as my personal development environment is built on WSL and it consumes a lot of memory space.

**Dockerfile** is for our Django backend server container configuration. There's also **frontend/Dockerfile** for configuring our React frontend container.

There are three main directories for our Django server.
 * blog
 * core
 * users

**blog** handles everything related to posts and comments.

**users** handles everything related to users.

The DB diagram should be very similar to the sample DBdiagram given, except User table contains more infomation, as we utilize the User table from django.contrib.auth.models.

**core** is the main directory for our Django server. Please check Django documentation for more infomation. There are many modified setting for our Django server in **core/settings.py**. We added **management/setup_test_data.py** as a custom command to generate dummy data using **factories.py** scripts in **blog** and **users**. The **factories.py** scripts leverages a package called **factory_boy** for faking dummy data. We are generating 5 users, 100 posts from any user and for each post there are 0-3 comments from any user. The data are completely randomized.

There are two useful urls from our backend, mounted in **core/urls.py**. **localhost:8000/graphql/** hosts our graphql APIs. Directly accessing the url will direct to the our GraphiQL interface. **localhost:8000/admin/** hosts our django admin interface. Please check Django admin documentation for more information.

There are **schema.py** for all three directories, for generating graphql APIs. Also, there is **test/** directory in both **blog** and **users** containing all unit test scripts for all graphql APIs.

**frontend** directory contains our React frontend source code. Basically, all the frontend pages, components, images, etc. are in **frontend/src/**

Note that we use apollo client to communicate with our graphql APIs from our React frontend. It is set up in **frontend/src/index.js**

## Functionalitis Explanation 
We will explain our functionalities our the website detailedly in this section. In other words, to explain our offered graphql API functionalities. There are 11 APIs including graphql queries and mutations, which are:
### Query

* userDetails: UserType
* allPosts: [PostType]
* postById(postId: ID!): PostType
* commentByPostId(postId: ID!): [CommentType]

### Mutation
* register(
email: String!
    username: String!
    password1: String!
    password2: String!
    ): Register
* tokenAuth(
password: String!
email: String
username: String
): ObtainJSONWebToken
* createComment(
author: ID!
content: String!
post: ID!
): CreateComment
* deleteComment(id: ID!): DeleteComment
* createPost(
author: ID!
content: String!
title: String!
): CreatePost
* updatePost(
content: String
id: ID!
title: String
): UpdatePost
* deletePost(id: ID!): DeletePost

Check the **schema.py** scripts or GraphiQL interface for more details about types and queries.

The names of these APIs should be self explanatory. Note that there are authentication check for JWT token for APIs requiring authentication. Also, the frontend pages have condition checks for showing functionality buttons. As mentioned above, there are unit test scripts for all 11 functionalities offered.

## Running the Application
The following steps should successfully run the application. We assume Docker Desktop is installed already.

First, clone the project from github using
```
git clone
```

Navigate to the root of the repo in a shell, run
```
docker-compose build
docker-compose up
```
This shell should run all three containers now.

Now, accessing the url **localhost:3000** should direct you to the login page of the application.

Enjoy BlogSpace!!!

## Useful Commands and Tools
We will be adding a little bit on useful commands and tools for our application in this section.

First, in case you want to access any of the containers, run the following command in a shell while the first shell for **docker-compose up** is running.
```
docker exec -it <container_name> /bin/bash
```
This opens a bash shell for the target container.

There are some useful commands for our django_container. Using the **docker exec** command above to go into our django container, we can use the following command to run any django command
```
python manage.py <command>
```
Some useful commands include:
* runserver
* setup_test_data
* createsuperuser
* test

**runserver** command starts our server.

**setup_test_data** command sets up our test dummy data.

**createsuperuser** command creates a super user to use the django admin site.

**test** command will run all our test scripts for all 11 functionalities. There are 34 tests in total.

Note the test, setup_test_data and runserver scripts are automatically run upon running **docker-compose up**. The are logs for these scripts on the console of the shell running **docker-compose up**, so you shouldn't need to run these commands separately.

However, if you want to navigate the django admin site, you have to create the super user manually following the above steps.

As mentioned above, GraphiQL is hosted at **localhost:8000/graphql/** and django admin is hosted at **localhost:8000/admin/**

This ends our documentation, please feel free to ask any further questions regarding the demo.

Cheers!