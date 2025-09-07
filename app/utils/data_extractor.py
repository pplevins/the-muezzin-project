from pathlib import Path

class DataExtractor:
    """A utility class to extract metadata from binary files"""
    def __init__(self, dir_path):
        self._dir_path = Path(dir_path)

    def get_all_in_dir(self):
        return self._dir_path.glob("*")


if __name__ == "__main__":
    print(list(DataExtractor('C:\\podcasts').get_all_in_dir()))