import os
import json
import hashlib
from typing import Dict, Optional
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_key(self, data: str) -> str:
        """Generate a cache key from input data."""
        return hashlib.md5(data.encode()).hexdigest()

    def _get_cache_path(self, key: str) -> str:
        """Get the full path for a cache file."""
        return os.path.join(self.cache_dir, f"{key}.json")

    def get(self, key: str) -> Optional[Dict]:
        """Get cached data if it exists and is not expired."""
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                # Check if cache is expired (24 hours)
                cached_time = datetime.fromisoformat(data['cached_at'])
                if datetime.now() - cached_time < timedelta(hours=24):
                    return data['content']
            except Exception:
                pass
        return None

    def set(self, key: str, content: Dict):
        """Cache data with timestamp."""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w') as f:
                json.dump({
                    'content': content,
                    'cached_at': datetime.now().isoformat()
                }, f)
        except Exception as e:
            print(f"Error caching data: {e}")
