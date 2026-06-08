# Botões de Play, Configurações, Tutorial, Time Attack e Sair
import pygame

# Imagens dos botões (serão carregadas após inicializar o display)
botao_play = None
botao_sair = None
botao_config = None
botao_tutorial = None
botao_time_attack = None
mao_seletora = None

def inicializar_botoes():
    global botao_play, botao_sair, botao_config, botao_tutorial, botao_time_attack, mao_seletora
    botao_play = pygame.image.load("assets/images/Play_of.png").convert_alpha()
    botao_sair = pygame.image.load("assets/images/Quit_of.png").convert_alpha()
    botao_config = pygame.image.load("assets/images/Config_of.png").convert_alpha()
    botao_tutorial = pygame.image.load("assets/images/Tutorial_of.png").convert_alpha()
    botao_time_attack = pygame.image.load("assets/images/TimeAttack_of.png").convert_alpha()
    mao_seletora = pygame.image.load("assets/images/mao_seletora.png").convert_alpha()

class botao():
    def __init__(self, x,y, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect() # Pega uma retangulo da imagem para usar como hitbox
        self.rect.topleft = (x,y)

    def exibir_botao(self, tela):
        tela.blit(self.imagem, self.rect.topleft)

    def clicado(self, pos):
        return self.rect.collidepoint(pos)    