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
├── compose.yaml            # Docker compose for the ElasticSearch stack (for now)
└── README.md               # Project documentation
```

---