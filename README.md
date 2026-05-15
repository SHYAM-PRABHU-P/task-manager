# Productivity AI Agent

A smart desktop productivity assistant powered by **Google Gemini API**.  
It helps manage reminders, notes, and to-do tasks with **natural language commands**.

---

## 🔹 Features

- **AI-powered intent parsing**: Understands natural language instructions using Google Gemini.  
- **Persistent reminders**: Reminders are saved in JSON and survive program restarts.  
- **Always-on-top popup notifications**: Desktop popups that grab attention immediately.  
- **Interactive popup controls**:
  - Dismiss reminder
  - Snooze 5 minutes
  - Snooze 10 minutes  
- **Non-blocking background engine**: The app continues listening while reminders run.  
- **Clean folder structure** for easy maintainability.

---

## 💻 Tech Stack

- Python 3.10+  
- Google Gemini API (`google.genai`)  
- `tkinter` for popups  
- JSON for persistent storage  
- `threading` for background scheduling  

---

## 🗂 Folder Structure

