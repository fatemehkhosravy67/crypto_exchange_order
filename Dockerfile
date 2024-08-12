# Use an official Python 3.10 image as the base image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a working directory for the project
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project source code to the container
COPY . /app/

# Run necessary commands to apply migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
