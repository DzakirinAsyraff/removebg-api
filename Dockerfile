# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app into the container
COPY . .

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
