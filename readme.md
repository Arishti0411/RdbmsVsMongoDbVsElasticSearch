# 🧪 RDBMS vs Elasticsearch vs MongoDB - Full Text Search Demo

This project demonstrates full-text search comparisons across three systems:

- **SQLite (RDBMS)**
- **MongoDB (NoSQL)**
- **Elasticsearch (Search Engine)**

## 📁 Project Structure

```
RdbmsVsEs/
├── data/
│   └── products.json               # Sample product data
├── sqlite_demo_gui.py             # GUI demo for SQLite search
├── mongo_demo.py                  # MongoDB full-text search demo
├── elastic_search_demo.py         # Elasticsearch search demo (with modes)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## ✅ Prerequisites
- Python 3.8+
- Docker (for MongoDB and Elasticsearch)
- MongoDB Compass (optional GUI)

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 How to Run the Demos

### 🔹 SQLite (RDBMS Search)
```bash
python sqlite_demo_gui.py
```
- Search: `track` → ✅ matches
- Typo: `trak` → ❌ no match

👉 SQLite uses `LIKE '%keyword%'`, so it only supports exact substring matches.

### 🔹 MongoDB Full-Text Search
```bash
docker run -d --name mongo -p 27017:27017 mongo
python mongo_demo.py
```
- Creates a text index on description
- Searches using:

```json
{ "$text": { "$search": "track" } }
```
- ✅ Matches: track, tracking
- ❌ Doesn't match: trak, wat

👉 MongoDB uses stemming but doesn't support typo tolerance or prefix matching out of the box.

### 🔹 Elasticsearch Full-Text Search
```bash
docker run -d --name es -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.0
```
(Optional: clear previous data)

```bash
curl -X DELETE http://localhost:9200/products
```
Then run:

```bash
python elastic_search_demo.py
```
In the script, try different queries:
- `match`
- `match_phrase_prefix`
- `match` with `"fuzziness": "AUTO"`

- ✅ Matches: track, trak, wat, smart

🔍 Elasticsearch supports fuzzy search, partial matches, and customizable analyzers.

## ⏱️ Execution Time & Relevance Scoring

To make the comparison more meaningful, I added execution time tracking for each backend so I could clearly show how fast each one performs under the same search condition. This helps highlight not just how the databases behave functionally, but also how they perform in real time.

I also included relevance scoring in Elasticsearch output, which gives a sense of how strongly each result matches the search keyword—a powerful feature that sets ES apart when it comes to full-text search accuracy.

## 🧠 Comparison Table

| Feature            | SQLite      | MongoDB         | Elasticsearch         |
|--------------------|-------------|-----------------|----------------------|
| Substring Match    | ✅ (LIKE)   | ❌              | ✅ (Analyzers)        |
| Full-text Search   | ❌          | ✅              | ✅                   |
| Stemming Support   | ❌          | ✅ (Basic)      | ✅ (Advanced)         |
| Typo-tolerance     | ❌          | ❌              | ✅ (fuzziness)        |
| Prefix Matching    | ❌          | ❌              | ✅ (match_phrase_prefix) |
| Relevance Scoring  | ❌          | Limited         | ✅ (TF/IDF scoring)   |

## ✅ Do's and ❌ Don'ts

**✅ DO:**
- Use PUT in Elasticsearch to avoid duplicate documents.
- Use match_phrase_prefix for prefix/autocomplete behavior.
- Use fuzziness to allow typo tolerance in ES.

**❌ DON'T:**
- Use POST repeatedly in Elasticsearch without deleting old data.
- Expect MongoDB to handle typos or partial keywords by default.
- Combine fuzziness with match_phrase_prefix — they are incompatible.

## 🔍 Example Search Keywords to Try

| Keyword | Matches In... | Why?                                   |
|---------|---------------|----------------------------------------|
| `track`  | All           | Common word present in multiple descriptions                                 |
| `trak`   | Only ES       | Typo — only Elasticsearch handles fuzzy match                                |
| `smart`  | SQLite, ES    | Substring match in `Smartwatch` and `Smart Scale`                            |
| `wat`    | SQLite, ES    | Substring match inside `Smartwatch`, `Water Bottle`, `Smart Scale`           |
| `grip`   | All           | Present in "extra grip" → tokenized in MongoDB and ES, substring in SQLite |
| `dumbel` | Only ES       | Typo for `dumbbells` → matched by ES fuzzy search                            |

## 📝 Why MongoDB Returns Multiple Results for `track`

MongoDB uses:
- Tokenization
- Stopword removal
- Stemming (e.g., tracking → track)

MongoDB does not support partial or fuzzy matching. But it does match exact tokens like grip, track, and tracking.
It does not match typos (trak) or word fragments (wat, smar) unless they're exact indexed terms.

So when you search for `track`:
- It matches both track and tracking
- But doesn’t match trak or incomplete words like wat

## 📦 Final Notes
- MongoDB is a great choice for basic full-text search and queries
- SQLite is fast and portable but lacks deep search features
- Elasticsearch is the most powerful for search-centric use cases
