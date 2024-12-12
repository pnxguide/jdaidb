from jdaidb.storage_manager.page import Page
from jdaidb.catalog.core import Catalog
from jdaidb.common.file import write_file, read_file, create_file
import os

class StorageManager:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self.disk_path = catalog.disk_path
        self.page_size = catalog.page_size

        self.current_page_id = 0
        self.page_directory = {}

        self.__restore()

    """
    Public Functions
    """

    # C
    def create_page(self) -> int:
        self.current_page_id += 1
        create_file(f"{self.disk_path}/{self.current_page_id}.page")
        self.page_directory[self.current_page_id] = f"{self.disk_path}/{self.current_page_id}.page"
        self.__flush()
        return self.current_page_id
    
    # R
    def read_page(self, id: int) -> Page:
        path = self.__find_page(id)
        if path == None:
            raise ValueError(f"Page {id} does not exist")
        page_content = read_file(path)
        return Page(page_content)
    
    # U
    def update_page(self, id: int, updated_page: Page):
        path = self.__find_page(id)
        if path == None:
            raise ValueError(f"Page {id} does not exist")
        write_file(path, str(updated_page))
        self.__flush()

    # D
    def delete_page(self, id: int):
        if self.__page_exist(id):
            os.remove(self.page_directory[id])
            self.page_directory.pop(id)
        else:
            raise ValueError(f"Page {id} does not exist")
        self.__flush()

    """
    Private Functions
    """

    def __page_exist(self, id: int) -> str:
        return id in self.page_directory

    def __find_page(self, id: int) -> str:
        return self.page_directory[id]

    def __flush(self):
        page_directory_str = f"{self.current_page_id}|{len(self.page_directory.keys())}"
        for page_id in self.page_directory.keys():
            page_directory_str += f"|{page_id}|{self.page_directory[page_id]}"
        page_directory_str += "\n"
        write_file(f"{self.disk_path}/.pagedir", page_directory_str)

    def __restore(self):
        if not os.path.exists(f"{self.disk_path}/.pagedir"):
            return
        
        content = read_file(f"{self.disk_path}/.pagedir").strip()
        tokens = content.split("|")
        self.current_page_id = int(tokens[0])
        num_page_directory_entry = int(tokens[1])
        for i in range(2, 2+num_page_directory_entry, 2):
            key = int(tokens[i])
            value = str(tokens[i+1])
            self.page_directory[key] = value
