from jdaidb.catalog.core import Catalog
from jdaidb.storage_manager.core import StorageManager

class QueryEngine():
    def __init__(self, catalog: Catalog, storage_manager: StorageManager):
        self.catalog = catalog
        self.storage_manager = storage_manager

    """
    Public Functions
    """

    # CREATE TABLE
    def create_table(self, table_name: str, column_names: list[str], column_types: list[type]):
        self.catalog.add_table_entry(table_name, column_names, column_types)
        page_id = self.storage_manager.create_page()
        self.catalog.add_page_to_table(table_name, page_id)
    
    # DROP TABLE
    def drop_table(self, table_name: str):
        page_ids = self.catalog.get_pages_from_table(table_name)
        for page_id in page_ids:
            self.storage_manager.delete_page(page_id)
            self.catalog.remove_page_from_table(table_name, page_id)
        self.catalog.remove_table_entry(table_name)

    # INSERT
    def insert_tuple_into_table(self, table_name: str, tuple: tuple[...]):
        if not table_name in self.catalog.table_directory:
            raise ValueError(f"{table_name} does not exist.")

    # SELECT *
    def read_table(self, table_name: str) -> str:
        text = ""
        text += self.catalog.get_table_header(table_name)
        
        row_count = 0
        page_ids = self.catalog.get_pages_from_table(table_name)
        for page_id in page_ids:
            page = self.storage_manager.read_page(page_id)
            text += str(page)
            row_count += page.length()

        text += f"(Result: {row_count} row(s))"

        return text
