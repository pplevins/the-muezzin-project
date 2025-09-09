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