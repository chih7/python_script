import plyvel

db = plyvel.DB('./db/', create_if_missing=True)

db.put(b'key', b'value')
print(db.get(b'key'))

for i in range(100000):
    db.put(bytes(i), bytes(i) * 100)


db.write()


