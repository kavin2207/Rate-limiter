# Distributed Rate Limiter

A distributed, API-level rate-limiting system built using Python and FastAPI, designed to enforce request throttling correctly under concurrent and multi-instance deployments.

WHY THIS PROJECT EXISTS
Rate limiting is a core infrastructure problem in large-scale systems. Naive implementations fail under concurrency and distributed deployments. This project focuses on correctness, concurrency, and system design.

KEY CONCEPTS
- Distributed systems fundamentals
- Concurrency and shared state
- API middleware design
- Performance measurement and latency analysis
- Practical Redis usage

ARCHITECTURE
Client -> FastAPI Application -> Rate Limiter Middleware -> Algorithm (Token / Leaky Bucket) -> Redis

FEATURES
- Token Bucket and Leaky Bucket algorithms
- Modular, pluggable architecture
- Redis-backed shared state
- Middleware-based enforcement
- HTTP 429 responses with headers
- Load tested under sustained traffic

PERFORMANCE
- 100,000+ requests tested
- ~500 requests/sec sustained throughput
- ~4ms p99 latency

TECH STACK
Python, FastAPI, Redis, Docker

