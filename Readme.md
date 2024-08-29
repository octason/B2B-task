# Test wallet task

Prerequisites

Before you begin, ensure you have the following installed:

    Docker
    Docker Compose

Setup Instructions

# 1. Clone the Repository

Start by cloning the repository to your local machine:

```shell
git clone https://github.com/octason/B2B-task.git
cd b2b_wallet_project
```

# 2. Create the .env File

You need to create a .env file in the root directory of the project. This file will store your environment variables.

To generate the .env file, you can copy the .env.template provided in the repository:
```shell
cp .env.template .env
```
# 3. Fill in the .env File

Open the .env file in your preferred text editor and fill in the required environment variables.

### Database settings

```shell
MYSQL_DATABASE=mydatabase
MYSQL_USER=root
MYSQL_PASSWORD=rootpassword
MYSQL_HOST=db
MYSQL_PORT=3306
```

### Other settings

Make sure to replace the placeholders with your actual configuration values.

# 4. Build and Start the Docker Containers

Once you have configured your .env file, you can build and start the Docker containers using Docker Compose:

```shell
docker-compose up
```


# 5. Access the Application

You can now access the Django application in your web browser at:

http://localhost:8000/swagger/

If you want to use admin site, you should create superuser

```shell
docker exec -it django_app /venv/bin/python manage.py createsuperuser
```