import sqlite3

def init_db():
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            time TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_reminder(user_id, time, text):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reminders (user_id, time, text) VALUES (?, ?, ?)', (user_id, time, text))
    conn.commit()
    conn.close()

def get_reminders(user_id):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, time, text FROM reminders WHERE user_id = ?', (user_id,))
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def delete_reminder(reminder_id):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
    conn.commit()
    conn.close()
