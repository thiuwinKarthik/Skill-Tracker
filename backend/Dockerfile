FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install spaCy and English model
RUN pip install spacy==3.6.1 \
    && pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.1/en_core_web_sm-3.6.1-py3-none-any.whl

# Copy app code
COPY . .

# Expose port for FastAPI
EXPOSE 10000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
