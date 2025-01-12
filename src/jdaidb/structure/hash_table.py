class HashTableEntry:
    def __init__(self):
        self.left = None
        self.right = None
        self.key = None
        
        # Doing "separate chaining" using list
        self.value = []

class HashTable:
    def __init__(self, table_size: int):
        self.table_size = table_size
        self.table = [HashTableEntry()] * self.table_size

    # TODO(A2): Implement this
    def insert(self, key, value):
        pass

    # TODO(A2): Implement this
    def read(self, key, value):
        pass

    # TODO(A2): Implement this
    def delete(self, key):
        pass

    # TODO(A2): Implement this
    def update(self, key, new_value):
        pass
