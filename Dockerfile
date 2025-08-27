FROM python:3.11-slim

# Environment Variable
ENV PYTHONUNBUFFERED=1

# Define working Directory
WORKDIR /app

# Copy
COPY . .

# Install Poetry
RUN pip install Poetry

# Installl all dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Expose API listening port 
EXPOSE 8000

# Launch FastAPI via uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]