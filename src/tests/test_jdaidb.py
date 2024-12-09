import pytest

import sys
sys.path.append('./src/')

from jdaidb.buffer_pool import BufferPool
from jdaidb.storage_manager import StorageManager

def test_simple():
    sm = StorageManager(page_size=1024, disk_path="disks")
    bp = BufferPool(storage_manager=sm, max_size=1048576)
    page_id = bp.new_page()
    page = bp.get_page(page_id)
    df = page.to_dataframe()
    print(df)
