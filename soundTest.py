import pygame
import time

pygame.mixer.init()

sound = pygame.mixer.Sound("select.wav")
sound.play()
time.sleep(1)

lsound = pygame.mixer.Sound("left.wav")
sound.play()
time.sleep(1)

csound = pygame.mixer.Sound("center.wav")
sound.play()
time.sleep(1)

rsound = pygame.mixer.Sound("right.wav")
sound.play()
time.sleep(1)
