# src/config/settings.py

import os
from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    """
    Base configuration class for the Multi-Modal AI System.
    """
    # Environment settings
    ENV: str = Field(..., env="ENV")
    DEBUG: bool = Field(False, env="DEBUG")

    # Database settings
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(..., env="DB_PORT")
    DB_USERNAME: str = Field(..., env="DB_USERNAME")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_NAME: str = Field(..., env="DB_NAME")

    # API settings
    API_HOST: str = Field(..., env="API_HOST")
    API_PORT: int = Field(..., env="API_PORT")
    API_TIMEOUT: int = Field(30, env="API_TIMEOUT")

    # Model settings
    MODEL_PATH: str = Field(..., env="MODEL_PATH")
    MODEL_TYPE: str = Field(..., env="MODEL_TYPE")

    # Security settings
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Logging settings
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")

    # Docker settings
    DOCKER_HOST: str = Field(..., env="DOCKER_HOST")
    DOCKER_PORT: int = Field(..., env="DOCKER_PORT")

    # JavaScript settings
    JS_HOST: str = Field(..., env="JS_HOST")
    JS_PORT: int = Field(..., env="JS_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Environment-specific settings
class DevSettings(Settings):
    """
    Development environment settings.
    """
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

class StagingSettings(Settings):
    """
    Staging environment settings.
    """
    LOG_LEVEL: str = "INFO"

class ProdSettings(Settings):
    """
    Production environment settings.
    """
    LOG_LEVEL: str = "WARNING"

# Get the current environment settings
def get_settings():
    env = os.getenv("ENV")
    if env == "dev":
        return DevSettings()
    elif env == "staging":
        return StagingSettings()
    elif env == "prod":
        return ProdSettings()
    else:
        raise ValueError("Invalid environment")

# Example usage
if __name__ == "__main__":
    settings = get_settings()
    print(settings)
```

```makefile
# .env
ENV=dev
DEBUG=True
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=user
DB_PASSWORD=password
DB_NAME=database
API_HOST=localhost
API_PORT=8000
API_TIMEOUT=30
MODEL_PATH=/path/to/model
MODEL_TYPE=type
SECRET_KEY=secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
DOCKER_HOST=localhost
DOCKER_PORT=2375
JS_HOST=localhost
JS_PORT=3000
```

```bash
# Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV ENV=prod
ENV DEBUG=False
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_USERNAME=user
ENV DB_PASSWORD=password
ENV DB_NAME=database
ENV API_HOST=localhost
ENV API_PORT=8000
ENV API_TIMEOUT=30
ENV MODEL_PATH=/path/to/model
ENV MODEL_TYPE=type
ENV SECRET_KEY=secret_key
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV LOG_LEVEL=INFO
ENV LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
ENV DOCKER_HOST=localhost
ENV DOCKER_PORT=2375
ENV JS_HOST=localhost
ENV JS_PORT=3000

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```javascript
// package.json
{
  "name": "multi-modal-ai-system",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.17.1"
  }
}
```

```javascript
// index.js
const express = require('express');
const app = express();
const port = process.env.JS_PORT;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Server started on port ${port}`);
});