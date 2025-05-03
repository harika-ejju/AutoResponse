#!/bin/bash

# Build and run the Docker container

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "GOOGLE_API_KEY=your_gemini_api_key"
    exit 1
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t autoresearch .

# Run the container
echo "Starting AutoResearch container..."
docker-compose up -d

# Show logs
echo "Container logs:"
docker-compose logs -f
