import pygame

pygame.mixer.init()

som_acerto = pygame.mixer.Sound("assets/sounds/acerto.mp3")
som_erro = pygame.mixer.Sound("assets/sounds/erro.mp3")
som_botao=pygame.mixer.Sound("assets/sounds/botao.mp3")

def tocar_acerto():
    som_acerto.play()

def tocar_erro():
    som_erro.play()

def tocar_botao():    
    som_botao.play()