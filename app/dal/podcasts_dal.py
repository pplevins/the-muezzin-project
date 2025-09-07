from app.core import Database


class PodcastsDal:
    def __init__(self, db: Database):
        """Constructor."""
        self.db = db

    async def list(self, collection_name):
        """List all podcasts in the database."""
        return await self.db.get_db_collection(collection_name).find().to_list()

    async def insert_document(self, collection_name, document):
        with open(document["path"], "rb") as file:
            file_id = await self.db.get_fs().put(file, filename=document["unique_id"], content_type="audio/wav")
        result = await self.db.get_db_collection(collection_name).insert_one(
            {"unique_id": document["unique_id"], "gridfs_id": file_id})
        document['podcast_id'] = str(result.inserted_id)
        return document
