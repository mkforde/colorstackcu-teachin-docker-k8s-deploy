# Use Python 3.11 slim image as base
# Slim images are smaller than full images, reducing build time and storage
FROM python:3.11-slim

# Set working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

# Copy requirements file first
# This is done separately to leverage Docker's layer caching
# If requirements don't change, this layer is reused
COPY web-service/requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# This comes after installing dependencies so code changes don't invalidate the pip install layer
COPY web-service/ .

# Expose port 5000 for the Flask application
# This is documentation; actual port mapping happens at runtime
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the application
# This is the default command when the container starts
CMD ["python", "app.py"]
