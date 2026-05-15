import speech_recognition as sr
import pyttsx3
import time
import re
from datetime import datetime, timedelta

# =========================
# VOICE ENGINE (FEMALE)
# =========================
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 165)

def speak(text):
    print("🤖", text)
    engine.say(text)
    engine.runAndWait()

# =========================
# SPEECH RECOGNITION
# =========================
recognizer = sr.Recognizer()
recognizer.energy_threshold = 350
recognizer.dynamic_energy_threshold = False

def listen():
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)

        text = recognizer.recognize_google(audio)
        print("🧑 You said:", text)
        return text.lower().strip()

    except sr.WaitTimeoutError:
        speak("I did not hear anything")
        return ""
    except:
        speak("Sorry, I could not understand")
        return ""

# =========================
# TIME PARSER
# =========================
def parse_time(text):
    match = re.search(
        r'(\d{1,2}):(\d{2})\s*(am|pm|a\.m\.|p\.m\.)?',
        text
    )
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2))
    period = match.group(3)

    if period:
        if "p" in period and hour != 12:
            hour += 12
        if "a" in period and hour == 12:
            hour = 0

    now = datetime.now()
    dt = now.replace(hour=hour, minute=minute, second=0)

    if dt <= now:
        dt += timedelta(days=1)

    return dt

# =========================
# REMINDER STORAGE
# =========================
reminders = []  # list of (time, task)

# =========================
# MAIN
# =========================
def main():
    speak("AI Productivity Assistant started")

    # -------- Conversation Phase --------
    while True:
        speak("Tell me your task")
        task = listen()
        if task == "":
            continue

        speak("At what time should I remind you?")
        time_text = listen()
        reminder_time = parse_time(time_text)

        if not reminder_time:
            speak("I could not understand the time. Please try again.")
            continue

        reminders.append((reminder_time, task))

        speak(
            f"I will remind you to {task} at "
            f"{reminder_time.strftime('%I:%M %p')}"
        )

        speak("Do you want to add another task?")
        answer = listen()

        if "no" in answer:
            speak("Okay. I will remind you on time.")
            break

    # -------- Reminder Loop (CRITICAL) --------
    speak("Reminder service is running")

    while True:
        now = datetime.now()

        for reminder in reminders[:]:
            reminder_time, task = reminder

            # Trigger within 1 second window
            if now >= reminder_time:

                speak(f"Reminder. {task}")
                reminders.remove(reminder)

        time.sleep(0.5)

# =========================
# START
# =========================
if __name__ == "__main__":
    main()

