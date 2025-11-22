from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _normalize(password: str) -> bytes:
    """
    Always convert password into fixed 32-byte SHA256 digest.
    This avoids bcrypt 72-byte limit safely.
    """
    return hashlib.sha256(password.encode()).digest()  # 32 bytes

def hash_password(password: str) -> str:
    """
    Hash password safely using bcrypt with SHA256 pre-hashing.
    """
    normalized = _normalize(password)
    return pwd_context.hash(normalized)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password by normalizing and checking against bcrypt hash.
    """
    normalized = _normalize(plain_password)
    return pwd_context.verify(normalized, hashed_password)
