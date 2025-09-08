FROM python:3.12-slim
LABEL authors="pplevins"
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY app/services/publisher/data_publisher.py ./publisher/data_publisher.py
COPY app/services/publisher/__init__.py ./publisher/__init__.py
COPY app/utils ./utils
COPY app/models ./models
COPY app/tests/publisher_main.py publisher_main.py
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "publisher_main.py"]