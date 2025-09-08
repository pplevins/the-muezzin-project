FROM python:3.12-slim
LABEL authors="pplevins"
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY app/services/processor/data_processor.py ./processor/data_processor.py
COPY app/services/processor/__init__.py ./processor/__init__.py
COPY app/core ./core
COPY app/dal ./dal
COPY app/utils ./utils
COPY app/models ./models
COPY app/tests/processor_main.py processor_main.py
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "processor_main.py"]