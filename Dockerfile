# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of backend to /app
COPY backend /app

EXPOSE 8080
ENV PORT 8080

# Command to run on container start
CMD ["python", "main.py"]
