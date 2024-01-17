# Beatles API Project

This project is a Django-based web application that provides an API for managing music album data, specifically focusing on the Beatles. It includes models for albums, songs, songwriters, and singers.

## Installation Instructions

To set up the project on your local machine, follow these steps:

1. **Clone the Repository:**

~~~
git clone https://github.com/ms8909/media_company.git
cd media_company
~~~

2. **Create and Activate a Virtual Environment (optional but recommended):**
For Unix or MacOS:

```
python3 -m venv venv
source venv/bin/activate
```
3. **Install Required Packages:**
```
pip install -r requirements.txt
```
4. **Run the Django Development Server:**
```
python manage.py runserver
```

## API Documentation

After running the application, you can access the API documentation at:
[http://127.0.0.1:8000/beatles/swagger/](http://127.0.0.1:8000/beatles/swagger/)

This documentation is provided by Swagger, and you can log in using the credentials (username: `evident`, password: `dev_interview`) to interact with the APIs.

## Admin Panel

The Django admin panel is accessible at:
[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Login credentials for the admin panel are:
- Username: `admin`
- Password: `admin`

## System Design

The system consists of a single backend service named `beatles`. This service is responsible for all backend logic, data handling, and API endpoints. It's built using Django and Django Rest Framework, and it follows RESTful principles for API design.


## Database Information

This application uses a PostgreSQL database service hosted by Vercel. The database is located in a Washington server.

### Performance Note:
- The read and write operations to this PostgreSQL database might be slower than usual, which can affect the response times of the APIs. This latency is due to the geographical location and performance characteristics of the cloud-hosted database service.

Please take this into consideration when using the APIs, as there might be a noticeable delay in responses.

---



