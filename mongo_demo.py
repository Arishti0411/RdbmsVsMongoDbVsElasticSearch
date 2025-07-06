from pymongo import MongoClient
import json
import time  # ⏱️ Import time module

# Load products
with open("data/products.json") as f:
    products = json.load(f)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.test
col = db.products

# Insert data if not already inserted
if col.count_documents({}) == 0:
    col.insert_many(products)
    print("Data inserted.")

# Create a full-text index on the 'description' field
col.create_index([("description", "text")])

# 🔍 First search: 'track'
keyword = "track"
start = time.time()
results = list(col.find({ "$text": { "$search": keyword } }))
elapsed = time.time() - start

print(f"\nSearch results for '{keyword}':")
for doc in results:
    print(f"{doc['id']}: {doc['name']} — {doc['description']} (₹{doc['price']})")

print(f"\n⏱️ MongoDB search for '{keyword}' took {elapsed:.3f} seconds")

# 🔍 Second search: 'dumbel'
keyword = "dumbel"
start = time.time()
results = list(col.find({ "$text": { "$search": keyword } }))
elapsed = time.time() - start

print(f"\nSearch results for '{keyword}':")
for doc in results:
    print(f"{doc['id']}: {doc['name']} — {doc['description']} (₹{doc['price']})")

print(f"\n⏱️ MongoDB search for '{keyword}' took {elapsed:.3f} seconds")
