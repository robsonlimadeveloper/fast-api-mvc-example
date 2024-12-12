from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, database
from app.database import SessionLocal, engine
from app.security.auth import create_access_token, verify_password, get_password_hash
from app.repositories.user_repository import UserRepository
from app.config import settings, pwd_settings
from app.seed import create_admin_user


models.Base.metadata.create_all(bind=engine)
create_admin_user()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if UserRepository.get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    user = UserRepository.create_user(db, username, hashed_password)
    return user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_username(db, form_data.username)
    
    print(form_data.password)
    print("user pass hash",user.hashed_password)


    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users", dependencies=[Depends(oauth2_scheme)])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return UserRepository.get_all_users(db, skip, limit)

@app.get("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def update_user(user_id: int, username: str, db: Session = Depends(get_db)):
    user = UserRepository.update_user(db, user_id, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = UserRepository.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
