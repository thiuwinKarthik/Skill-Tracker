FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python -m spacy download en_core_web_sm
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
