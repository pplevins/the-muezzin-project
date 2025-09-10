FROM python:3.12-slim
LABEL authors="pplevins"
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY app/services/transcriber/data_transcriber.py ./transcriber/data_transcriber.py
COPY app/services/transcriber/__init__.py ./transcriber/__init__.py
COPY app/core ./core
COPY app/dal ./dal
COPY app/utils/audio_transcriber.py ./utils/audio_transcriber.py
COPY app/models ./models
COPY app/tests/transcriber_main.py transcriber_main.py
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "transcriber_main.py"]