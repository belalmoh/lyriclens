# LyricLens

LyricLens is a web application that provides a summary about a song and list the countries mentioned in the lyrics

## Overview

LyricLens is a web application that combines song analysis with geographical insights. The application processes song lyrics to provide concise summaries and identifies any countries referenced within the lyrics. Built with modern technologies like Django and React, it offers a containerized architecture using Docker for easy deployment and development.

The project is structured with a Django backend API that handles the song analysis logic, and a React frontend that provides an intuitive user interface. The application uses environment variables for configuration and includes comprehensive Makefile commands for streamlined development workflows.


## Features

- User-friendly song and artist search functionality through an intuitive web interface
- Song Summary Generation: Get AI-powered summaries of song lyrics
- Country Detection: Identify countries mentioned in song lyrics
- Modern Web Interface: Clean and responsive UI built with React and Tailwind CSS
- RESTful API: Well-structured backend API for song analysis
- Containerized Architecture: Easy deployment with Docker
- Development Tools: Comprehensive Makefile commands for development workflow


## Technologies

- Python
- Django
- Docker
- React with TypeScript
- Tailwind CSS
- Shadcn UI


## Prerequisites

- Docker
- Node.js

## Setup

1. Clone the repository
2. Rename `.env.example` to `.env` and set the environment variables with the correct values
3. Run `make build` to build and run the application using Docker Compose
4. _(Optional) Run `make run-frontend` to run the frontend application_

## API Documentation

The API documentation is available at `/docs`.

# Makefile Commands
```shell
make build # Builds and runs the application using Docker Compose

make run # Runs the application containers without rebuilding

make run-backend # Runs only the backend container without rebuilding

make run-frontend # Runs only the frontend application

make stop # Stops all running containers

make clean # Stops containers and removes associated volumes
```
