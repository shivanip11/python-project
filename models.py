import time
from datetime import datetime

def gen_id(prefix: str = 'ID') -> str:
    return f"{prefix}{int(time.time() * 1000)}"

def now_iso() -> str:
    return datetime.now().strftime("%d-%m-%Y")

def parse_iso(s: str):
    from datetime import datetime
    return datetime.fromisoformat(s) if s else None
