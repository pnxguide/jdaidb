from sunbears.dataframe import DataFrame
from jdaidb.tuple import Tuple

class Page:
    def __init__(self, slotted_array: list[int], tuples: list[Tuple]):
        self.slotted_array = []
        self.tuples = []
    
    # TODO(A1): implement this
    def to_bytes(self) -> bytes:
        return bytes()

    # TODO(A1): implement this
    def to_dataframe(self) -> DataFrame:
        return DataFrame([], [], [])
