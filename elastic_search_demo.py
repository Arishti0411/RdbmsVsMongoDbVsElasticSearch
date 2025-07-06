import requests
import json
import time

# Load products
with open("data/products.json") as f:
    products = json.load(f)

# Index each product in Elasticsearch
for product in products:
    res = requests.put(
        f"http://localhost:9200/products/_doc/{product['id']}",
        json=product
    )
    if res.status_code not in [200, 201]:
        print(f"Failed to index {product['id']}: {res.text}")

# --- OPTION A: match (strict full-text search, no stemming) ---
# query = {
#     "query": {
#         "match": {
#             "description": keyword
#         }
#     }
# }

# --- OPTION B: match_phrase_prefix (matches prefix words like "track" → "tracking") ---
#keyword = "track"
#query = {
#     "query": {
#         "match_phrase_prefix": {
#             "description": keyword
#         }
#     }
# }

# --- OPTION C: match with fuzziness (for typos like 'trak') ---
keyword = "trak"
query = {
    "query": {
        "match": {
            "description": {
                "query": keyword,
                "fuzziness": "AUTO"
            }
        }
    }
}

start_time = time.time()
res = requests.get("http://localhost:9200/products/_search", json=query)
data = res.json()
elapsed = time.time() - start_time

print(f"\nSearch results for '{keyword}':")
for hit in data["hits"]["hits"]:
    source = hit["_source"]
    score = hit["_score"]
    print(f"{source['id']}: {source['name']} — {source['description']} (₹{source['price']}) [Score: {score:.2f}]")

print(f"\n⏱️ Elasticsearch search took {elapsed:.3f} seconds")