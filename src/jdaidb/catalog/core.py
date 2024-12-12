from jdaidb.catalog.table_entry import TableEntry

import os

class Catalog:
    def __init__(self, disk_path: str, page_size: int, buffer_size: int):
        self.disk_path = disk_path
        self.catalog_path = f"{disk_path}/.catalog"
        self.restore()

        self.page_size = page_size
        self.buffer_size = buffer_size

        # catalog state
        self.__table_directory = {}
    
    def __del__(self):
        self.flush()

    def add_table_entry(self, table_name: str, column_names: list[str], column_types: list[type]):
        if table_name in self.__table_directory:
            raise ValueError(f"{table_name} has already existed.")
        self.__table_directory[table_name] = TableEntry(table_name, column_names, column_types)

    def remove_table_entry(self, table_name: str, column_names: list[str], column_types: list[type]):
        if not table_name in self.catalog.__table_directory:
            raise ValueError(f"{table_name} does not exist.")
        self.__table_directory.pop(table_name)

    def get_table_header(self, table_name: str):
        if not table_name in self.__table_directory:
            raise ValueError(f"{table_name} does not exist.")
        return str(self.__table_directory[table_name])

    def add_page_to_table(self, table_name: str, page_id: int):
        self.__table_directory[table_name].add_page(page_id)
    
    def remove_page_from_table(self, table_name: str, page_id: int):
        self.__table_directory[table_name].remove_page(page_id)
    
    def get_pages_from_table(self, table_name: str) -> list[int]:
        return self.__table_directory[table_name].page_ids

    def restore(self):
        # if the catalog does not exist, create the catalog
        if not os.path.exists(self.catalog_path):
            f = open(self.catalog_path, "w")
            f.close()

        # open and read the catalog
        f = open(self.catalog_path, "r")
        catalog_content = f.read()
        f.close()

        # TODO(A1): recover table_directory
        self.__table_directory = {}

    def flush(self):
        f = open(self.catalog_path, "w")

        # TODO(A1): serialize table_directory
        table_directory_str = ""

        f.write(table_directory_str)
        f.close()
