# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install Flask directly via pip
RUN pip install --no-cache-dir flask==2.3.3

# Copy your application code into the container
COPY app.py .

# Expose the port the app runs on
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
