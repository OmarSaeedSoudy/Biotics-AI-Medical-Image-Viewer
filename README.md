# Biotics-AI-Medical-Image-Viewer
Overview
Biotics-AI Medical Image Viewer is a comprehensive application designed to handle and process medical images in DICOM format. It comprises a backend API built with Flask and Flask-Smorest and a frontend built with React. The backend provides RESTful API endpoints for managing medical records, patients, and user authentication, while the frontend offers a user-friendly interface for interacting with these functionalities.

Backend Documentation
Core Technologies
Flask: A lightweight and flexible Python web framework.
Flask-Smorest: A Flask extension for building RESTful APIs with OpenAPI 3 support.
Why Use Flask-Smorest?
Flask-Smorest simplifies API development by providing:

1- OpenAPI Documentation: Automatic generation of API documentation. (Can be accessd via "http://127.0.0.1:5000/swagger-ui" after running the application.)
2- Validation: Built-in request validation based on provided schemas.
3- Serialization: Simplified data serialization to JSON responses.
4- Error Handling: Consistent and structured error handling.
5- Code Organization: Encourages structured and organized codebase.


Project Structure
The backend is organized into the following directories and files:

instance: Configuration files
models: Database ORM models
resources: API endpoints and business logic
schemas: Marshmallow schemas for data validation and serialization
utilities: Utility classes for handling DICOM files and AWS operations
app.py: Flask application setup and configuration
db.py: Database initialization and SQLAlchemy instance
blocklist.py: JWT token blocklist for logout functionality

CORS: Enabled Cross-Origin Resource Sharing.
JWTManager: Initialized JWT for user authentication and authorization.
SQLAlchemy: Configured SQLAlchemy to connect to the database.
Amazon Web Services: S3 for Reliability & Scalability of memory and medical files.

For More Details 

Frontend Documentation
Structure
The frontend is built using React and has the following directory layout:

App.js: Main entry point of the React application.
Components: Reusable UI components.
Redux: Redux slices for managing application state.
Key Features
Routing: Defined using react-router-dom.
Components Integration: Integration of various components to create a seamless user experience.

Main Components: 
1- AuthenticatedLayout
2- DicomWebView
3- Login
4- Navbar
5- MedicalRecords
6- Patients

For More Information Visit The Full Documentation: "https://docs.google.com/document/d/1IjnTHrRA_kcik613iqSLGBoo0RlBsBugCOG-owx9wTQ/edit?usp=sharing".

# Running the Biotics-AI Medical Image Viewer Application using Docker Compose
Follow the steps below to run both the backend and frontend components of the Biotics-AI Medical Image Viewer application using Docker Compose.

Prerequisites
Docker installed
Docker Compose installed
Steps
Navigate to Project Directory

bash
Copy code
cd /path/to/project/directory
Replace /path/to/project/directory with the actual path to your project directory containing the docker-compose.yml file.

Build and Run Docker Containers

bash
Copy code
docker-compose up --build
This command will build the Docker images for both the backend and frontend, create and start the containers, and output the logs to the terminal.

Note: This build takes between 5 to 10 minutes.

Access the Application

Backend: Open your web browser and navigate to http://localhost:5000.
Frontend: Open your web browser and navigate to http://localhost:3000.
Stopping the Application
To stop the application and remove the containers, run:

bash
Copy code
docker-compose down

###########################################
IF you faced any problems you can run each Dockerfile individually

Backend Steps:
1- Navigate to Backend Directory

bash
Copy code
cd /path/to/backend/directory
Replace /path/to/backend/directory with the actual path to your backend directory containing the Dockerfile.

2- Build Docker Image

bash
Copy code
docker build -t biotics_ai_backend .

3- Run Docker Container

bash
Copy code
docker run -p 5000:5000 biotics_ai_backend
The backend server should now be running at http://localhost:5000.

Frontend Steps:

1- Navigate to Frontend Directory

bash
Copy code
cd /path/to/frontend/directory
Replace /path/to/frontend/directory with the actual path to your frontend directory containing the Dockerfile.

2- Build Docker Image

bash
Copy code
docker build -t biotics_ai_frontend .

3- Run Docker Container

bash
Copy code
docker run -p 3000:3000 biotics_ai_frontend
The frontend development server should now be running at http://localhost:3000.
