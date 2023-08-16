# Use the official Node.js image as a parent image
FROM node:16

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY ./frontend/package*.json ./

# Install any needed packages
RUN npm install

# Copy the rest of the code to the container
COPY ./frontend /app

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run the app
CMD ["npm", "start"]
