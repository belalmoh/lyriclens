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
- Search for songs by title and artist name
- View full lyrics for found songs
- Generate AI-powered analysis of song lyrics
- Extract themes, topics, and countries mentioned
- Cache analysis results for improved performance


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

## Setup & Installation

### Prerequisites

- Docker and Docker Compose
- Git

### Running with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lyriclens.git
   cd lyriclens
   ```

2. Create a `.env` file from the sample:
   ```bash
   cp sample.env .env
   ```

3. Update the `.env` file with your API keys:
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

4. Build and run the application with Docker Compose:
   ```bash
   make build
   ```

### Development Setup

To run the backend and frontend separately for development:

1. Start the backend with Redis:
   ```bash
   make run-backend
   ```

2. Start the frontend:
   ```bash
   make run-frontend
   ```

## API Endpoints

- `GET /api/song/search?query={search_term}` - Search for songs
- `GET /api/song/lyrics?artist_name={artist}&track_name={title}` - Get lyrics for a song
- `POST /api/song/analyze` - Analyze lyrics (with caching)
