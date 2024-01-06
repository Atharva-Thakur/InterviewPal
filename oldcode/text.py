import speech_recognition as sr

def getText():
    recognizer = sr.Recognizer()

    print("Speak")
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recorded_audio = recognizer.listen(source, timeout=10)
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("Done recording")
    
    text = recognizer.recognize_google(recorded_audio, language="en-US")
    
    return text

# Uncomment the following line to list available microphones
# print(sr.Microphone.list_microphone_names())