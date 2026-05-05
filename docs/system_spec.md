# 🧠 Drug Search System — System Specification (PRD + TRD)

---

# 1. 📌 Overview

## 1.1 Product Name

Drug/Product Search System

## 1.2 Objective

Build a complete system that:

* Crawls product data from https://chiaki.vn/
* Stores data locally
* Indexes data for search
* Provides search API

---

# 2. 🎯 Scope

## 2.1 In Scope

* Crawl ~1000 products
* Extract:

  * name
  * description
  * comments (if available)
* Store in MongoDB
* Build keyword search using Elasticsearch
* Provide API `/search?q=...`

## 2.2 Out of Scope

* Authentication
* Payment
* Recommendation system
* Semantic/vector search

---

# 3. 🏗️ System Architecture

```text
Crawler → MongoDB → Elasticsearch → FastAPI → Client
```

---

# 4. 🧱 Tech Stack

* Crawl: requests + BeautifulSoup
* Database: MongoDB (local)
* Search Engine: Elasticsearch
* API: FastAPI
* Container: Docker

---

# 5. 📁 Project Structure

```text
drug-search-system/

├── crawler/
├── data_pipeline/
├── database/
├── search_service/
├── config/
├── scripts/
├── docs/
```

---

# 6. 🕷️ Crawler Module

## Responsibilities

* Crawl product pages from Chiaki.vn
* Extract product information

## Strategy

* BFS crawl
* Start from homepage
* Follow internal links only
* Filter product pages using `/p/`

## Constraints

* max_products = 1000
* delay = 1 second
* must not crash

---

## Input

```text
start_url: str
```

---

## Output

```json
{
  "name": str,
  "description": str,
  "comments": list[str],
  "url": str
}
```

---

# 7. 🗄️ Database Module

## Database

MongoDB (local)

## Database Name

drug_search

## Collection

products

---

## Schema

```json
{
  "_id": ObjectId,
  "name": string,
  "description": string,
  "comments": [string],
  "url": string,
  "combined_text": string,
  "created_at": datetime
}
```

---

## Functions

```text
insert_product(product)
get_all_products()
```

---

# 8. 🧹 Data Pipeline Module

## Responsibilities

* Clean data
* Transform data
* Prepare for indexing

---

## Cleaning Rules

* lowercase text
* remove special characters
* trim whitespace

---

## Transformation Logic

```text
combined_text = name + " " + description + " " + " ".join(comments)
```

---

## Pipeline Flow

```text
MongoDB → clean → transform → Elasticsearch
```

---

# 9. 🔍 Search Module

## Engine

Elasticsearch

## Index Name

products

---

## Mapping

```json
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "description": { "type": "text" },
      "comments": { "type": "text" },
      "combined_text": { "type": "text" }
    }
  }
}
```

---

## Query

```json
{
  "query": {
    "match": {
      "combined_text": "<query>"
    }
  }
}
```

---

## Output

```json
[
  {
    "name": string,
    "score": float
  }
]
```

---

# 10. 🚀 API Module

## Framework

FastAPI

---

## Endpoint

### GET /search

### Query Params

```text
q: string
```

---

## Response

```json
[
  {
    "name": "...",
    "score": 0.92
  }
]
```

---

# 11. ⚙️ Configuration

```python
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "drug_search"

ES_HOST = "http://localhost:9200"
ES_INDEX = "products"

MAX_PRODUCTS = 1000
CRAWL_DELAY = 1
```

---

# 12. 🐳 Deployment

## Docker Services

* MongoDB
* Elasticsearch

---

# 13. 🔄 Execution Flow

```text
1. Start Docker
2. Run crawler → save MongoDB
3. Run pipeline → index Elasticsearch
4. Run API
5. Query via /search
```

---

# 14. ⚠️ Constraints

* Must handle HTTP errors (403, timeout)
* Must not crash when parsing fails
* Must respect crawl delay

---

# 15. 📊 Success Criteria

* ≥ 500 products crawled
* Search response < 1s
* Relevant results returned

---

# 16. 🧪 Testing

* Test crawler output
* Test database insert
* Test search results
* Test API endpoint

---

# 17. 📌 Notes for Coding Agent

* Follow module responsibilities strictly
* Do not over-engineer
* Handle errors gracefully
* Keep functions simple and readable
* Use clean separation of concerns
* Always validate data before storing

---

# ✅ END OF SPEC
