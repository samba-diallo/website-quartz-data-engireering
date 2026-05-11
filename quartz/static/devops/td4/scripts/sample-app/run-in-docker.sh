#!/usr/bin/env bash

set -e

name=$(grep -o '"name": "[^"]*"' package.json | cut -d'"' -f4)
version=$(grep -o '"version": "[^"]*"' package.json | cut -d'"' -f4)

echo "Running $name:$version in Docker..."

# Stop and remove existing container if it exists
docker stop "$name" 2>/dev/null || true
docker rm "$name" 2>/dev/null || true

# Run the container
docker run -d \
  -p 8080:8080 \
  --name "$name" \
  "$name:$version"

echo "Container started successfully!"
echo "Access the app at: http://localhost:8080"
echo ""
echo "To view logs: docker logs $name"
echo "To stop: docker stop $name"
