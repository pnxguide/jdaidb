import os.path

class Catalog:
    def __init__(self, disk_path: str):
        self.disk_path = disk_path
        self.catalog_path = f"{disk_path}/.catalog"
        self.__read_from_disk()

        self.current_page_id = 0
        self.page_directory = {}

    def new_page_directory_entry(self) -> int:
        self.current_page_id += 1
        self.page_directory[self.current_page_id] = f"{self.disk_path}/{self.current_page_id}.page"
        return self.current_page_id

    def page_exist(self, id: int) -> str:
        return id in self.page_directory

    def find_page(self, id: int) -> str:
        if id in self.page_directory:
            return self.page_directory[id]
        else:
            return None

    # TODO(A1): cast 'data' into self.page_directory
    def __recover_page_directory(self, data: str):
        pass

    # TODO(A1): serialize self.page_directory into str
    def __str__(self):
        return ""

    def __read_from_disk(self):
        # if the catalog does not exist, create the catalog
        if not os.path.exists(self.catalog_path):
            f = open(self.catalog_path, "w")
            f.close()

        # open and read the catalog
        f = open(self.catalog_path, "r")
        catalog_content = f.read()
        f.close()
        self.__recover_page_directory(catalog_content)

    def flush(self):
        f = open(self.catalog_path, "w")
        f.write(str(self))
        f.close()
