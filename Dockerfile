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

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port that the Flask app listens on
EXPOSE 5000

# Define the command to run the application
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]