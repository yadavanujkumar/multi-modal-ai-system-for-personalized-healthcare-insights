# Stage 1: Builder/compiler
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create unprivileged user
RUN groupadd -r appgroup && useradd -r -g appgroup -m -d /app appuser

# Change ownership of working directory
RUN chown -R appuser:appgroup /app

# Compile/build application (if needed)
# RUN command to compile/build application

# Stage 2: Runtime image
FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Copy application code from builder stage
COPY --from=builder /app /app

# Create unprivileged user
RUN groupadd -r appgroup && useradd -r -g appgroup -m -d /app appuser

# Change ownership of working directory
RUN chown -R appuser:appgroup /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set command to run application
CMD ["python", "app.py"]

# Health check directive
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

# Proper signal handling
ENTRYPOINT ["su", "appuser", "-c", "exec python app.py"]

# Clear metadata
LABEL maintainer="Your Name <your@email.com>"
LABEL version="1.0"
LABEL description="Multi-Modal AI System for Personalized Healthcare Insights"

# GPU support directives (if applicable)
# ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
# ENV NVIDIA_VISIBLE_DEVICES=all
# RUN apt-get update && apt-get install -y nvidia-cuda-toolkit

# CUDA dependencies (if applicable)
# RUN apt-get update && apt-get install -y nvidia-cuda-dev

# Expose port
EXPOSE 8000

# User to run the command
USER appuser:appgroup