from jdaidb.storage_manager.page import Page
# from jdaidb.storage_manager.storage_manager import StorageManager # remove since cyclic import

class BufferPool:
    def __init__(self, num_slots: int, storage_manager):
        self.storage_manager = storage_manager

        self.num_slots = num_slots
        self.num_pages = 0

        # list of pages (i.e., page IDs)
        self.page_ids = [-1] * self.num_slots
        self.pages = [None] * self.num_slots

        # TODO(A1): add more local variables (if needed)

    """
    Public Functions
    """
    
    # TODO(A1): read the page in the database 
    def get(self, id: int) -> Page:
        return None

    # TODO(A1): write the page in the database 
    def put(self, id: int, updated_page: Page):
        return

    # use by storage manager
    def flush_all(self):
        for i in range(self.num_slots):
            if self.page_ids[i] != -1:
                self.storage_manager.flush_page(self.page_ids[i], self.pages[i])

    # TODO(A1): evict the page based on the LRU policy
    #           if id is None, just evict without replacing
    #           if id is not None, evict and replace with the page with id
    def evict(self, id=None) -> int:
        pass

    """
    Private Functions
    """

    # TODO:
    def pin_page(self, id: int, new_page: Page) -> int:
        pass
