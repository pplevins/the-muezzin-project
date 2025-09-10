FROM python:3.12-slim
LABEL authors="pplevins"
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY app/services/classifier/data_classifier.py ./classifier/data_classifier.py
COPY app/services/classifier/__init__.py ./classifier/__init__.py
COPY app/utils/text_classifier.py ./utils/text_classifier.py
COPY app/utils/words_decryptor.py ./utils/words_decryptor.py
COPY app/models ./models
COPY app/tests/classifier_main.py classifier_main.py
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "classifier_main.py"]