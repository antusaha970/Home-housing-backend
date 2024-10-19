
# House renting project

The House Rent Site is a web application that allows users to post and find rental advertisements. The backend is built using Django, Django REST Framework, SQLite3 for the database, and Stripe for payment processing. The application supports user authentication, advertisement management, rent requests, filtering, saving favorites, and reviews and ratings.


## API documentation
Read API documentation from here made with POSTMAN
[Documentation](https://documenter.getpostman.com/view/36480406/2sA3kPp4vk) 


## Features
### User Authentication
- Users can register, log in, and log out.
- During registration, users receive an email to verify their account.
- After email verification, users can log in.
- Users can manage their profiles.
- Different user roles are available: admin and users.
- Token based Authentication

### Rent Advertise
- Users can create house rent advertisements.
- Admins can review and approve advertisements.
- Only approved advertisements are visible to all users.

### Rent Requests
- Users can send rent requests to the owner of the advertisement.
- Advertisers can accept requests.
- Once a request is accepted, no further requests can be made for that advertisement.
- While sending rent request users can pay with Credit card

### Filtering
- Users can filter rent advertisements based on categories.
- Users can filter rent advertisements based on Price,rating,division,district.

### Saving Favorites
- Users can save their favorite rent advertisements.

### Reviews and Ratings
- Users can provide ratings for any rent advertisement.

### Deployment
- The application is deployed on a secure and scalable hosting platform.


## Tech Stack

**Django:** Web framework for the backend.

**Django REST Framework:** For building APIs.

**SQLite3:** Database for storing data.

**Stripe:** Payment gateway for processing payments.


## Docker Setup

Ensure that you have Docker and Docker Compose installed on your machine.

## Building the Docker Image

```bash
  docker compose build
```

This command will build the Docker image based on the Dockerfile and configurations in docker-compose.yml.

## Running the Application

```bash
  docker compose up
```

This command will build (if not already built) and start the containers as defined in the docker-compose.yml file. The application should be accessible at http://localhost:9000.





