# This shit is not working

# --- Build Stage ---
  FROM python:3.12-slim AS build

  ENV PYTHONUNBUFFERED=1 \
      UV_NO_CACHE_DIR=1 \
      DOCKER_BUILDKIT=1
  
  # Install curl and rust (for uv) dependencies
  RUN apt-get update && apt-get install -y curl ca-certificates build-essential \
      && rm -rf /var/lib/apt/lists/*
  
  # Install uv and add to PATH
  RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
      ln -s ~/.cargo/bin/uv /usr/local/bin/uv
  
  # Set work directory
  WORKDIR /app
  
  # Copy only pyproject.toml first for better caching
  COPY ./pyproject.toml ./
  
  # Create venv and install dependencies
  RUN uv venv && uv sync
  
  # Copy the rest of the app
  COPY ./adapters ./adapters
  COPY ./api ./api
  COPY ./domain ./domain
  COPY ./config.py ./config.py
  COPY ./main.py ./main.py
  
  # --- Runtime Stage ---
  FROM python:3.12-slim AS runtime
  
  ENV PYTHONUNBUFFERED=1
  
  WORKDIR /app
  
  # Copy the virtual environment from the build stage
  COPY --from=build /app/.venv /app/.venv
  
  # Copy application code
  COPY --from=build /app /app
  
  # Set the Python path to the venv
  ENV PATH="/app/.venv/bin:$PATH"
  
  # Run the app using the virtualenv Python
  CMD ["python", "main.py"]
  