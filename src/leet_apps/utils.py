"""
Utility helpers: simple rate limiter and caching helper for connectors (MVP).

This provides a lightweight per-host rate limiter and an in-memory cache decorator useful
for testing and to demonstrate N1 requirements.
"""
import time
import threading
from functools import wraps

# Simple per-host rate limiter using last-access timestamps
# Robots.txt parser cache
import urllib.robotparser

_robot_parsers = {}


def allowed_to_fetch(url: str, user_agent: str = "*") -> bool:
    """Check robots.txt for the given URL's host and return whether fetching is allowed.

    Results are cached per host to avoid repeated network calls. If robots.txt cannot be
    fetched or parsed, default to False (conservative).
    """
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc
        if not host:
            return False
        rp = _robot_parsers.get(host)
        if rp is None:
            robots_url = f"{parsed.scheme}://{host}/robots.txt"
            rp = urllib.robotparser.RobotFileParser()
            try:
                rp.set_url(robots_url)
                rp.read()
            except Exception:
                # If robots can't be read, be conservative and disallow
                _robot_parsers[host] = None
                return False
            _robot_parsers[host] = rp
        if _robot_parsers[host] is None:
            return False
        return _robot_parsers[host].can_fetch(user_agent, url)
    except Exception:
        return False

# Simple per-host rate limiter using last-access timestamps
_host_locks = {}
_host_last_access = {}
_host_lock = threading.Lock()


def rate_limit(host: str, min_interval: float = 1.0):
    """Decorator to ensure a minimum interval between actions for a given host."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with _host_lock:
                lock = _host_locks.setdefault(host, threading.Lock())
            with lock:
                last = _host_last_access.get(host)
                now = time.time()
                if last is not None:
                    elapsed = now - last
                    if elapsed < min_interval:
                        time.sleep(min_interval - elapsed)
                _host_last_access[host] = time.time()
                return func(*args, **kwargs)

        return wrapper

    return decorator


# Simple in-memory cache decorator (no expiration) for demonstration
_cache_store = {}


def simple_cache(key_fn=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = None
            if key_fn:
                key = key_fn(*args, **kwargs)
            else:
                key = (func.__name__, args, tuple(sorted(kwargs.items())))
            if key in _cache_store:
                return _cache_store[key]
            res = func(*args, **kwargs)
            _cache_store[key] = res
            return res

        return wrapper

    return decorator
