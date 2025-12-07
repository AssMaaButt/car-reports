from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.neo4j_repo import push_user_to_neo4j
from app.db import get_db
from app.models.user import User
from app.web.users.schemas import SignupRequest, LoginRequest, UserResponse
from app.auth.jwt import create_access_token
from app.auth.password import verify_password, hash_password

router = APIRouter(prefix="", tags=["Users"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    """
    User registration
    """
    # Truncate password to 72 bytes to avoid bcrypt error
    safe_password = payload.password[:72]

    # Check duplicates
    existing = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already exists"
        )

    # Create user
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(safe_password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    push_user_to_neo4j(user)
    return UserResponse(id=user.id, username=user.username)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    User login
    """
    safe_password = payload.password[:72]  # truncate if necessary
    user = db.query(User).filter(User.username == payload.username).first()

    if not user or not verify_password(safe_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token}
