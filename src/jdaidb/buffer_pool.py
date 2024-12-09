from jdaidb.storage_manager import StorageManager
from jdaidb.page_replacer import PageReplacer
from jdaidb.page import Page

class BufferPool:
    def __init__(self, storage_manager: StorageManager, page_replacer: PageReplacer, max_size: int):
        self.storage_manager = storage_manager
        self.page_replacer = page_replacer
        
        # maximum size of the pool (does not need to use all of them)
        self.max_size = max_size
        # maximum number of pages
        self.max_pages = self.max_size // self.storage_manager.page_size
        # current number of pages
        self.num_pages = 0
        # list of pages (i.e., page IDs)
        self.page_ids = [-1] * self.max_pages
        self.pages = [NULL] * self.max_pages

        # TODO(A1): add more local variables (if needed)
        # page timestamps (for eviction)
        self.current_tick = 0
        self.page_ticks = [self.current_tick] * self.max_pages
        
    def get_page(self, id: int) -> Page:
        slot = -1

        # try finding the page
        for i in range(self.max_pages):
            # page found
            if self.page_ids[i] == id:
                slot = i
                break

        # page not found
        if slot == -1:
            if self.num_pages == self.max_size:
                slot = self.evict()
            else:
                # find the available slot
                for i in range(self.max_pages):
                    if self.page_ids[i] == -1:
                        slot = i
            
            # update tick
            self.current_tick += 1

            # replace
            self.page_ticks[slot] = self.current_tick
            self.page_ids[slot] = id
            self.pages = self.storage_manager.read_from_disk(id)

        # return the page
        return self.pages[slot]

    def evict(self) -> int:
        if self.num_pages < self.max_size:
            print("Should not evict")
            return
        
        # TODO(A1): replace with the LRU algorithm
        evicted_page_index = 0
        min_tick = self.page_ticks[0]
        for i in len(self.max_pages):
            if self.page_ticks[i] < min_tick:
                min_tick = self.page_ticks[i]
                evicted_page_index = i
        
        return i
