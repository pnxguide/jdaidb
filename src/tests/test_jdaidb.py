# import pytest

# import sys
# sys.path.append('./src/')

# from jdaidb.buffer_pool import BufferPool
# from jdaidb.storage_manager.core import StorageManager

# def test_simple():
#     sm = StorageManager(page_size=1024, disk_path="disks")
#     bp = BufferPool(storage_manager=sm, max_size=1048576)
#     page_id = bp.new_page()
#     print(bp.read_page(page_id).to_dataframe())
#     bp.delete_page(page_id)