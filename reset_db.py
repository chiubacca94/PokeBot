# Import libraries
from tinydb import TinyDB, Query

db = TinyDB('users.json')
db.purge()
