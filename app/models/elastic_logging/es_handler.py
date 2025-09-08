import logging
import os
from datetime import datetime, timezone

from elasticsearch import Elasticsearch


class ESHandler(logging.Handler):
    def __init__(self, index_name):
        super().__init__()
        self.es = Elasticsearch(os.environ['ELASTIC_URL'])
        self.index = index_name

    def emit(self, record):
        try:
            self.es.index(index=self.index, document={
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage()
            })
        except Exception as e:
            print(f"ES log failed: {e}")
