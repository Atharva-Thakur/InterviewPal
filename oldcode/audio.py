import pyttsx3  

def createAudio(text):
    engine = pyttsx3.init()
    engine.say(text) 
    engine.runAndWait()