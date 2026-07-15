import json
import os


class AccessCodeManager:

    def __init__(self, codes, limit, storage_path):
        self.codes = set(codes)
        self.limit = limit
        self.storage_path = storage_path
        self.usage_counts = self._load_usage_counts()

    def _load_usage_counts(self) -> dict:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_usage_counts(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.usage_counts, f)

    def remaining_uses(self, code: str) -> int:
        return self.limit - self.usage_counts.get(code, 0)

    def try_use_code(self, code: str) -> bool:
        if code not in self.codes or self.remaining_uses(code) <= 0:
            return False
        self.usage_counts[code] = self.usage_counts.get(code, 0) + 1
        self._save_usage_counts()
        return True
