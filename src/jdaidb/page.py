from sunbears.dataframe import DataFrame

class Page:
    def __init__(self, types: list[type], tuples: list[tuple[...]], page_size: int):
        self.types = types
        self.tuples = tuples
        self.page_size = page_size
        # let's make an assumption that all the types use 32 bytes
        self.tuple_size = 32 * len(types)
        # compute the max number of tuples
        self.max_tuples = self.page_size // self.tuple_size
    
    # TODO(A1): serialize the object into a string
    #           the string should be CSV-like
    #           1st row: column names, 2nd row: column types, 3rd onwards: data
    def __str__(self):
        return ""

    # TODO(A1): deserialize the string into an object
    def __init__(self, page_str: str):
        pass

    def __init__(self, page_size: int):
        self.types = []
        self.tuples = []
        self.page_size = page_size

    # TODO(A1): add a tuple at the back of the tuple list
    #           HINT: .append(tuple)
    def add_tuple(self, new_tuple: tuple[...]):
        pass

    # TODO(A1): remove a tuple at the certain slot
    #           other tuples must be shifted
    #           HINT: .pop(index)
    def remove_tuple(self, index: int):
        pass

    # TODO(A1): convert from Page to DataFrame object
    #           HINT: Page -> CSV -> DataFrame
    def to_dataframe(self) -> DataFrame:
        return DataFrame([], [], [])
