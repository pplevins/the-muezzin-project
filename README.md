# The Muezzin Project

A backend pipline service that retrieves audio files, processes them and stores them for future use.
The project is using **Kafka** data stream to send the retrieved files to processing,
**ElasticSearch** and **Kibana** for indexing and visualizing its metadata, and **MongoDB** to store the raw binary
`WAV` files.

---

## Directory Structure

```
the-muezzin-project/
├── app/
│ ├── core/                 # The core connections (MongoDB connection class)
│ ├── dal/                  # The Data Access Layer for handling the data storage processes.
│ │
│ ├── models/               # The client models used for the project.
│ │ ├── elastic_search/         # The ElasticSearch client model.
│ │ ├── kafka/                  # The Kafka client models (Producer & Consumer).
│ │ └── elastic_logging/        # The ElasticSearch logger models (Logger & ESHandler).
│ │
│ ├── services/
│ │ ├── publisher/          # The Kafka publisher service.
│ │ └── processor/          # The data processor and storage service.
│ │
│ ├── utils/                # A utility package for necessary code procedures.
│ │ ├── data_hash.py            # hashlib for creating unique str id.
│ │ └── metadata_extractor.py   # pathlib for retrieving file metadata.
│ │
│ └── tests/                # Test code to run the services locally
├── scripts/                # Docker & CLI command scripts used for the project.
├── compose.yaml            # Docker compose for the ElasticSearch stack (elastic & kibana for now)
└── README.md               # Project documentation
```

---

## Implementation details

### Stage 1 - The Data Publisher Service

- **Requirements** - Creating a service that reads `WAV` files from a local directory, extracting its metadata, then
  publishes the data to a **Kafka** topic
- **Current implementation** - A simple local service that runs in a loop, and for every file in the local directory
  extracts its metadata and publish it. The service stops when all the files was published.
- **Rationale** - A single publish service that sets up the data pipline, and uses extracting the local data for the
  next process down the road.
- **Tech & Library Used:**
    1. `kafka` docker container and `kafka-python` for producing the data in the pipline.
    2. `pathlib` for extracting the metadata from a given file path.
- **Future Improvements:**
    - Containerization and support for remote file access.

### Stage 2 - The Data Processor Service

- **Requirements** - Creating a service that consume the published data from the **Kafka** topic, calculating a unique
  ID based on the metadata, then store the binary file in **MongoDB** and indexes the details in **ElasticSearch**.
  Also, adding **Kibana** for data visualization.
- **Current implementation** - A Kafka consumer that waiting for massages, and for every massage consumed reads the
  local file, calculates its ID, and then stores the data in the DB and Elastic.
- **Rationale** - The process data need to be consistent, so it's important to set a unique ID and store both the binary
  and the metadata under the same ID. Also, large files storage need to be supported, and the ES index should be mapped
  properly.
- **Tech & Library Used:**
    1. `kafka` docker container and `kafka-python` for consuming the data in the pipline.
    2. `hashlib` for hash and create unique ID based of the passed data parameters.
    3. `AsyncMongoClient` and `AsyncGridFS` for asynchronous database storage operation and handling large binary files.
    4. `elasticsearch` client for indexing the metadata and preparing the mapped index for future service in the
       pipline.
- **Future Improvements:**
    - Containerization and support for remote file access.
    - Minor improvements, detailed in the **TODO** comments.

### Breaking Mission - Logger

- **Requirements** - Implementing a logging process for every meaningful action in the code. The logs should be
  different: `INFO` for successful operation and `ERROR` for a failure.
- **Current implementation** - Using the given logger implementation and the ESHandler (with a few modifications), and
  calling the logger for every operation.
- **Rationale** - Logs are important for debugging and error handling, so the implementation should be integrated within
  the error handling process. every try-except should be logged.
- **Tech & Library Used:**
    1. `logging` module in python, and ESHandler implemented using the handler base class.

### Stage 3 - The Data Transcriber Service

- **Requirements** - Implementing a Speech-to-Text service for our data pipline, where every WAV file will be
  transcribed and the text will be saved in the ElasticSearch index.
- **Current implementation** -
- **Rationale** -
- **Tech & Library Used:**
    1.
    2.

- **Future Improvements:**
    - Containerization and support for remote file access.
    - Minor improvements, detailed in the **TODO** comments.

### Stage 3 - The Data Transcriber Service

- **Requirements** - Implementing a Speech-to-Text service for our data pipline, where every WAV file will be
  transcribed and the text will be saved in the ElasticSearch index.
- **Current implementation** - The processor service publishes the file Id to a new Kafka topic to flag the transcriber
  the files ready for transcription. The transcriber retrieves the Wav file from the MongoDB, transcribes it, and
  updates the text to the ElasticSearch index when finished.
- **Rationale** - The transcription process takes a long run time to transcribe the audio to text. So, it will be much
  efficient to separate this logic from the core processor, and index the metadata and store the raw audio first for
  access. Then, one file after another, the transcriber will transcribe the audio and updates its text when the
  transcription is finised.
- **Tech & Library Used:**
    1. Faster-whisper model for efficient and precise Speech-to-Text transcription, and also for retrieveing the
       detected
       language in the process.
- **Future Improvements:**
    - Containerization and support for remote file access.
    - Minor improvements, detailed in the TODO comments.

### Stage 4 - The Data Classifier Service

- **Requirements** - Implement a classifier service that will receive the transcribed text and classify its level of BDS
  threat based on a given set of words. The words are encrypted in a string and need to be decrypted before
  classification.
- **Current implementation**:
    - The transcriber service publishes the file ID and the transcribed text to a new Kafka
      topic to be consumed for classification.
      Then, the classifier will clean the text (removing stopwords, lower, etc.), classify it using a term-frequency
      algorithm based on the decrypted words lists, then it will update the classification to the ElasticSearch index.
    - After classification, The visualization in Kibana will updated and will show the count of document for each class
      and threat level using bar and pie charts.
- **Rationale**:
    - The classification process depends on the transcriber service for the text supply, so the classifier should be
      another service in the data pipline waiting for every text to be produced and then classify it and updating the
      result in the Elastic.
    - Using an encoding detector, I found that the words list is encoded using a base64 encoding. So I created a class
      with static function for decrypting the string in base64 encoding.
    - The algorithm for the classification is based on the Term-Frequency part of TF/IDF algorithm, where for each
      document it calculates it's relevancy according the count of words find in the text per the text length (in
      words).
    - The threshold for the threat classification is determent based on the score founding in the previous step. From
      examining the score distribution, I learned that most of the scores are between 0%-30%. So, I decided to put the
      threshold to be 10% for `is_bds` with medium threat level, and 20% for high threat. The result are presented in
      the Kibana Screenshots.
- **Tech & Library Used:**
    1. `base64` for the words list decryption.
    2. `nltk` for stopwords removal (normalizing the result).
    3. A self-made **Term-Frequency** algorithm for score calculation.
- **Future Improvements:**
    - Containerization and support for remote file access.
    - Minor improvements, detailed in the TODO comments.