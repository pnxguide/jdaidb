class TableEntry:
    def __init__(self, table_name: str, column_names: list[str], column_types: list[type], page_ids=[]):
        self.table_name = table_name
        self.column_names = column_names
        self.column_types = column_types
        self.page_ids = page_ids

    def __str__(self):
        text = f"{self.table_name}|{len(self.column_names)}"
        for i in range(len(self.column_names)):
            text += f"|{self.column_names[i]}|{self.column_types[i]}"
        text += f"|{len(self.page_ids)}"
        for page_id in self.page_ids:
            text += f"|{page_id}"
        return text + "\n"

    """
    Public Functions
    """

    # C
    def add_page(self, page_id: int):
        if page_id in self.page_ids:
            raise ValueError(f"page {page_id} has already been added.")
        self.page_ids.append(page_id)
    
    # D
    def remove_page(self, page_id: int):
        if not page_id in self.page_ids:
            raise ValueError(f"page {page_id} has not already been added.")
        self.page_ids.remove(page_id)

    def fancy_str(self):
        text = ""
        for i in range(len(self.column_names)):
            text += f"{self.column_names[i]}-{self.column_types[i]}"
            if i < (len(self.column_names) - 1):
                text += "|"

        table_name = self.table_name.center(len(text), " ")
        
        text += "\n"
        text = table_name + "\n" + text
        
        return text
