import threading
import time
from datetime import datetime
import tkinter as tk
from storage import load_reminders, save_reminders
from datetime import datetime, timedelta  # <-- add timedelta here



reminders = load_reminders()  # 🔹 LOAD ON STARTUP


def normalize_time(time_str):
    try:
        return datetime.strptime(time_str.lower(), "%I:%M %p").strftime("%H:%M")
    except:
        return None


def show_popup(reminder_index):
    """
    reminder_index: index of reminder in the global 'reminders' list
    """
    r = reminders[reminder_index]
    task = r["task"]

    def dismiss():
        r["done"] = True
        save_reminders(reminders)
        root.destroy()

    def snooze(minutes):
        # Recalculate new time
        new_time = (datetime.now() + timedelta(minutes=minutes)).strftime("%H:%M")
        r["time"] = new_time
        r["done"] = False
        save_reminders(reminders)
        root.destroy()
        print(f"🤖 Reminder snoozed for {minutes} min → {task}")

    root = tk.Tk()
    root.title("⏰ Reminder")
    root.attributes("-topmost", True)
    root.geometry("400x180+1000+600")
    root.resizable(False, False)

    tk.Label(
        root,
        text=task,
        font=("Segoe UI", 14),
        wraplength=350,
        justify="center"
    ).pack(pady=20)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Dismiss", width=10, command=dismiss).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Snooze 5 min", width=12, command=lambda: snooze(5)).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Snooze 10 min", width=12, command=lambda: snooze(10)).pack(side="left", padx=5)

    root.mainloop()



def add_reminder(task, time_str):
    time_24 = normalize_time(time_str)

    if not time_24:
        print("🤖 Could not understand the time.")
        return

    reminders.append({
        "task": task,
        "time": time_24,
        "done": False
    })

    save_reminders(reminders)  # 🔹 SAVE
    print(f"🤖 Reminder saved for {time_24} → {task}")


def reminder_loop():
    while True:
        now = datetime.now().strftime("%H:%M")

        for i, r in enumerate(reminders):
            if r["time"] == now and not r["done"]:
                threading.Thread(
                    target=show_popup,
                    args=(i,),
                    daemon=True
                ).start()
                r["done"] = True
                save_reminders(reminders)


        time.sleep(20)


def start_reminder_engine():
    threading.Thread(target=reminder_loop, daemon=True).start()



