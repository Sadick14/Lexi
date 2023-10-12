import speech_recognition as sr
import pyttsx3
import datetime
import time
import os
import webbrowser


engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Hello! Sadick, I am your voice assistant. How can I help you today?")

    while True:
        query = listen().lower()

        if "exit" in query:
            speak("Goodbye! Have a great day.")
            break

        # Add more conditions based on what actions you want your assistant to perform
        elif "your_name" in query:
            speak("I am a voice assistant created with Python.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")
            speak(f"Sir, the time is {strTime}") 

        elif 'shutdown' in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call('shutdown / p /f')

        elif "restart" in query:
            print('restarting system.....')
            subprocess.call(["shutdown", "/r"])

        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")


