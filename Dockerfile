# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install Flask and Google Cloud Secret Manager directly
RUN pip install --no-cache-dir flask==2.3.3 google-cloud-secret-manager==2.20.2

# Copy your application code into the container
COPY app.py .

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
