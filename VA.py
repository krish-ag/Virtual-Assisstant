import wolframalpha # Wolfram Alpha API (THE BRAINS!!!)
import pyttsx3 # Speech Synthesis
import speech_recognition as sr 
import random 
from playsound import playsound # Media Player 

r = sr.Recognizer()
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
app_id = "Q52YQA-HQH6T3GK9J"

def main():
    with sr.Microphone() as source:
        ans = ["What's up?", "What do you need?", "What can I do for you?"] # Catalog of phrases after trigger 
        wait = ["Give me a second while I think.", "Ok thinking"] # Catalog of phrases after command
        random_ans = random.choice(ans) # Randomizes answer phrase choice
        random_wait = random.choice(wait) #  Randomizes wait phrase choice
        try:
            r.adjust_for_ambient_noise(source) # Adjusts audio input for improved speech recognition
            audio = r.listen(source) # Listens for voice
            if r.recognize_google(audio) == "hey Sarah" or "Hey sarah" or "Hey Sarah" or "hey sarah": # Trigger (What the Assistant answer to) // Also checks for trigger
                playsound('ding.mp3') 
                engine.say(random_ans)
                print("Sarah: "+random_ans)
                engine.runAndWait()
                audio = r.listen(source)
                if r.recognize_google(audio) == "nevermind":
                    print("You: "+r.recognize_google(audio))
                    engine.say("Ok Bye.")
                    print("Sarah: "+"Ok Bye.")
                    engine.runAndWait()
                    main()
                else:
                    print("You: "+r.recognize_google(audio))
                    engine.say(random_wait)
                    print("Sarah: "+random_wait)
                    engine.runAndWait()
                    client = wolframalpha.Client(app_id)
                    res = client.query(r.recognize_google(audio))
                    print("Sarah: "+next(res.results).text)
                    engine.say(next(res.results).text)
                    engine.runAndWait()
                    main()
        except sr.UnknownValueError:
            main()
main()
