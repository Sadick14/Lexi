import subprocess
import speech_recognition as sr
import pyttsx3
import datetime
import time
import os
import webbrowser
import smtplib
import google.generativeai as genai


engine = pyttsx3.init()
engine.setProperty('rate', 150) 
engine.setProperty( 'depth', 10)
engine.setProperty('voiceselect', 'english+f2')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

def listen():
	
	r = sr.Recognizer()
	
	with sr.Microphone() as source:
		
		print("Listening...")
		r.pause_threshold = 1
		audio = r.listen(source)

	try:
		print("Recognizing...")
		query = r.recognize_google(audio, language ='en-in')
		print(f"User said: {query}\n")

	except Exception as e:
		print(e)
		print("Unable to Recognize your voice.")
		return "None"
	
	return query

def sendEmail(to, content):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	
	# Enable low security in gmail
	address= input("Enter your email address")
	password =input("Enter your email password")
	server.login(address, password)
	server.sendmail(address, to, content)
	server.close()

def web_search(query):
  search_url = f"https://www.google.com/search?q={query}"
  return search_url

def generate_code(prompt):

  # Configure API key (replace with your actual key)
  genai.configure(api_key="AIzaSyDIMekkyv2GtTbHZPDBkmE5eikl9tuy9wE")

  # Initialize the generative model
  model = genai.GenerativeModel("gemini-pro")

  # Generate content based on the prompt
  response = model.generate_content(prompt)
  generated_code = response.text

  return generated_code

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

if __name__ == "__main__":
    
    speak(f"Hello...!, 'LEXI' here! , your voice assistant. Enter 'help' in query to know how i can assist you.")

    while True:

        speak("Enter your query")
        query = input("Enter your query: ")
        #listen().lower() 
        
        

        if "exit" in query:
            speak("Goodbye! Have a great day.")
            break

        # Add more conditions based on what actions you want your assistant to perform
        elif "your name" in query:
            speak("You can call me Lexi")

        elif "who are you" in query:
            speak('I am Lexi, a voice assistance whose aim is to help you')

        elif 'help' in query:
            speak(
                'My assistance include: opening any inbuilt tool, starting services like bluetooth, making simple web searches, date and timesystem shutdown and restart. Thats all for now.'
            )


        elif "bluetooth" in query:
            os.system('systemctl start bluetooth')
            speak("Bluetooth is enabled")

        elif "play music" in query:
            speak('opening your music player')
            os.system("rhythmbox")
            

        elif 'date' in query:
             date_with_month = datetime.datetime.now().strftime("%B %d, %Y")  # Example: March 13, 2024
             print(f"The date is {date_with_month}.")
             speak(f"The date is {date_with_month}.")
        
        elif 'time' in query:
             time_now = datetime.datetime.now().strftime("%H:%M:%S")
             print(f"the time is {time_now}")
             speak(f"The time is {time_now}.")

        elif 'shutdown' in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            os.system('sudo shutdown now')

        elif "restart" in query:
            speak('restarting system.....')
            os.system("sudo reboot now")

        elif "clear log" in query:
            speak("clearing your log files")
            os.system('sudo rm -rf /kali/var/log')

        elif 'file' in query:
            speak("File manager will open shortly. Please wait...")
            os.system('nautilus')
            
        elif 'email' in query:
            try:
                speak("What should I say?")
                content = input("compose your email: ") #listen()
                to = input("Receiver email address:")
                sendEmail(to, content)
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'search' in query:
            search_url = web_search(query)  # Or use google_search(query) if using Google Custom Search Engine
            if search_url:
                speak('Opening a web browser for your search...')
                webbrowser.open(search_url)
            else:
                speak('Search failed. Please try again.')

        elif 'ai' in query:
            speak("Hello you are with Lexi Chatbot")
            while True:
                speak("please enter your prompt")
                prompt = input("Enter your prompt: ")
                generated_code = generate_code(prompt)
        
                print(f"Prompt: {prompt}")
                print(f"\nLexi Ai:\n{generated_code}")
        
        elif query:
            speak(f"Opening {query}...")
            os.system(query)


        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")


