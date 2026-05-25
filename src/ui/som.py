import pygame

som_botao = None
som_intro = None
som_acerto = None
som_erro = None
som_manoel = None
som_mide = None
som_zap = None

def iniciar_sons():
    global som_botao, som_intro, som_acerto, som_erro, som_manoel, som_mide, som_zap

    try:
        som_botao = pygame.mixer.Sound("assets/sounds/botao.mp3")
        som_intro = pygame.mixer.Sound("assets/sounds/intro_som.mp3")
        som_acerto = pygame.mixer.Sound("assets/sounds/acerto.mp3")
        som_erro = pygame.mixer.Sound("assets/sounds/erro.mp3")
        som_manoel = pygame.mixer.Sound("assets/sounds/manoel.mp3")
        som_mide = pygame.mixer.Sound("assets/sounds/mide.mp3")
        som_zap = pygame.mixer.Sound("assets/sounds/zap.mp3")
    except pygame.error:
        pass

def tocar_acerto():
    if som_acerto:
        som_acerto.play()

def tocar_erro():
    if som_erro:
        som_erro.play()

def tocar_intro():
    if som_intro:
        som_intro.play()

def tocar_botao():
    if som_botao:
        som_botao.play()

def tocar_manoel():
    if som_manoel:
        som_manoel.play()

def tocar_mide():
    if som_mide:
        som_mide.play()

def tocar_zap():
    if som_zap:
        som_zap.play()