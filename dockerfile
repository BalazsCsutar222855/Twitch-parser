# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy the Python script and requirements file into the container
COPY parser.py requirements.txt cronfile /app/

# Install Python dependencies and cron
RUN apt-get update && apt-get install -y cron \
    && pip install --no-cache-dir -r requirements.txt \
    && crontab /app/cronfile

# Set the command to start cron in the foreground
CMD ["cron", "-f"]
