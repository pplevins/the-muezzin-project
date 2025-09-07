from elasticsearch import Elasticsearch


class ElasticSearchClient:
    def __init__(self, index_name):
        self.es = Elasticsearch('http://localhost:9200')
        self.index_name = index_name
        self._set_mapping()

    def _set_mapping(self):
        mappings = {
            "properties": {
                "unique_id": {
                    "type": "keyword"
                },
                "created_at": {
                    "type": "date",
                    "format": "dd-MM-yyyy HH:mm:ss"
                },
                "last_modified": {
                    "type": "date",
                    "format": "dd-MM-yyyy HH:mm:ss"
                },
                "path": {
                    "type": "keyword"
                },
                "size_in_bytes": {
                    "type": "long"
                },
                "name": {
                    "type": "keyword"
                },
                "file_type": {
                    "type": "keyword"
                }
            }
        }
        self.es.indices.delete(index=self.index_name, ignore_unavailable=True)
        self.es.options(ignore_status=[400]).indices.create(
            index=self.index_name,
            mappings=mappings
        )

    def load_to_es(self, document):
        self.es.index(
            index=self.index_name,
            id=document['unique_id'],
            document=document)
