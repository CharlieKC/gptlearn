# Use the official Redis image as the base image
FROM redis:latest

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Expose Redis port
EXPOSE 6379

# Start Redis server
CMD ["redis-server"]
