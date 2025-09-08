import hashlib


class DataHash:
    @staticmethod
    def hash_file(file_str):
        """A static method to hash a given string."""
        return hashlib.md5(file_str.encode('ascii')).hexdigest()
