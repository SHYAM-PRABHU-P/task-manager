import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # force voice

engine.say("Hello Shyam, voice output is working")
engine.runAndWait()
