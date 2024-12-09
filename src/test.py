from jdaidb.buffer_pool import BufferPool
from jdaidb.storage_manager import StorageManager
from sunbears.dataframe import DataFrame

sm = StorageManager(page_size=1024)
bp = BufferPool(storage_manager=sm, max_size=1048576)

page = bp.get_page(id=1)
df = page.to_dataframe()
print(df)
