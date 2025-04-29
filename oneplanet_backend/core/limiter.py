import os
from slowapi import Limiter
from slowapi.util import get_remote_address

print("TESTING ENV in limiter.py:", os.getenv("TESTING"))

if os.getenv("TESTING") == "1":
    limiter = Limiter(key_func=get_remote_address, default_limits=[])
else:
    print("Limiter config: production → 100/minute")
    limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
