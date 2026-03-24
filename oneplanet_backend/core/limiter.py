from slowapi import Limiter
from slowapi.util import get_remote_address

from .config import RATE_LIMIT_DEFAULT, TESTING

if TESTING:
    limiter = Limiter(key_func=get_remote_address, default_limits=[])
else:
    limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT_DEFAULT])
