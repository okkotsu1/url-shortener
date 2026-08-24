# ⚡ URL Shortener

A production-ready URL shortening service built with **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**. Features Redis caching, sliding window rate limiting, and full containerization.

---

## 🏗️ Architecture

```
Client → FastAPI → Redis (cache hit?)
                 ↓ cache miss
              PostgreSQL
```

```
POST /shorten → Rate Limiter (Redis) → PostgreSQL → Return short URL
GET /{code}   → Redis Cache → PostgreSQL (fallback) → 302 Redirect
```

---

## 🚀 Features

- **URL Shortening** — Generate a cryptographically secure 6-character short code
- **Redis Caching** — Frequently accessed URLs served from memory, bypassing the database
- **Sliding Window Rate Limiting** — 10 requests/minute per IP using Redis sorted sets
- **302 Redirects** — Fast redirects with proper HTTP semantics
- **Auto Documentation** — Interactive API docs via FastAPI's built-in Swagger UI
- **Fully Containerized** — One command to spin up the entire stack

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| Cache / Rate Limiter | Redis |
| ORM | SQLModel |
| Containerization | Docker + Docker Compose |
| Language | Python 3.14 |

---

## 📁 Project Structure

```
url-shortener/
├── main.py           # FastAPI app and route definitions
├── database.py       # PostgreSQL connection and session management
├── models.py         # SQLModel table definitions
├── cache.py          # Redis caching logic
├── limiter.py        # Sliding window rate limiter
├── utils.py          # Short code generator
├── Dockerfile        # App container definition
├── docker-compose.yml # Full stack orchestration
└── requirements.txt  # Python dependencies
```

---

## ⚙️ Getting Started

### Prerequisites
- Docker
- Docker Compose

### Run Locally

```bash
# Clone the repository
git clone https://github.com/okkotsu1/url-shortener.git
cd url-shortener

# Start the full stack
docker-compose up --build
```

The API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## 📡 API Reference

### Shorten a URL

```http
POST /shorten/
Content-Type: application/json

{
  "original_url": "https://www.example.com/very/long/url"
}
```

**Response:**
```json
{
  "short_code": "aB3kR9",
  "short_url": "http://localhost:8000/aB3kR9"
}
```

### Redirect

```http
GET /{short_code}
```

Returns a `302 Temporary Redirect` to the original URL.
Returns `404` if the short code doesn't exist.

---

## 🔒 Rate Limiting

The `/shorten/` endpoint is rate limited to **10 requests per minute per IP**.

Implemented using a **sliding window algorithm** with Redis sorted sets:
- Each request timestamp is stored in a Redis sorted set keyed by IP
- Timestamps older than 60 seconds are removed on each request
- If the count exceeds 10, a `429 Too Many Requests` response is returned

Exceeding the limit returns:
```json
{
  "detail": "127.0.0.1 is rate limited."
}
```

---

## ⚡ Caching Strategy

Uses a **cache-aside (lazy loading)** pattern:

1. On redirect request, check Redis first
2. **Cache hit** → return immediately (sub-millisecond)
3. **Cache miss** → query PostgreSQL, store result in Redis with 24-hour TTL
4. Subsequent requests served from Redis

---

## 🐳 Docker Services

| Service | Image | Port |
|---|---|---|
| app | Custom (FastAPI) | 8000 |
| db | postgres | 5432 |
| redis | redis | 6379 |

The app waits for PostgreSQL to pass a healthcheck before starting, preventing connection errors on cold start.

---

## 📄 License

MIT