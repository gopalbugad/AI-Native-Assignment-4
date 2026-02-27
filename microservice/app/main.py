import os
import sqlite3
import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel

# -----------------------------
# Configuration (Externalized)
# -----------------------------

DATABASE = "sqlite.db"
JWT_SECRET = os.getenv("JWT_SECRET")
DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD")
ALGORITHM = "HS256"

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable is not set")

if not DEFAULT_ADMIN_PASSWORD:
    raise RuntimeError("DEFAULT_ADMIN_PASSWORD environment variable is not set")

# -----------------------------
# App Initialization
# -----------------------------

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

def get_db():
    return sqlite3.connect(DATABASE)

# -----------------------------
# Database Initialization
# -----------------------------

@app.on_event("startup")
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()

    # Seed default admin if not exists
    cursor = conn.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        hashed = pwd_context.hash(DEFAULT_ADMIN_PASSWORD)
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", hashed)
        )
        conn.commit()

    conn.close()

# -----------------------------
# Authentication APIs
# -----------------------------

@app.post("/login")
def login(data: LoginRequest):
    conn = get_db()
    cursor = conn.execute(
        "SELECT password FROM users WHERE username = ?",
        (data.username,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row or not pwd_context.verify(data.password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": data.username,
        "iss": "user-service",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 1800
    }

# -----------------------------
# Token Verification
# -----------------------------

@app.get("/verify")
def verify(authorization: str | None = Header(default=None, alias="Authorization")):
    if not authorization:
        return {"valid": False, "message": "No token provided"}

    try:
        token = authorization.replace("Bearer ", "")
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return {"valid": True, "user": decoded["sub"]}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "message": "Token expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "message": "Invalid token"}

# -----------------------------
# Protected Endpoint
# -----------------------------

@app.get("/users")
def get_users(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "users": ["admin"],
        "requested_by": decoded["sub"]
    }

# -----------------------------
# Public Health Endpoint
# -----------------------------

@app.get("/health")
def health():
    return {"status": "ok"}
