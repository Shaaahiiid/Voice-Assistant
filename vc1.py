import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
from gtts import gTTS
import os
import platform
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()

def talk(text, lang='en', accent='co.uk'):
    try:
        tts = gTTS(text=text, lang=lang, tld=accent, slow=False)
        filename = "response.mp3"
        tts.save(filename)
        if platform.system() == "Windows":
            os.system(f"start {filename}")
        elif platform.system() == "Darwin":  # macOS
            os.system(f"afplay {filename}")
        else:
            os.system(f"mpg321 {filename} 2>/dev/null || cvlc --play-and-exit {filename} 2>/dev/null || aplay {filename}")
    except Exception as e:
        print("Error in TTS:", e)

def recognize_speech():
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        print('Listening...')
        text_area.insert(tk.END, 'Listening...\n')
        try:
            audio = listener.listen(source, timeout=5)
            command = listener.recognize_google(audio).lower()
            print('You said:', command)
            text_area.insert(tk.END, 'You said: ' + command + '\n')
            process_command(command)
        except sr.UnknownValueError:
            print('Sorry, could not understand audio.')
            text_area.insert(tk.END, 'Sorry, could not understand audio.\n')
            talk('Sorry, I could not understand that.')
        except sr.RequestError as e:
            print('Could not request results; {0}'.format(e))
            text_area.insert(tk.END, 'Could not request results.\n')
            talk('I am having trouble connecting to the internet.')
        except Exception as e:
            print('Error:', e)
            text_area.insert(tk.END, 'Error occurred.\n')
            talk('An error occurred while processing your request.')

def process_command(command):
    text_area.insert(tk.END, 'Processing command...\n')
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + current_time)
    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk('There are multiple results. Please be more specific.')
        except wikipedia.exceptions.PageError:
            talk('Sorry, I could not find information on that.')
    elif 'date' in command:
        talk('Sorry, I have a headache.')
    elif 'are you single' in command:
        talk('I am in a relationship with WiFi.')
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        print(joke)
    elif 'bye' in command or 'goodbye' in command:
        talk('Goodbye!')
        window.quit()
    else:
        talk('Please say the command again.')

def on_click():
    text_area.insert(tk.END, 'Button clicked...\n')
    threading.Thread(target=recognize_speech).start()

window = tk.Tk()
window.title('Voice Assistant')

text_area = scrolledtext.ScrolledText(window, width=40, height=10)
text_area.pack(padx=10, pady=10)

button = tk.Button(window, text='Start Listening', command=on_click)
button.pack(pady=5)

def test_voice():
    talk("How do i sound?")

button_test = tk.Button(window, text='Test Voice', command=test_voice)
button_test.pack(pady=5)

window.mainloop()
