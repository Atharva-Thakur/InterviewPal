from gtts import gTTS
import pygame
import os

def createAudio(text):
    file_name = "welcome.mp3"

    myobj = gTTS(text=text, lang="en", slow=False)
    myobj.save(file_name)

    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_name)
    sound.play()

    pygame.time.wait(int(sound.get_length() * 1000))

    pygame.mixer.stop()

    os.remove(file_name)