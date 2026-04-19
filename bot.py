import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import database
import scheduler

logging.basicConfig(level=logging.INFO)

TOKEN = "8605114997:AAG_II-LnXBlABH_M-0IryIjotplhxJab58"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я бот‑напоминатель о полезных привычках.\n"
        "Отправь мне время (в формате ЧЧ:ММ) и текст напоминания."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if ':' in text:
        try:
            time_part, reminder_text = text.split(' ', 1)
            database.add_reminder(user_id, time_part, reminder_text)
            await update.message.reply_text(f"Напоминание установлено на {time_part}: {reminder_text}")
            scheduler.schedule_reminders(context.bot)
        except ValueError:
            await update.message.reply_text("Ошибка формата. Используйте: ЧЧ:ММ текст напоминания")
    else:
        await update.message.reply_text("Отправь время (ЧЧ:ММ) и текст напоминания.")

async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    reminders = database.get_reminders(user_id)
    if not reminders:
        await update.message.reply_text("У тебя нет активных напоминаний.")
        return
    response = "Твои напоминания:\n"
    for reminder_id, time, text in reminders:
        response += f"{reminder_id}. {time}: {text}\n"
    response += "\nЧтобы удалить напоминание, отправь его номер."
    await update.message.reply_text(response)

async def delete_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        reminder_id = int(update.message.text)
        database.delete_reminder(reminder_id)
        await update.message.reply_text("Напоминание удалено.")
        scheduler.schedule_reminders(context.bot)
    except ValueError:
        await update.message.reply_text("Отправь номер напоминания для удаления.")

def main():
    database.init_db()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list", list_reminders))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Regex(r'^\d+$'), delete_reminder))
    scheduler.schedule_reminders(application.bot)
    scheduler.scheduler.start()
    application.run_polling()

if __name__ == '__main__':
    main()
