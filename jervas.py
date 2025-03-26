import speech_recognition as sr
import pyttsx3
import datetime
import requests
import time
import threading
import numexpr as ne
import os

try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
except Exception as e:
    print(f"Error initializing pyttsx3: {e}")
    exit(1)

should_exit = False

reminders = []
reminders_lock = threading.Lock()

API_KEY = 'bc684fae3120dc80d09629437ae5de55'

def speak(text):
    """Convert text to speech and play it."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def set_female_voice():
    """Set the voice to a female option if available."""
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} ({voice.id})")
        if 'female' in voice.name.lower() or 'zelda' in voice.name.lower() or 'tessa' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            speak("Female voice activated.")
            return
    print("No female voice found. Using default voice.")
    speak("No female voice found. Using default voice.")

def play_wakeup_sound():
    """Play a simple wake-up sound (beep) if available."""
    try:
        if os.name == 'nt':
            import winsound
            winsound.Beep(1000, 200)
    except Exception:
        pass 

def greet():
    """Greet the user upon starting the assistant."""
    play_wakeup_sound()
    speak("Hello! I am JERVAS, your personal assistant. Say 'JERVAS help' to learn what I can do.")

def tell_time():
    """Tell the current time."""
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    speak(f"The current time is {time_str}")

def tell_date():
    """Tell the current date."""
    now = datetime.datetime.now()
    date_str = now.strftime("%B %d, %Y")
    speak(f"Today is {date_str}")

def calculate(expression):
    """Perform a mathematical calculation safely using numexpr."""
    try:
        result = ne.evaluate(expression).item()
        speak(f"The result is {result}")
    except Exception as e:
        print(f"Calculation error: {e}")
        speak("Sorry, I couldn't calculate that. Please use numbers and operators like plus, minus, times, or divided by.")

def get_weather(city):
    """Fetch and speak the current weather for a specified city."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            speak(f"The weather in {city} is {weather} with a temperature of {temperature} degrees Celsius.")
        else:
            speak(f"Sorry, I couldn't find weather data for {city}.")
    except requests.RequestException as e:
        print(f"Weather fetch error: {e}")
        speak("Sorry, there was an error getting the weather. Check your internet connection.")

def check_reminders():
    """Check if any reminders are due and speak them."""
    now = datetime.datetime.now()
    with reminders_lock:
        for reminder in reminders[:]:
            if reminder[0] <= now:
                play_wakeup_sound()
                speak(f"Reminder: {reminder[1]}")
                reminders.remove(reminder)

def list_help():
    """List available commands."""
    speak("Here’s what I can do: say 'JERVAS time' for the time, 'date' for the date, 'calculate' followed by a math expression, 'weather in' followed by a city, 'set reminder at' with a time like 14:30 and a message, or 'exit' to stop me.")

def process_command(recognizer, audio):
    """Process recognized audio commands in the background."""
    global should_exit
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        if "jervas" in command:
            play_wakeup_sound()
            command = command.replace("jervas", "").strip()
            print(f"Processing command: {command}")
            if "time" in command:
                tell_time()
            elif "date" in command:
                tell_date()
            elif "calculate" in command:
                try:
                    expression = command.split("calculate", 1)[1].strip()
                    expression = expression.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
                    calculate(expression)
                except IndexError:
                    speak("Please provide a calculation after 'calculate', like '5 plus 3'.")
            elif "weather in" in command:
                try:
                    city = command.split("weather in", 1)[1].strip()
                    get_weather(city)
                except IndexError:
                    speak("Please specify a city after 'weather in'.")
            elif "set reminder at" in command:
                try:
                    parts = command.split("set reminder at", 1)[1].strip().split(" to ", 1)
                    time_str = parts[0].strip()
                    message = parts[1].strip()
                    now = datetime.datetime.now()
                    reminder_time = datetime.datetime.strptime(time_str, "%H:%M").replace(
                        year=now.year, month=now.month, day=now.day
                    )
                    if reminder_time < now:
                        reminder_time += datetime.timedelta(days=1)
                    with reminders_lock:
                        reminders.append((reminder_time, message))
                    speak(f"Reminder set for {time_str} to {message}")
                except Exception as e:
                    print(f"Reminder error: {e}")
                    speak("Sorry, I couldn’t set the reminder. Say it like 'set reminder at 14:30 to call mom'.")
            elif "help" in command:
                list_help()
            elif "exit" in command or "stop" in command:
                speak("Goodbye! Shutting down now.")
                should_exit = True
            else:
                speak("Sorry, I didn’t understand that. Say 'JERVAS help' for a list of commands.")
    except sr.UnknownValueError:
        print("Speech not recognized")
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        speak("Sorry, there was an error with speech recognition. Please check your internet.")

def main():
    """Main function to run the assistant."""
    set_female_voice()
    greet()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Adjustment complete. Listening in the background.")

    stop_listening = recognizer.listen_in_background(microphone, process_command)

    while not should_exit:
        check_reminders()
        time.sleep(1)

    stop_listening(wait_for_stop=False)
    print("JERVAS has stopped.")

if __name__ == "__main__":
    required_modules = ['speech_recognition', 'pyttsx3', 'requests', 'numexpr']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Missing module: {module}. Install it with 'pip install {module}'")
            exit(1)

    if API_KEY == 'bc684fae3120dc80d09629437ae5de55':
        print("Warning: Replace 'bc684fae3120dc80d09629437ae5de55' with a valid OpenWeatherMap API key for weather functionality.")
    
    main()