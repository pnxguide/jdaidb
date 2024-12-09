from jdaidb.page import Page
from jdaidb.catalog import Catalog

class StorageManager:
    def __init__(self, page_size: int, catalog: Catalog):
        self.page_size = page_size
        self.catalog = catalog
    
    # TODO(A1): implement this
    def read_from_disk(self, id: int) -> Page:
        path = self.catalog.find_page(id)
        if path == -1:
            return Page()

        # TODO(A1): read from the path as bytes
        bytes_in_page = read_file_as_bytes(path)

        return Page([], [])

    # TODO(A1): implement this
    def write_to_disk(self, id: int):
        pass

    # TODO(A1): implement this
    def read_file_as_bytes(filepath: str) -> bytes:
        return bytes()
