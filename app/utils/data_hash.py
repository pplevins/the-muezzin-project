import hashlib


class DataHash:
    @staticmethod
    def hash_file(file_str):
        return hashlib.md5(file_str.encode('ascii')).hexdigest()
