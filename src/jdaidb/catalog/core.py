from jdaidb.catalog.table_entry import TableEntry

import os

class Catalog:
    def __init__(self, disk_path: str, page_size: int, buffer_size: int):
        self.disk_path = disk_path
        self.catalog_path = f"{disk_path}/.catalog"
        self.page_size = page_size
        self.buffer_size = buffer_size

        self.__table_directory = {}
        self.__restore()

    def teardown(self):
        self.__flush()
    
    """
    Public Functions
    """

    # C
    def add_table_entry(self, table_name: str, column_names: list[str], column_types: list[type]):
        if table_name in self.__table_directory:
            raise ValueError(f"{table_name} has already existed.")
        self.__table_directory[table_name] = TableEntry(table_name, column_names, column_types)
        self.__flush()

    # R
    def get_table_header(self, table_name: str):
        if not table_name in self.__table_directory:
            raise ValueError(f"{table_name} does not exist.")
        return self.__table_directory[table_name].fancy_str()

    def get_pages_from_table(self, table_name: str) -> list[int]:
        return self.__table_directory[table_name].page_ids

    def get_types_from_table(self, table_name: str) -> list[str]:
        return self.__table_directory[table_name].column_types

    # U
    def add_page_to_table(self, table_name: str, page_id: int):
        self.__table_directory[table_name].add_page(page_id)
        self.__flush()
    
    def remove_page_from_table(self, table_name: str, page_id: int):
        self.__table_directory[table_name].remove_page(page_id)
        self.__flush()

    # D
    def remove_table_entry(self, table_name: str):
        if not table_name in self.__table_directory:
            raise ValueError(f"{table_name} does not exist.")
        self.__table_directory.pop(table_name)
        self.__flush()

    """
    Private Functions
    """

    def __restore(self):
        # if the catalog does not exist, create the catalog
        if not os.path.exists(self.catalog_path):
            f = open(self.catalog_path, "w")
            f.close()

        # open and read the catalog
        f = open(self.catalog_path, "r")

        for line in f:
            line = line.strip()
            tokens = line.split("|")
            
            table_name = tokens[0]
            num_columns = int(tokens[1])
            column_names = []
            column_types = []
            for i in range(2, 2+(num_columns * 2), 2):
                column_names.append(tokens[i])
                column_types.append(tokens[i+1])
            num_pages = int(tokens[2+(num_columns * 2)])
            page_ids = []
            for i in range(3+(num_columns * 2), 3+(num_columns * 2)+num_pages, 1):
                page_ids.append(int(tokens[i]))

            self.__table_directory[table_name] = TableEntry(table_name, column_names, column_types, page_ids)

        f.close()

    def __flush(self):
        f = open(self.catalog_path, "w")

        table_directory_str = ""
        for table_name in self.__table_directory.keys():
            table_directory_str += str(self.__table_directory[table_name])

        f.write(table_directory_str)
        f.close()
