from gemini_intent import extract_intent
from reminder_engine import start_reminder_engine, add_reminder

print("🤖 Productive AI Agent is running.")
print("👉 Try: remind me to drink water at 10:55 pm")

# 🔔 start reminder engine in background
start_reminder_engine()

while True:
    user = input("🧑 You: ").strip()

    if not user:
        continue

    if user.lower().startswith(("python", "pip", "cd", "dir")):
        print("🤖 Please type a task, not a terminal command.")
        continue

    intent = extract_intent(user)

    if intent["intent"] == "reminder":
        add_reminder(intent["task"], intent["time"])
    else:
        print("🤖 Parsed:", intent)




