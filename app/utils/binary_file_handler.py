from bson.binary import Binary


# NOTE: this file is not used in the project, because of the use of GridFS in the MongoDB service.

class BinaryFileHandler:
    @staticmethod
    def get_binary_from_file(file_path):
        with open(file_path, "rb") as file:
            binary_blob = file.read()
        return Binary(binary_blob)
