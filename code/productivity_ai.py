import speech_recognition as sr
import pyttsx3
import schedule
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

    except sr.UnknownValueError:
        speak("Sorry, I could not understand")
        return ""

    except sr.RequestError:
        speak("Speech service is unavailable")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""


# =========================
# TIME PARSER (AM / PM)
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
    reminder_time = now.replace(hour=hour, minute=minute, second=0)

    if reminder_time <= now:
        reminder_time += timedelta(days=1)

    return reminder_time

# =========================
# REMINDER
# =========================
def remind(task):
    speak(f"Reminder. {task}")

# =========================
# MAIN LOGIC
# =========================
def main():
    speak("AI Productivity Assistant started")

    # =====================
    # CONVERSATION PHASE
    # =====================
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

        schedule.every().day.at(
            reminder_time.strftime("%H:%M")
        ).do(remind, task)

        speak(
            f"Task saved. I will remind you to {task} at "
            f"{reminder_time.strftime('%I:%M %p')}"
        )

        speak("Do you want to add another task?")
        answer = listen()

        if "no" in answer:
            speak("Okay. I will remind you on time.")
            break

        if "yes" in answer:
            continue

    # =====================
    # REMINDER PHASE
    # =====================
    speak("Reminder service is running")

    while True:
        schedule.run_pending()
        time.sleep(1)

# =========================
# START
# =========================
if __name__ == "__main__":
    main()
