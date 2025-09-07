import time
from pathlib import Path


class MetadataExtractor:
    """A utility class to extract metadata from binary files"""

    def __init__(self, dir_path):
        self._dir_path = Path(dir_path)

    def get_all_in_dir(self):
        """Get all file paths in the directory as a iterator mapping object (not a list)"""
        return self._dir_path.glob("*")

    def extract_metadata(self, file_path):
        return {
            "path": file_path,
            "name": self._get_filename(file_path),
            "size_in_bytes": self._get_filesize(file_path),
            "created_at": self._get_creation_time(file_path),
            "last_modified": self._get_last_modified(file_path),
            "file_type": self._get_filetype(file_path)
        }

    def _get_filename(self, file_path):
        return file_path.stem

    def _get_filesize(self, file_path):
        return file_path.stat().st_size

    def _get_creation_time(self, file_path):
        file_time = file_path.stat().st_ctime
        return time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(file_time))

    def _get_last_modified(self, file_path):
        file_time = file_path.stat().st_mtime
        return time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(file_time))

    def _get_filetype(self, file_path):
        return file_path.suffix


if __name__ == "__main__":
    extractor = MetadataExtractor('C:\\podcasts')
    for file in extractor.get_all_in_dir():
        data = extractor.extract_metadata(file)
        print(f'file {file.name}:\n{data}\n')
