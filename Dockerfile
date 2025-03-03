# Use a small Python image as the base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining project files
COPY . /app/

# Expose the port that the Flask app listens on
EXPOSE 5000

# Define the command to run the application
CMD ["python3", "app.py"]