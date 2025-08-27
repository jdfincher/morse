import pygame
import numpy as np

def play_sound(duration=0.25):
    pygame.mixer.init(frequency=44100, size=-16, channels=1)

    sample_rate = 44100
    frequency = 600.00

    time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    wave = 32767 * np.sin(2 * np.pi * frequency * time)
    wave = wave.astype(np.int16)

    sound = pygame.sndarray.make_sound(wave)
    sound.play()


    

    
    
