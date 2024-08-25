import subprocess
import speech_recognition as sr
import pyttsx3
import datetime
import time
import os
import webbrowser
import smtplib
import google.generativeai as genai
import pyaudio
import wave
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from pocketsphinx import LiveSpeech



engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('depth', 1)
engine.setProperty('voiceselect', 'english+f2')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)




def record_audio(seconds=10):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    filename = "output.wav"

    p = pyaudio.PyAudio()

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def listen():
    recognizer = sr.Recognizer()
    filename = record_audio()

    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language = "en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"
    return query

def listen_for_wake_word(wake_word="hey lexi"):
    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        filename = record_audio(seconds=5)  # Record for 2 seconds to detect wake word
        with sr.AudioFile(filename) as source:
            print("Listening for wake word...")
            audio = r.record(source)
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"User said: {query}\n")
                if wake_word in query.lower():
                    print("Wake word detected")
                    speak("Yes, 'LEXI' here! , your voice assistant. how can I help you?")
                    break
            except Exception as e:
                print(e)
                continue

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    
    # Enable low security in gmail
    address = input("Enter your email address: ")
    password = input("Enter your email password: ")
    server.login(address, password)
    server.sendmail(address, to, content)
    server.close()

def web_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    return search_url

def generate_code(prompt):
    
    genai.configure(api_key="AIzaSyDIMekkyv2GtTbHZPDBkmE5eikl9tuy9wE")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    generated_code = response.text

    return generated_code


def process_response(response):
    tokens = word_tokenize(response)

    # Remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [word for word in tokens if word.lower() not in stop_words and word not in punctuation]

    # Join the cleaned tokens back into a string
    cleaned_response = ' '.join(cleaned_tokens)

    return cleaned_response

def speak(audio):
    # processed_audio = process_response(audio)
    engine.say(audio)
    engine.runAndWait()

if __name__ == "__main__":
    
    listen_for_wake_word()
    
    speak(f"' Enter 'help' in query to know how I can assist you.")

    while True:
        speak("Enter your query")
        query = listen().lower() 
        
        if "exit" in query:
            speak("Goodbye! Have a great day.")
            break

        elif "your name" in query:
            speak("You can call me Lexi")

        elif "who are you" in query:
            speak('I am Lexi, a voice assistant whose aim is to help you')

        elif 'help' in query:
            speak(
                'My assistance includes: opening any inbuilt tool, starting services like Bluetooth, making simple web searches, providing date and time, system shutdown and restart. That\'s all for now.'
            )

        elif "bluetooth" in query:
            os.system('systemctl start bluetooth')
            speak("Bluetooth is enabled")

        elif "play music" in query or "music" in query:
            speak('Opening your music player')
            os.system("rhythmbox")
            
        elif 'date' in query:
             date_with_month = datetime.datetime.now().strftime("%B %d, %Y")  
             print(f"The date is {date_with_month}.")
             speak(f"The date is {date_with_month}.")
        
        elif 'time' in query:
             time_now = datetime.datetime.now().strftime("%H:%M:%S")
             print(f"The time is {time_now}")
             speak(f"The time is {time_now}.")

        elif 'shutdown' in query:
            speak("Hold On a Sec! Your system is on its way to shut down")
            os.system('sudo shutdown now')

        elif "restart" in query:
            speak('Restarting system...')
            os.system("sudo reboot now")

        elif "clear log" in query:
            speak("Clearing your log files")
            os.system('sudo rm -rf /kali/var/log')

        elif 'file' in query:
            speak("File manager will open shortly. Please wait...")
            os.system('nautilus')
            
        elif 'email' in query:
            try:
                speak("What should I say?")
                content = input("Compose your email: ")
                to = input("Receiver email address: ")
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'search' in query:
            search_url = web_search(query)  
            if search_url:
                speak('Opening a web browser for your search...')
                webbrowser.open(search_url)
            else:
                speak('Search failed. Please try again.')

        elif 'ai' in query:
            speak("Hello, you are with Lexi Chatbot")
            while True:
                speak("Please enter your prompt")
                prompt = listen().lower()
                if prompt == "exit":
                    break
                generated_code = generate_code(prompt)
        
                print(f"Prompt: {prompt}")
                print(f"\nLexi AI:\n{generated_code}")
                speak(generated_code)
        
        elif query:
            speak(f"Opening {query}...")
            os.system(query)

        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")
