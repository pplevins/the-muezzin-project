from bson.binary import Binary


# TODO: Change the implementation to use GridFS for large binary files

class BinaryFileHandler:
    @staticmethod
    def get_binary_from_file(file_path):
        with open(file_path, "rb") as file:
            binary_blob = file.read()
        return Binary(binary_blob)
