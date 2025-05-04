from fastapi import APIRouter, Depends, HTTPException, Form
from passlib.hash import bcrypt
from sqlmodel import Session, select

from database import get_session
from models import User

router = APIRouter()

# -------- Ayarlar --------
XP_STEP = 10
BADGE_THRESHOLDS = {50: "Bronz", 150: "Gümüş", 300: "Altın"}


# -------- Kayıt --------
@router.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    if session.exec(select(User).where(User.email == email)).first():
        raise HTTPException(400, "Bu e‑posta zaten kayıtlı.")
    user = User(username=username, email=email, password_hash=bcrypt.hash(password))
    session.add(user)
    session.commit()
    return {"message": "Kayıt başarılı!"}


# -------- Giriş --------
@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        raise HTTPException(401, "Geçersiz giriş bilgisi")
    return {"message": f"Hoş geldin {user.username}!"}


# -------- Profil güncelle --------
@router.post("/update-profile")
def update_profile(
    email: str = Form(...),
    current_password: str = Form(...),
    new_username: str | None = Form(None),
    new_password: str | None = Form(None),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not bcrypt.verify(current_password, user.password_hash):
        raise HTTPException(401, "Kimlik doğrulama hatalı")

    if new_username:
        user.username = new_username
    if new_password:
        user.password_hash = bcrypt.hash(new_password)

    session.add(user)
    session.commit()
    return {"message": "Profil güncellendi!"}


# -------- XP / Rozet --------
@router.post("/gain-xp")
def gain_xp(email: str = Form(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(404, "Kullanıcı bulunamadı")
    user.xp += XP_STEP
    for th, badge in BADGE_THRESHOLDS.items():
        if user.xp >= th:
            user.badge = badge
    session.add(user)
    session.commit()
    return {"xp": user.xp, "badge": user.badge}
