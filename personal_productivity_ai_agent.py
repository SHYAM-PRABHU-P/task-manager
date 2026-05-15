import sqlite3
import spacy
import dateparser
import schedule
import time
from datetime import datetime

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        due_date TEXT,
        priority INTEGER,
        status TEXT DEFAULT 'pending'
    )
    """)
    conn.commit()
    conn.close()

# ---------------- NLP PARSER ----------------
def parse_command(command):
    doc = nlp(command)

    task = command
    priority = 2  # default
    due_date = None

    # Priority detection
    if "high" in command.lower():
        priority = 1
    elif "low" in command.lower():
        priority = 3

    # Date extraction
    date = dateparser.parse(command, settings={'PREFER_DATES_FROM': 'future'})
    if date:
        due_date = date.strftime("%Y-%m-%d %H:%M")
        task = command.replace(date.strftime("%Y-%m-%d %H:%M"), "")

    return task, due_date, priority

# ---------------- TASK OPERATIONS ----------------
def add_task(task, due_date, priority):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (task_name, due_date, priority) VALUES (?, ?, ?)",
        (task, due_date, priority)
    )
    conn.commit()
    conn.close()
    print(f"✅ Task added: {task}")

def view_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY priority, due_date")
    tasks = c.fetchall()
    conn.close()

    print("\n📋 Your Tasks:")
    for t in tasks:
        print(f"ID:{t[0]} | {t[1]} | Due:{t[2]} | Priority:{t[3]} | {t[4]}")
    print()

# ---------------- REMINDER ----------------
def reminder():
    now = datetime.now()
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT task_name, due_date FROM tasks WHERE status='pending'")
    for task, due in c.fetchall():
        if due:
            due_time = datetime.strptime(due, "%Y-%m-%d %H:%M")
            if 0 <= (due_time - now).total_seconds() <= 60:
                print(f"⏰ Reminder: {task} is due now!")
    conn.close()

# ---------------- MAIN LOOP ----------------
def main():
    init_db()
    schedule.every(1).minutes.do(reminder)

    print("🤖 Offline Personal Productivity AI Agent")
    print("Type your task naturally or 'view' / 'exit'\n")

    while True:
        schedule.run_pending()
        user_input = input(">> ").lower()

        if user_input == "exit":
            print("Goodbye!")
            break
        elif user_input == "view":
            view_tasks()
        else:
            task, due, priority = parse_command(user_input)
            add_task(task, due, priority)

if __name__ == "__main__":
    main()




