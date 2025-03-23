.PHONY: build run stop clean run-backend run-frontend backend-terminal

# Build and run the application
build:
	cd docker && docker-compose --env-file ../.env up --build -d && docker-compose --env-file ../.env exec backend python manage.py makemigrations && docker-compose --env-file ../.env exec backend python manage.py migrate

# Run the application without rebuilding
run:
	cd docker && docker-compose --env-file ../.env up -d

# Stop all containers
stop:
	cd docker && docker-compose --env-file ../.env down

# Clean up docker resources
clean:
	cd docker && docker-compose --env-file ../.env down -v

# Run the backend container without rebuilding
run-backend:
	cd docker && docker-compose --env-file ../.env up -d backend

# Run the frontend application
run-frontend:
	cd lyriclens-client && npm install && npm run dev

# Open a terminal in the backend container
backend-terminal:
	cd docker && docker-compose --env-file ../.env exec backend bash
