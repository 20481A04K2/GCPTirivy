# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy your application code into the container
COPY app.py .

# Install Flask directly
RUN pip install --no-cache-dir flask==2.3.3

# Expose Flask default port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
