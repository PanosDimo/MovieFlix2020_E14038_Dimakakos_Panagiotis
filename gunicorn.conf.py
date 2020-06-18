"""Gunicorn Configuration Options."""
import multiprocessing
import os

cores = multiprocessing.cpu_count()
workers_per_core = int(os.getenv("WORKERS_PER_CORE", "2"))
max_workers_env = os.getenv("MAX_WORKERS")
max_workers = None
if max_workers_env:
    max_workers = int(max_workers_env)
web_concurrency_env = os.getenv("WEB_CONCURRENCY")
web_concurrency = None
if web_concurrency_env:
    web_concurrency = int(web_concurrency_env)
default_web_concurrency = cores * workers_per_core + 1
if web_concurrency:
    concurrency = web_concurrency
else:
    concurrency = max(default_web_concurrency, 2)
    if max_workers:
        concurrency = min(concurrency, max_workers)

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8000")

access_log = os.getenv("ACCESS_LOG") or None
error_log = os.getenv("ERROR_LOG", "-") or None

# Configuration
bind = os.getenv("BIND") or f"{host}:{port}"
loglevel = os.getenv("LOG_LEVEL", "info")
workers = concurrency
accesslog = access_log
errorlog = error_log
