# Use Python 3 as the base image
FROM python:3

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensures Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY docker/requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the entire current directory into the container
COPY . /app/