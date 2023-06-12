import hashlib
import random
import string
import datetime
import jwt
from core.system_config import access_token_expire_minutes, algorithm, secret_key


def get_random_string(length: int = 12) -> str:
    """Return generated random string (salt)."""
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def get_hash_password(password: str, salt: str = None) -> str:
    """Hash password with salt."""
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac(hash_name="sha256", password=password.encode(), salt=salt.encode(), iterations=100_000)
    return f"{salt}${enc.hex()}"


def validate_password(password: str, hashed_password: str) -> bool:
    """Validate password hash with db hash."""
    salt, hashed = hashed_password.split(sep="$")
    return get_hash_password(password=password, salt=salt) == hashed_password


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=access_token_expire_minutes)})
    return jwt.encode(payload=to_encode, key=secret_key, algorithm=algorithm)


def decode_access_token(token: str) -> str:
    try:
        encoded_jwt = jwt.decode(jwt=token, key=secret_key, algorithms=algorithm)
    except jwt.DecodeError:
        encoded_jwt = None
    return encoded_jwt
