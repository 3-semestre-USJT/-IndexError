import pygame

som_botao = None
som_intro = None
som_acerto = None
som_erro = None
som_manoel = None
som_mide = None
som_zap = None
som_menu = None
som_gameplay = None

# Controles de áudio
musica_ativada = True
som_efeitos_ativado = True

def iniciar_sons():
    global som_botao, som_intro, som_acerto, som_erro, som_manoel, som_mide, som_zap, som_menu, som_gameplay

    try:
        som_botao = pygame.mixer.Sound("assets/sounds/botao.mp3")
        som_intro = pygame.mixer.Sound("assets/sounds/intro_som.mp3")
        som_acerto = pygame.mixer.Sound("assets/sounds/acerto.mp3")
        som_erro = pygame.mixer.Sound("assets/sounds/erro.mp3")
        som_manoel = pygame.mixer.Sound("assets/sounds/manoel.mp3")
        som_mide = pygame.mixer.Sound("assets/sounds/mide.mp3")
        som_zap = pygame.mixer.Sound("assets/sounds/zap.mp3")
        som_menu = pygame.mixer.Sound("assets/sounds/musica_menu.mp3")
        som_gameplay = pygame.mixer.Sound("assets/sounds/musica_gameplay.mp3")
    except pygame.error:
        pass

def tocar_acerto():
    if som_efeitos_ativado and som_acerto:
        som_acerto.play()

def tocar_erro():
    if som_efeitos_ativado and som_erro:
        som_erro.play()

def parar_erro():
    if som_erro:
        som_erro.stop()

def tocar_menu():
    if musica_ativada:
        pygame.mixer.Channel(0).set_volume(0.8)
        if not pygame.mixer.Channel(0).get_busy():
            pygame.mixer.Channel(0).play(som_menu, loops=-1)

def parar_menu():
     pygame.mixer.Channel(0).stop()

def tocar_intro():
    if som_efeitos_ativado and som_intro:
        som_intro.play()

def parar_intro():
    if som_intro:
        som_intro.stop()

def tocar_botao():
    if som_efeitos_ativado and som_botao:
        som_botao.play()

def tocar_manoel():
    if som_efeitos_ativado and som_manoel:
        som_manoel.play()

def tocar_mide():
    if som_efeitos_ativado and som_mide:
        som_mide.play()

def tocar_zap():
    if som_efeitos_ativado and som_zap:
        som_zap.play()

def tocar_gameplay():
    if musica_ativada:
        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(som_gameplay, loops=-1)

def parar_gameplay():
     pygame.mixer.Channel(1).stop()

def alternar_musica():
    global musica_ativada
    musica_ativada = not musica_ativada
    if not musica_ativada:
        parar_menu()
        parar_gameplay()

def alternar_som_efeitos():
    global som_efeitos_ativado
    som_efeitos_ativado = not som_efeitos_ativado