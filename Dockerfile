# Use an official Python runtime as a parent image
FROM python:3.7.4-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

# Run app.py when the container launches
CMD ["gunicorn", "-w1", "--bind=0.0.0.0", "label_image_server:app"]

