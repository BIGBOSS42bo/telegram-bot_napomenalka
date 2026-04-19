from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
import database
import sqlite3  # Добавьте эту строку

scheduler = BackgroundScheduler()

async def send_reminder(bot: Bot, user_id: int, text: str):
    await bot.send_message(chat_id=user_id, text=f"⏰ Напоминание: {text}")

def schedule_reminders(bot: Bot):
    scheduler.remove_all_jobs()
    for user_id in get_all_user_ids():
        reminders = database.get_reminders(user_id)
        for reminder_id, time_str, text in reminders:
            hour, minute = map(int, time_str.split(':'))
            scheduler.add_job(
                send_reminder,
                'cron',
                hour=hour,
                minute=minute,
                args=[bot, user_id, text],
                id=f"{user_id}_{reminder_id}"
            )

def get_all_user_ids():
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT user_id FROM reminders')
    user_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return user_ids
