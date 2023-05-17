# Base image
FROM python:3.9

# Output redirection
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /django

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
