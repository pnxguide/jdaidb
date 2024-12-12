class BufferPool:
    def __init__(self, num_slots: int):
        self.num_slots = num_slots
        self.num_pages = 0

        # list of pages (i.e., page IDs)
        self.page_ids = [-1] * self.num_slot
        self.pages = [None] * self.num_slot

        # TODO(A1): add more local variables (if needed)
        # page timestamps (for eviction)
        self.current_tick = 0
        self.page_ticks = [self.current_tick] * self.num_slot
    
    def pin_page(self, id: int):
        pass

    # TODO(A1): write the page in the database 
    def write_page(self, id: int, updated_page: Page):
        pass

    def delete_page(self, id: int):
        self.storage_manager.catalog.delete_page(id)

    # TODO(A1): flush the page in the buffer pool into the disk
    def flush_page(self, id: int) -> Page:
        pass

    def read_page(self, id: int) -> Page:
        if not self.storage_manager.catalog.page_exist(id):
            return None

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
                slot = self.__evict()
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
            self.pages[slot] = self.storage_manager.read_page(id)

        # return the page
        return self.pages[slot]

    def __evict(self) -> int:
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
