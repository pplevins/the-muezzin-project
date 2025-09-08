import time
from pathlib import Path


class MetadataExtractor:
    """A utility class to extract metadata from binary files"""

    def __init__(self, dir_path):
        self._dir_path = Path(dir_path)

    def get_all_in_dir(self):
        """Get all file paths in the directory as an iterator mapping object (not a list)"""
        return self._dir_path.glob("*")

    def extract_metadata(self, file_path):
        """Extract metadata from given file path"""
        return {
            "path": file_path,
            "name": self._get_filename(file_path),
            "size_in_bytes": self._get_filesize(file_path),
            "created_at": self._get_creation_time(file_path),
            "last_modified": self._get_last_modified(file_path),
            "file_type": self._get_filetype(file_path)
        }

    @staticmethod
    def _get_filename(file_path):
        """Extract filename from given file path"""
        return file_path.stem

    @staticmethod
    def _get_filesize(file_path):
        """Extract file size from given file path"""
        return file_path.stat().st_size

    @staticmethod
    def _get_creation_time(file_path):
        """Extract creation time from given file path"""
        file_time = file_path.stat().st_ctime
        return time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(file_time))

    @staticmethod
    def _get_last_modified(file_path):
        """Extract last modified time from given file path"""
        file_time = file_path.stat().st_mtime
        return time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(file_time))

    @staticmethod
    def _get_filetype(file_path):
        """Extract file type from given file path"""
        return file_path.suffix
