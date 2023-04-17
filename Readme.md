# Online Chat Backend

This is the backend server for an online chat application
built with Django and Django Channels.

The backend server is designed to work with the
corresponding [frontend client](https://github.com/Maksvell129/online-chat-frontend),
which is built with React and integrates with the server using the provided API.

## Local Development Environment

### Requirements

* Python 3.10 or higher
* pip
* virtualenv (optional)
* Redis
* PostgreSQL (if not using SQLite)

### Installation

1. Clone the repository to your local machine and navigate to the project directory.
    ```bash
    git clone https://github.com/Maksvell129/online-chat-backend
    cd online-chat-backend
    ```
2. Create a virtual environment and activate it (optional).
    ```bash
    virtualenv env
    source env/bin/activate
    ```
3. Install the project dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```
4. Install Redis. You can download Redis from the official website or use your operating system's package manager to install it.
5. Create a `.env` file in the project root directory and add the following lines to it:
    ```
    USE_SQLITE=True
    REDIS_HOST=127.0.0.1
    ```
    This sets the database configuration to use SQLite by default and specifies the Redis server host to `127.0.0.1`.
    
    If you prefer to use PostgreSQL instead of SQLite update the database variables accordingly.
    ```
    DATABASE_NAME=mydatabase
    DATABASE_USER=myusername
    DATABASE_PASSWORD=mypassword
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    ```
6. Migrate the database by running:
    ```bash
    python manage.py migrate
    ```

### Running the Server

1. Start Redis server by running:
    ```bash
    redis-server
    ```
2. In a separate terminal window, start the Django development server by running:
    ```bash
    python manage.py runserver
    ```
3. Access the development server at `http://localhost:8000/`.

## Docker Compose

### Requirements

* Docker
* Docker Compose

### Installation

1. Clone the repository to your local machine and navigate to the project directory.
    ```bash
    git clone https://github.com/Maksvell129/online-chat-backend
    cd online-chat-backend
    ```

### Running the Server

1. Build and run the Docker containers by running the following command:
    ```bash
    docker-compose up --build
    ```

2. Access the development server at `http://localhost:8000/`.


### Actions

* Start the containers:
    ```bash
    docker-compose up
    ```
* Stop the containers:
    ```bash
    docker-compose down
    ```
* Create superuser
   ```bash
   docker-compose run web python manage.py createsuperuser
   ```

# About the Project

The online chat application provides a platform for users 
to send and receive messages in real-time. 
Users can create an account, login with their credentials,
and start chatting with other users.

JWT authentication is used to secure the API endpoints.
When a user logs in, the backend generates a JWT token
that the frontend can use to authenticate future requests.

The application uses Django Channels to handle the real-time communication between users.
Channels is a Django library that extends the built-in ASGI server with WebSocket support.
