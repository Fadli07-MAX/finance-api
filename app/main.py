from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import UserDB, ItemDB, Base
from app.dependencies import get_current_admin
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

# Membuat tabel jika belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================================================
# JWT CONFIGURATION
# =========================================================
SECRET_KEY = "your-super-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================================================
# PYDANTIC SCHEMAS
# =========================================================
class Item(BaseModel):
    id: int
    name: str
    price: int

    model_config = {
        "from_attributes": True
    }


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# =========================================================
# DATABASE DEPENDENCY
# =========================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# AUTH FUNCTIONS
# =========================================================
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================================================
# BASIC ROUTES
# =========================================================
@app.get("/")
def root():
    return {
        "message": "Finance API with PostgreSQL is running!"
    }


# =========================================================
# ITEM ROUTES
# =========================================================
@app.post("/items", response_model=Item)
def create_item(
    item: Item,
    db: Session = Depends(get_db)
):
    existing_item = db.query(ItemDB).filter(
        ItemDB.id == item.id
    ).first()

    if existing_item:
        raise HTTPException(
            status_code=400,
            detail="Item ID already exists"
        )

    db_item = ItemDB(
        id=item.id,
        name=item.name,
        price=item.price
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Karena response_model=Item,
    # kita harus mengembalikan objek item langsung.
    return db_item


@app.get("/items", response_model=list[Item])
def get_items(
    db: Session = Depends(get_db)
):
    return db.query(ItemDB).all()


@app.get("/items/{item_id}", response_model=Item)
def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(ItemDB).filter(
        ItemDB.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(ItemDB).filter(
        ItemDB.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Item deleted successfully"
    }


# =========================================================
# AUTH ROUTES
# =========================================================
@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(UserDB).filter(
        UserDB.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    db_user = UserDB(
        username=user.username,
        hashed_password=hash_password(
            user.password
        )
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User created successfully"
    }


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(
        UserDB.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = (
        db.query(UserDB)
        .filter(UserDB.username == username)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user


# =========================================================
# CURRENT USER
# =========================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(UserDB).filter(
        UserDB.username == username
    ).first()

    if user is None:
        raise credentials_exception

    return user

# =========================================================
# PROTECTED ROUTE
# =========================================================

@app.get("/me")
def read_me(
    current_user: UserDB = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username
    }

from fastapi import Depends
from app.dependencies import get_current_user
from app.models import UserDB


@app.get("/me")
def get_me(current_user: UserDB = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username
    }


@app.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    users = db.query(UserDB).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
        for user in users
    ]