import speech_recognition as sr
import pyttsx3
import datetime

recognizer = sr.Recognizer()
tts = pyttsx3.init()

# Function to speak text
def speak(text):
    tts.say(text)
    tts.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn’t understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech service.")
            return ""

# Main loop
while True:
    command = listen()
    if command:
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("It is " + current_time)
        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak("Today is " + current_date)
        elif "hello" in command:
            speak("Hello! How can I help you?")
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn’t catch that. Please try again.")