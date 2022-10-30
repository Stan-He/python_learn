from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb import JSONStorage
import time

#tinydb 只有MemoryStorage和JSONStorage

#tinydb middleware:CachingMiddleware
#CachingMiddleware会导致写操作不会立即落盘，会在cache中驻留，如果不调用db.storage.flush，数据就不会立即落盘
#db = TinyDB('cache_db.json', storage=CachingMiddleware(JSONStorage))

#普通的storage不会经过Cache和dump的流程
db = TinyDB('cache_db.json')
table = db.table('user')
print(table.all())
table.insert({'name': "shawn", "age": 18})
print(table.all())

