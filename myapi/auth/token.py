from datetime import datetime, timedelta, timezone
from ..config import SECRET_KEY, ALGORITHM
from jose import jwt


def create_token(data: dict, expiry: timedelta):
    encode_data = data.copy()
    expire = datetime.now(timezone.utc) + expiry
    encode_data.update({"exp":expire})
    return jwt.encode(encode_data, SECRET_KEY, ALGORITHM)
