# Use the official Python image as a base
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port for the Django application
EXPOSE 8000

# Default command (can be overridden in docker-compose.yml)
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000"]