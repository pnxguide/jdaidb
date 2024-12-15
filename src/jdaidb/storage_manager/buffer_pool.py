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
        # page timestamps (for eviction)
        self.current_tick = 0
        self.page_ticks = [self.current_tick] * self.num_slots

    """
    Public Functions
    """
    
    # TODO(A1): read the page in the database 
    def get(self, id: int) -> Page:
        # if found
        for i in range(self.num_slots):
            if self.page_ids[i] == id:
                return self.pages[i]

        return None

    # TODO(A1): write the page in the database 
    def put(self, id: int, updated_page: Page):
        # if found
        for i in range(self.num_slots):
            if self.page_ids[i] == id:
                self.pages[i] = updated_page
                return
        
        # if not found
        self.pin_page(id, updated_page)
        return

    def flush_all(self):
        for i in range(self.num_slots):
            if self.page_ids[i] != -1:
                self.storage_manager.flush_page(self.page_ids[i], self.pages[i])

    # TODO:
    def pin_page(self, id: int, new_page: Page) -> int:
        # if buffer is available
        if self.num_pages < self.num_slots:
            # find the index
            for i in range(self.num_slots):
                if self.page_ids[i] == -1:
                    index = i
                    break
        # if not, eviction is needed
        else:
            index = self.evict(id=None)
        
        # update tick
        self.current_tick += 1
        self.num_pages += 1

        # replace
        self.page_ticks[index] = self.current_tick
        self.page_ids[index] = id

        if new_page == None:
            self.pages[index] = self.storage_manager.read_page(id)
        else:
            self.pages[index] = new_page

        # return the page
        return index

    def evict(self, id=None) -> int:
        evicted_index = -1

        if id == None:
            if self.num_pages < self.num_slots:
                raise Exception("eviction should not happen")
        
            # TODO(A1): use LRU
            min_tick = self.page_ticks[0]
            for i in range(self.num_slots):
                if self.page_ticks[i] < min_tick:
                    min_tick = self.page_ticks[i]
                    evicted_index = i
        else:
            for i in range(self.num_slots):
                if self.page_ids[i] == id:
                    evicted_index = i
                    break

            if evicted_index == -1:
                raise Exception("buffer pool cannot evict")

        # TODO(A1): flush page to disk
        self.storage_manager.flush_page(self.page_ids[evicted_index], self.pages[evicted_index])

        # TODO(A1): update buffer pool entry
        self.page_ids[evicted_index] = -1
        self.page_ticks[evicted_index] = self.current_tick

        self.num_pages -= 1

        return evicted_index