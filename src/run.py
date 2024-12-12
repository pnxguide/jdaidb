from jdaidb.interface.cli import CLI
from jdaidb.query_engine.core import QueryEngine
from jdaidb.storage_manager.core import StorageManager
from jdaidb.catalog.core import Catalog

catalog = Catalog(disk_path="disks", page_size=1024, buffer_size=1048576)
sm = StorageManager(catalog=catalog)
qe = QueryEngine(catalog=catalog, storage_manager=sm)

instance = CLI(qe)
instance.run()
