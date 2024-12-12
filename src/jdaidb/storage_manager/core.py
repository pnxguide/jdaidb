from jdaidb.storage_manager.page import Page
from jdaidb.catalog.core import Catalog
from jdaidb.common.file import write_file, read_file, create_file

class StorageManager:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self.disk_path = catalog.disk_path
        self.page_size = catalog.page_size

        self.current_page_id = 0
        self.page_directory = {}

    """
    Public Functions
    """

    # C
    def create_page(self) -> int:
        self.current_page_id += 1
        create_file(f"{self.disk_path}/{self.current_page_id}.page")
        self.page_directory[self.current_page_id] = f"{self.disk_path}/{self.current_page_id}.page"
        return self.current_page_id
    
    # R
    def read_page(self, id: int) -> Page:
        path = self.__find_page(id)
        if path == -1:
            return None
        page_content = read_file(path)
        return Page(page_content)
    
    # U
    def update_page(self, id: int, updated_page: Page):
        path = self.__find_page(id)
        if path == -1:
            # TODO(A1): create new file for the page
            pass
        write_file(path, str(updated_page))

    # D
    def delete_page(self, id: int):
        if self.__page_exist(id):
            os.remove(self.page_directory[id])
            self.page_directory[id] = f""

    """
    Private Functions
    """

    def __page_exist(self, id: int) -> str:
        return id in self.page_directory

    def __find_page(self, id: int) -> str:
        if self.__page_exist(id):
            return self.page_directory[id]
        else:
            return None

    # TODO(A1): serialize self.page_directory into str
    def __serialize_page_directory(self) -> str:
        return ""

    # TODO(A1): cast 'data' into self.page_directory
    def __deserialize_page_directory(self, data: str):
        pass
