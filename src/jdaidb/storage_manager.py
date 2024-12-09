from jdaidb.page import Page
from jdaidb.catalog import Catalog

class StorageManager:
    def __init__(self, page_size: int, disk_path: str):
        self.page_size = page_size
        self.disk_path = disk_path
        self.catalog = Catalog(disk_path)

    def __del__(self):
        self.catalog.flush()
    
    def read_page(self, id: int) -> Page:
        path = self.catalog.find_page(id)
        if path == -1:
            return None

        page_content = self.__read_file(path)
        return Page(page_content)
    
    def flush_page(self, id: int, updated_page: Page):
        path = self.catalog.find_page(id)
        if path == -1:
            # TODO(A1): create new file for the page
            pass

        self.__write_file(path, str(updated_page))
        
    def __read_file(self, filepath: str) -> bytes:
        f = open(filepath, "r")
        data = f.read()
        f.close()
        return data

    def __write_file(self, filepath: str, content: str) -> bytes:
        f = open(filepath, "w")
        f.write(content)
        f.close()
