import speech_recognition as sr
import pyttsx3
import schedule
import time
import dateparser
from datetime import datetime

engine = pyttsx3.init()
recognizer = sr.Recognizer()
tasks = []

def speak(text):
    print(f"🤖 {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        speak("Listening")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🧑 You said: {text}")
        return text.lower()
    except:
        speak("Sorry, I did not understand")
        return ""

def notify(task):
    speak(f"Reminder. {task}")

def smart_time_parse(text):
    return dateparser.parse(
        text,
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": datetime.now()
        }
    )

def clean_task_text(text):
    remove_words = [
        "remind me to", "remind me", "at", "after",
        "in", "tomorrow", "every day"
    ]
    for w in remove_words:
        text = text.replace(w, "")
    return text.strip()

def add_task(text):
    dt = smart_time_parse(text)

    if not dt:
        speak("I could not understand the time")
        return

    task = clean_task_text(text)
    notify_time = dt.strftime("%H:%M")

    if "every day" in text:
        schedule.every().day.at(notify_time).do(notify, task)
    else:
        schedule.every().day.at(notify_time).do(notify, task).tag(task)

    tasks.append((task, dt.strftime("%Y-%m-%d %H:%M")))
    speak(f"Task scheduled. {task} at {dt.strftime('%I:%M %p')}")

def main():
    speak("Voice AI Reminder Agent started")

    while True:
        schedule.run_pending()

        speak("Say your command")
        command = listen()

        if command == "":
            continue

        if "exit" in command or "stop" in command:
            speak("Goodbye")
            break

        if "view" in command:
            if not tasks:
                speak("No tasks scheduled")
            else:
                speak("Your tasks are")
                for t in tasks:
                    speak(f"{t[0]} at {t[1]}")
            continue

        add_task(command)
        time.sleep(1)

if __name__ == "__main__":
    main()
