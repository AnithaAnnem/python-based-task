# Use official Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy your application code
COPY samplemod/ ./samplemod/
COPY setup.py .
COPY README.rst .
COPY samplemod/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Run app (replace with your real entry point if needed)
CMD ["python3", "-m", "samplemod.sample.core"]
