from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session, select
from database import engine
from models import User
from mailer import EmailSender
from gemini_utils import get_conversion_idea
import asyncio

email_sender = EmailSender()
sched = BackgroundScheduler(timezone="Europe/Istanbul")


async def build_weekly_tip() -> str:
    return await get_conversion_idea("eski tişört")


def weekly_job():
    # 1) AI'dan fikir al (hata varsa dummy metin)
    try:
        idea = asyncio.run(build_weekly_tip())
    except Exception as e:
        idea = f"Bu hafta AI fikri alınamadı. Test e‑postası.\n(Hata: {e})"

    # 2) Tüm kullanıcıların mail listesi
    with Session(engine) as s:
        recipients = [u.email for u in s.exec(select(User))]
    if recipients:
        email_sender.send(
            recipients,
            subject="Haftanın Geri Dönüşüm Fikri ♻️",
            body=idea,
        )



# Pazartesi 09:00
sched.add_job(weekly_job, "cron", day_of_week="mon", hour=9, minute=0)


def start():
    sched.start()
