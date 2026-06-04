import pygame
import os     # Padroniza caminhos de arquivos p/ que o jogo rode em qualquer computador sem dar erro de 'Pasta não encontrada'
import sys    # Biblioteca usada para fechar a janela do jogo
import time   # Para rastreamento de tempo de partida
import webbrowser  # Biblioteca para abrir URLs no navegador padrão
import src.logic.logic as logic  # Importa a ponte de lógica que criamos
from src.ui.som import *   # Importa a ponte de som que criamos
from src.logic.pontuacao import GerenciadorPontuacao 
from src.ui.cores import * # Para organizar a interface
from src.ui.menus import exibir_menu_principal, exibir_game_over, exibir_video_intro, obter_botao_clicado, escala_tela
from src.ui.tela_jogo import exibir_gameplay, escalonar_animacao
from src.content.easter_eggs import *

# ===== IMPORTS DAS 11 FEATURES =====
from src.logic.dificuldade import GerenciadorDificuldade, NivelDificuldade
from src.logic.achievements import GerenciadorAchievements
from src.logic.historico import GerenciadorHistorico
from src.logic.controles import MapeadorControles
from src.logic.powerups import GerenciadorPowerups, TipoPowerup
from src.logic.animacoes import GeradorParticulas, AnimadorTransicao
from src.ui.tutorial import GerenciadorTutorial
from src.logic.niveis import GerenciadorNiveis
from src.ui import som
# ===== FIM DOS IMPORTS =====

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FONTE = os.path.join(BASE_DIR, "assets", "fonts", "PressStart2P-Regular.ttf")

pygame.init()

try:
    pygame.mixer.init()
    print("Som iniciado")
except pygame.error:
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    pygame.mixer.init()
    print("Sem dispositivo de áudio")

iniciar_sons()

# Tela e FPS
largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("! IndexError - A Tupã Production")
relogio = pygame.time.Clock() # Controla a velocidade do jogo

# Inicializa os botões após o display
from src.ui import botoes
botoes.inicializar_botoes()

imagem_fundo_og = pygame.image.load("assets/images/img_menu.png").convert()
imagem_fundo = pygame.transform.smoothscale(imagem_fundo_og, (largura, altura))

imagem_gameplay_og = pygame.image.load("assets/images/img_gameplay.png").convert()
imagem_gameplay = pygame.transform.smoothscale(imagem_gameplay_og, (largura, altura))

imagem_loop_1 = pygame.image.load("assets/images/canoa_1.png").convert_alpha()
imagem_loop_2 = pygame.image.load("assets/images/canoa_2.png").convert_alpha()
animacao_perso = escalonar_animacao([imagem_loop_1, imagem_loop_2], largura, altura)

deslocamento_x = 0
deslocamento_y = 0
alvo_x = 0
alvo_y = 0
suavidade_ida = 0.15 # Controla a velocidade da ida
suavidade_volta = 0.07 # Controla a velocidade da volta para o centro

# Fontes 
fonte_Grande = pygame.font.Font(CAMINHO_FONTE, 35)
fonte_Media = pygame.font.Font(CAMINHO_FONTE, 20)
fonte_Pequena = pygame.font.Font(CAMINHO_FONTE, 15)

fontes_jogo = {
    'grande': fonte_Grande,
    'media': fonte_Media,
    'pequena': fonte_Pequena
}

# Possíveis estados do jogo
intro, menu, jogando, GAME_OVER, REGISTRANDO, OPCOES, TUTORIAL, PAUSADO, MENU_DIFICULDADE, TELA_HISTORICO, TELA_CONQUISTAS, TELA_CONTROLES, TELA_DESAFIO, TIME_ATTACK, MULTIPLAYER = (
    'INTRO','MENU', 'JOGANDO', 'GAME_OVER', 'REGISTRANDO', 'OPCOES',
    'TUTORIAL', 'PAUSADO', 'MENU_DIFICULDADE',
    'TELA_HISTORICO', 'TELA_CONQUISTAS', 'TELA_CONTROLES', 'TELA_DESAFIO', 'TIME_ATTACK', 'MULTIPLAYER'
)

nome_input = "" # Variável para guardar as 3 letras que o jogador vai digitar
estado_Atual = intro #Estado Inicial do jogo
opcao_menu= 0
opcao_opcoes = 0  # 0 = Resolução, 1 = Música, 2 = Som de Efeitos, 3 = Controles, 4 = Histórico, 5 = Conquistas, 6 = Desafio Diário
opcao_pausa = 0  # Menu de pausa
opcao_dificuldade = 0  # Menu de dificuldade
indice_resolucao = 3  # Começa em FULLSCREEN

# Variáveis do modo Time Attack
time_attack_tempo_total = 60.0  # 60 segundos
time_attack_acertos = 0
time_attack_desafios_completados = 0

# Variáveis do Tutorial In-Game
tutorial_in_game_ativo = False
tutorial_passo_atual = 0
tutorial_mensagem = ""
tutorial_mensagem_visivel = ""
tutorial_mostrar = False

# Variáveis de paginação
pagina_conquistas = 0
pagina_desafios = 0
tutorial_letra_atual = 0
tutorial_tempo_ultima_letra = 0

# Variáveis do Menu de Seleção de Tutorial
tutorial_opcao_selecionada = 0  # 0 = In-Game, 1 = Web

# Variáveis de feedback visual de powerups
powerup_feedback_ativo = False
powerup_feedback_texto = ""
powerup_feedback_tempo_inicio = 0
powerup_feedback_duracao = 2.0

# Variáveis para efeitos de powerups
multiplicador_congelado = False
multiplicador_congelado_tempo_inicio = 0
multiplicador_congelado_duracao = 30.0

pontos = 0
desafio = None # A variavel precisa existir, por isso 'None' que vai ser substituido depois

# ===== INICIALIZAÇÃO DAS 11 FEATURES =====
sistema_pontos = GerenciadorPontuacao()
gerenciador_dificuldade = GerenciadorDificuldade(NivelDificuldade.NORMAL)
gerenciador_achievements = GerenciadorAchievements()
gerenciador_historico = GerenciadorHistorico()
mapeador_controles = MapeadorControles()
gerenciador_powerups = GerenciadorPowerups()
gerador_particulas = GeradorParticulas()
animador_transicao = AnimadorTransicao()
gerenciador_tutorial = GerenciadorTutorial()
gerenciador_niveis = GerenciadorNiveis()

# Rastreamento de tempo e estatísticas
tempo_partida_inicio = 0
tempo_total_partida = 0.0
# ===== FIM INICIALIZAÇÃO =====
tempo_restante = 0

# ===== VARIÁVEIS ADICIONAIS PARA FEATURES =====
multiplicador_powerup_ativo = 1.0  # Multiplicador de powerup (x2)
escudo_ativo = False  # Se o jogador tem escudo ativo
opcoes_removidas = []  # Opções erradas removidas pelo powerup
ultimo_uso_powerup = 0  # Timestamp do último uso de powerup (para limitar spam)
cooldown_powerup = 1.0  # Cooldown em segundos entre usos

# Sistema de Popup de Conquistas (estilo Xbox)
popup_conquista_ativo = False
popup_conquista_texto = ""
popup_conquista_tempo_inicio = 0
popup_conquista_duracao = 3.0  # Duração em segundos

# Sistema de Popup de Powerup
popup_powerup_ativo = False
popup_powerup_texto = ""
popup_powerup_tempo_inicio = 0
popup_powerup_duracao = 2.0  # Duração em segundos

# Sistema de Intro Melhorada
intro_animacao_ativa = True
intro_tempo_inicio = time.time()
intro_fase = 0  # 0 = fade in logo, 1 = texto aparecendo, 2 = transição para menu
intro_alpha = 0
intro_texto_visivel = ""
intro_letra_atual = 0
# ===== FIM VARIÁVEIS ADICIONAIS =====



resolucoes = [ 
    (800, 600),
    (1280, 720),
    (1920, 1080),
    "FULLSCREEN" 
]

def aplicar_resolucao(opcao):
    global tela, largura, altura, imagem_fundo, imagem_gameplay, animacao_perso

    if opcao == "FULLSCREEN":
        tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        largura, altura = tela.get_size()
    else:
        largura, altura = opcao
        tela = pygame.display.set_mode((largura, altura))
    
    imagem_fundo = escala_tela(imagem_fundo_og, tela)
    imagem_gameplay = escala_tela(imagem_gameplay_og, tela)
    animacao_perso = escalonar_animacao([imagem_loop_1, imagem_loop_2], largura, altura)

def aplicar_efeito_powerup(tipo_powerup):
    """
    Aplica o efeito de um powerup ao jogo.

    Args:
        tipo_powerup: Tipo do powerup a ser aplicado
    """
    global multiplicador_powerup_ativo, escudo_ativo, tempo_restante
    global powerup_feedback_ativo, powerup_feedback_texto, powerup_feedback_tempo_inicio
    global multiplicador_congelado, multiplicador_congelado_tempo_inicio
    global opcoes_removidas

    if tipo_powerup == TipoPowerup.TEMPO_EXTRA:
        # Adiciona 5 segundos ao tempo
        tempo_restante += 5.0
        gerador_particulas.criar_explosao(largura // 2, altura // 2, (0, 255, 100), 30)
        powerup_feedback_texto = "+5 SEGUNDOS!"
    elif tipo_powerup == TipoPowerup.CONGELAR_MULTIPLICADOR:
        # Congela o multiplicador por 30s
        multiplicador_congelado = True
        multiplicador_congelado_tempo_inicio = time.time()
        gerador_particulas.criar_explosao(largura // 2, altura // 2, (0, 150, 255), 30)
        powerup_feedback_texto = "MULTIPLICADOR CONGELADO!"
    elif tipo_powerup == TipoPowerup.REMOVER_OPCAO:
        # Remove 1 opção errada
        if desafio and "opcoes" in desafio:
            opcoes = desafio["opcoes"]
            corretas = desafio["corretas"]
            # Encontrar uma opção errada e remover
            for opcao in opcoes[:]:
                if opcao not in corretas:
                    opcoes.remove(opcao)
                    opcoes_removidas.append(opcao)
                    gerador_particulas.criar_explosao(largura // 2, altura // 2, (255, 200, 0), 30)
                    powerup_feedback_texto = "OPÇÃO REMOVIDA!"
                    break
    elif tipo_powerup == TipoPowerup.ESCUDO:
        # Ativa escudo
        escudo_ativo = True
        gerador_particulas.criar_explosao(largura // 2, altura // 2, (255, 100, 200), 30)
        powerup_feedback_texto = "ESCUDO ATIVO!"
    elif tipo_powerup == TipoPowerup.MULTIPLICADOR_DOBRADO:
        # Dobra o multiplicador por 15s
        multiplicador_powerup_ativo = 2.0
        gerador_particulas.criar_explosao(largura // 2, altura // 2, (255, 100, 100), 30)
        powerup_feedback_texto = "MULTIPLICADOR x2!"

    # Ativar feedback visual
    powerup_feedback_ativo = True
    powerup_feedback_tempo_inicio = time.time()

def mostrar_popup_conquista(nome_conquista):
    """
    Mostra um popup de conquista estilo Xbox.

    Args:
        nome_conquista: Nome da conquista desbloqueada
    """
    global popup_conquista_ativo, popup_conquista_texto, popup_conquista_tempo_inicio
    popup_conquista_ativo = True
    popup_conquista_texto = nome_conquista
    popup_conquista_tempo_inicio = time.time()
    # Tocar som de conquista (se existir)
    tocar_botao()  # Usando som de botão temporariamente

def mostrar_popup_powerup(tipo_powerup):
    """
    Mostra um popup de powerup.

    Args:
        tipo_powerup: Tipo do powerup obtido
    """
    global popup_powerup_ativo, popup_powerup_texto, popup_powerup_tempo_inicio
    nomes_powerups = {
        TipoPowerup.TEMPO_EXTRA: "TEMPO EXTRA +5s",
        TipoPowerup.CONGELAR_MULTIPLICADOR: "MULTIPLICADOR CONGELADO",
        TipoPowerup.REMOVER_OPCAO: "OPCAO REMOVIDA",
        TipoPowerup.ESCUDO: "ESCUDO ATIVADO",
        TipoPowerup.MULTIPLICADOR_DOBRADO: "MULTIPLICADOR x2"
    }
    popup_powerup_ativo = True
    popup_powerup_texto = nomes_powerups.get(tipo_powerup, "POWERUP")
    popup_powerup_tempo_inicio = time.time()
    tocar_botao()

def atualizar_intro():
    """
    Atualiza a animação da intro melhorada.
    """
    global intro_animacao_ativa, intro_tempo_inicio, intro_fase, intro_alpha, intro_texto_visivel, intro_letra_atual, estado_Atual

    if not intro_animacao_ativa:
        return

    tempo_atual = time.time()
    tempo_decorrido = tempo_atual - intro_tempo_inicio

    if intro_fase == 0:
        # Fade in do logo
        if tempo_decorrido < 2.0:
            intro_alpha = int((tempo_decorrido / 2.0) * 255)
        else:
            intro_alpha = 255
            intro_fase = 1
            intro_tempo_inicio = tempo_atual
    elif intro_fase == 1:
        # Texto aparecendo letra por letra
        texto_completo = "! INDEXERROR"
        if tempo_decorrido < 0.05:  # Velocidade de cada letra
            pass
        else:
            intro_letra_atual = int(tempo_decorrido / 0.05)
            if intro_letra_atual >= len(texto_completo):
                intro_texto_visivel = texto_completo
                if tempo_decorrido > 3.0:
                    intro_fase = 2
                    intro_tempo_inicio = tempo_atual
            else:
                intro_texto_visivel = texto_completo[:intro_letra_atual]
    elif intro_fase == 2:
        # Transição para o menu
        if tempo_decorrido > 1.0:
            intro_animacao_ativa = False
            estado_Atual = menu
            tocar_menu()

def iniciar_tutorial_in_game():
    """
    Inicia o tutorial interativo in-game.
    """
    global tutorial_in_game_ativo, tutorial_passo_atual, tutorial_mensagem, tutorial_mensagem_visivel, tutorial_mostrar, tutorial_letra_atual, tutorial_tempo_ultima_letra
    tutorial_in_game_ativo = True
    tutorial_passo_atual = 0
    tutorial_mensagem = "Bem-vindo ao tutorial! Use as setas para mover o personagem."
    tutorial_mensagem_visivel = ""
    tutorial_mostrar = True
    tutorial_letra_atual = 0
    tutorial_tempo_ultima_letra = time.time()

def avancar_tutorial():
    """
    Avança para o próximo passo do tutorial.
    """
    global tutorial_passo_atual, tutorial_mensagem, tutorial_mensagem_visivel, tutorial_letra_atual, tutorial_tempo_ultima_letra, tutorial_in_game_ativo

    passos_tutorial = [
        "Bem-vindo ao tutorial! Use as setas para mover o personagem.",
        "Pressione a seta correspondente à direção correta.",
        "Acertos aumentam seu combo e pontuação.",
        "Erros perdem vidas. Você tem 3 vidas.",
        "Powerups aparecem aleatoriamente. Use teclas 1, 2, 3.",
        "Pressione ESC para pausar o jogo.",
        "Tutorial concluído! Pressione ESPAÇO para continuar."
    ]

    tutorial_passo_atual += 1
    if tutorial_passo_atual < len(passos_tutorial):
        tutorial_mensagem = passos_tutorial[tutorial_passo_atual]
        tutorial_mensagem_visivel = ""
        tutorial_letra_atual = 0
        tutorial_tempo_ultima_letra = time.time()
    else:
        tutorial_mensagem = ""
        tutorial_mensagem_visivel = ""
        tutorial_mostrar = False
        tutorial_in_game_ativo = False  # Encerra o tutorial completamente

def atualizar_tutorial():
    """
    Atualiza o texto do tutorial aparecendo letra por letra automaticamente.
    """
    global tutorial_mensagem_visivel, tutorial_letra_atual, tutorial_tempo_ultima_letra

    if not tutorial_mostrar or not tutorial_in_game_ativo:
        return

    tempo_atual = time.time()
    if tempo_atual - tutorial_tempo_ultima_letra >= 0.05:  # Velocidade de cada letra
        if tutorial_letra_atual < len(tutorial_mensagem):
            tutorial_mensagem_visivel = tutorial_mensagem[:tutorial_letra_atual + 1]
            tutorial_letra_atual += 1
            tutorial_tempo_ultima_letra = tempo_atual

def desenhar_texto(texto, cor, y_offset, fonte_base, max_largura=750):
    tamanho_atual = fonte_base.get_height()
    nova_fonte = fonte_base

    while nova_fonte.size(texto)[0] > max_largura and tamanho_atual > 10:
        tamanho_atual -= 2
        nova_fonte = pygame.font.Font(CAMINHO_FONTE, tamanho_atual)

    surface = nova_fonte.render(texto, True, cor)
    rect = surface.get_rect(center=(largura // 2, altura // 2 + y_offset))
    tela.blit(surface, rect)

CONFIG_EASTER_EGGS = [
    {"palavra": "jequiti", "img": "assets/images/unicornio.png", "som": None},
    {"palavra": "caneta",   "img": "assets/images/manoel.png",     "som" : tocar_manoel},
    {"palavra": "mide",   "img": "assets/images/lobo.png",     "som": tocar_mide},
    {"palavra": "cinema",  "img": "assets/images/cinema.png",    "som": None},
    {"palavra": "zap",  "img": "assets/images/zap.png",    "som": tocar_zap},
]

gerenciador_eggs = GerenciadorEasterEggs()
for dados in CONFIG_EASTER_EGGS:
    gerenciador_eggs.adicionar(
        EasterEggTeclado(dados["palavra"], dados["img"], dados["som"]))

while True:
    if estado_Atual == intro:
        # Tocar música própria da intro
        if som.musica_ativada:
            som.tocar_intro()

        # Atualizar animação da intro
        if intro_animacao_ativa:
            atualizar_intro()

        # Renderizar intro melhorada
        tela.fill(PRETO)

        # Criar surface com alpha para fade effect
        intro_surface = pygame.Surface((largura, altura), pygame.SRCALPHA)

        # Desenhar logo com alpha
        logo_cor = (255, 255, 255, intro_alpha)
        fonte_logo = pygame.font.Font(CAMINHO_FONTE, 80)
        texto_logo = fonte_logo.render("TupãStudios", True, logo_cor[:3])
        texto_logo.set_alpha(intro_alpha)
        logo_rect = texto_logo.get_rect(center=(largura // 2, altura // 2 - 100))
        intro_surface.blit(texto_logo, logo_rect)

        # Desenhar texto aparecendo letra por letra
        if intro_fase >= 1:
            fonte_texto = pygame.font.Font(CAMINHO_FONTE, 60)
            texto_render = fonte_texto.render(intro_texto_visivel, True, (255, 200, 100))
            texto_rect = texto_render.get_rect(center=(largura // 2, altura // 2 + 50))
            intro_surface.blit(texto_render, texto_rect)

        # Adicionar partículas no fundo
        if intro_fase >= 0:
            for i in range(20):
                x = (time.time() * 50 + i * 100) % largura
                y = (time.time() * 30 + i * 50) % altura
                tamanho = 3 + (time.time() + i) % 5
                pygame.draw.circle(intro_surface, (100, 200, 255, 150), (int(x), int(y)), int(tamanho))

        tela.blit(intro_surface, (0, 0))

        # Permitir pular intro com ESPAÇO
        for evento_intro in pygame.event.get():
            if evento_intro.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento_intro.type == pygame.KEYDOWN and evento_intro.key == pygame.K_SPACE:
                intro_animacao_ativa = False
                estado_Atual = menu
                tocar_menu()

        pygame.display.flip()
        relogio.tick(60)
        continue
    # Logica do movimento do barco
    # Faz o deslocamento atual chegar perto do alvo (Movimento de IDA)
    deslocamento_x += (alvo_x - deslocamento_x) * suavidade_ida
    deslocamento_y += (alvo_y - deslocamento_y) * suavidade_ida

    # Faz o alvo ser puxado de volta para o centro constantemente (Movimento de VOLTA)
    alvo_x += (0 - alvo_x) * suavidade_volta
    alvo_y += (0 - alvo_y) * suavidade_volta

    # Limpeza para evitar que o computador fique calculando números infinitesimais
    if abs(deslocamento_x) < 0.1: deslocamento_x = 0
    if abs(deslocamento_y) < 0.1: deslocamento_y = 0

    # ==== Desenha a imagem de Fundo ========
    tela.blit(imagem_fundo,(0,0))

    gameplay_musica_tocando = False

    if estado_Atual == jogando or estado_Atual == TIME_ATTACK:
        if not gameplay_musica_tocando:
            tocar_gameplay()
            gameplay_musica_tocando = True

    musica_menu_tocando = False
    if estado_Atual == menu:
        if not musica_menu_tocando:
            tocar_menu()
            musica_menu_tocando = True

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        gerenciador_eggs.processar_eventos(evento)

        # MENU
        if estado_Atual == menu:
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    tocar_botao()
                    opcao_menu = (opcao_menu - 1) % 5 # 5 botoes (Play, Time Attack, Tutorial, Config, Sair)

                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    opcao_menu = (opcao_menu + 1) % 5
                    tocar_botao()

                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER: # Navegação no menu usando as setinhas

                    if opcao_menu == 0:  # primeiro botao - Play
                        tocar_botao()
                        # Feature: Sistema de Dificuldade - Mostrar menu de seleção antes de jogar
                        estado_Atual = MENU_DIFICULDADE
                        opcao_dificuldade = 1  # Começa em NORMAL
                    elif opcao_menu == 1:  # segundo botao - Tutorial (texto)
                        tocar_botao()
                        # Mostrar submenu de tutorial (In-Game vs Web)
                        estado_Atual = TUTORIAL
                        tutorial_opcao_selecionada = 0
                    elif opcao_menu == 2:  # terceiro botao - Time Attack (texto)
                        tocar_botao()
                        # Iniciar modo Time Attack
                        time_attack_tempo_total = 60.0
                        time_attack_acertos = 0
                        time_attack_desafios_completados = 0
                        sistema_pontos.resetar_partida()
                        desafio = logic.obter_novo_desafio(0)
                        tempo_restante = time_attack_tempo_total
                        deslocamento_y = 0
                        deslocamento_x = 0
                        tempo_partida_inicio = time.time()
                        estado_Atual = TIME_ATTACK
                        parar_menu()
                    elif opcao_menu == 3:  # quarto botao - Config
                        tocar_botao()
                        estado_Atual = OPCOES
                    elif opcao_menu == 4:  # quinto botao - Quit
                        tocar_botao()
                        pygame.quit()
                        sys.exit()

        # MENU DE SELEÇÃO DE TUTORIAL
        elif estado_Atual == TUTORIAL:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    tocar_botao()
                    tutorial_opcao_selecionada = (tutorial_opcao_selecionada - 1) % 2
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    tocar_botao()
                    tutorial_opcao_selecionada = (tutorial_opcao_selecionada + 1) % 2
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    tocar_botao()
                    if tutorial_opcao_selecionada == 0:  # Tutorial In-Game
                        iniciar_tutorial_in_game()
                        sistema_pontos.resetar_partida()
                        desafio = logic.obter_novo_desafio(0)
                        tempo_restante = 999999  # Sem limite de tempo no tutorial
                        deslocamento_y = 0
                        deslocamento_x = 0
                        tempo_partida_inicio = time.time()
                        estado_Atual = jogando
                        parar_menu()
                    elif tutorial_opcao_selecionada == 1:  # Tutorial Web
                        webbrowser.open("https://index-error-web.vercel.app/")
                elif evento.key == pygame.K_ESCAPE:
                    estado_Atual = menu
                # Se o mouse estiver sobre um botão, a mãozinha pula para ele
            elif evento.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                acao = obter_botao_clicado(pos, tela)
                opcao_anterior = opcao_menu

            
                if acao == "play":                   
                    opcao_menu = 0                  
                elif acao == "tutorial":
                    opcao_menu = 1
                elif acao == "time_attack":
                    opcao_menu = 2
                elif acao == "config":
                    opcao_menu = 3
                elif acao == "quit":
                    opcao_menu = 4      

                if opcao_menu != opcao_anterior:
                 tocar_botao()


            elif evento.type == pygame.MOUSEBUTTONDOWN: # Navegação no menu usando o mouse
                pos = pygame.mouse.get_pos()
                acao = obter_botao_clicado(pos,tela)
                if acao == "play":
                    tocar_botao()
                    sistema_pontos.resetar_partida()
                    desafio = logic.obter_novo_desafio(sistema_pontos.combo)
                    tempo_restante = sistema_pontos.calcular_tempo_limite()
                    estado_Atual = jogando
                    deslocamento_y = 0
                    deslocamento_x = 0
                elif acao == "tutorial":
                    tocar_botao()
                    # Mostrar submenu de tutorial (In-Game vs Web)
                    estado_Atual = TUTORIAL
                    tutorial_opcao_selecionada = 0
                elif acao == "time_attack":
                    tocar_botao()
                    # Iniciar Time Attack
                    sistema_pontos.resetar_partida()
                    time_attack_tempo_total = 60.0
                    time_attack_acertos = 0
                    time_attack_desafios_completados = 0
                    tempo_restante = time_attack_tempo_total
                    desafio = logic.obter_novo_desafio(0)
                    estado_Atual = TIME_ATTACK
                    deslocamento_y = 0
                    deslocamento_x = 0
                    tempo_partida_inicio = time.time()
                    parar_menu()
                elif acao == "config":
                    tocar_botao()
                    estado_Atual = OPCOES
                elif acao == "quit":
                    tocar_botao()
                    pygame.quit()
                    sys.exit()

        elif estado_Atual == OPCOES:
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    tocar_botao()
                    opcao_opcoes = (opcao_opcoes - 1) % 7  # 7 opções: Resolução, Música, Som, Controles, Histórico, Conquistas, Desafio

                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    tocar_botao()
                    opcao_opcoes = (opcao_opcoes + 1) % 7

                elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    tocar_botao()
                    if opcao_opcoes == 0:  # Resolução
                        indice_resolucao = (indice_resolucao - 1) % len(resolucoes)
                        aplicar_resolucao(resolucoes[indice_resolucao])
                    elif opcao_opcoes == 1:  # Música
                        som.alternar_musica()
                    elif opcao_opcoes == 2:  # Som de Efeitos
                        som.alternar_som_efeitos()

                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    tocar_botao()
                    if opcao_opcoes == 0:  # Resolução
                        indice_resolucao = (indice_resolucao + 1) % len(resolucoes)
                        aplicar_resolucao(resolucoes[indice_resolucao])
                    elif opcao_opcoes == 1:  # Música
                        som.alternar_musica()
                    elif opcao_opcoes == 2:  # Som de Efeitos
                        som.alternar_som_efeitos()

                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    tocar_botao()
                    if opcao_opcoes == 3:  # Controles
                        estado_Atual = TELA_CONTROLES
                    elif opcao_opcoes == 4:  # Histórico
                        estado_Atual = TELA_HISTORICO
                    elif opcao_opcoes == 5:  # Conquistas
                        estado_Atual = TELA_CONQUISTAS
                    elif opcao_opcoes == 6:  # Desafio Diário
                        estado_Atual = TELA_DESAFIO

                elif evento.key == pygame.K_ESCAPE:
                    tocar_botao()
                    estado_Atual = menu

        # TELA HISTÓRICO (Feature: Histórico de Partidas)
        elif estado_Atual == TELA_HISTORICO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    tocar_botao()
                    estado_Atual = OPCOES

        # TELA CONQUISTAS (Feature: Sistema de Achievements)
        elif estado_Atual == TELA_CONQUISTAS:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    tocar_botao()
                    estado_Atual = OPCOES
                # Navegação de páginas
                elif evento.key == pygame.K_a:
                    conquistas = list(gerenciador_achievements.achievements.values())
                    conquistas_por_pagina = 8
                    total_paginas = (len(conquistas) + conquistas_por_pagina - 1) // conquistas_por_pagina
                    if pagina_conquistas > 0:
                        pagina_conquistas -= 1
                        tocar_botao()
                elif evento.key == pygame.K_d:
                    conquistas = list(gerenciador_achievements.achievements.values())
                    conquistas_por_pagina = 8
                    total_paginas = (len(conquistas) + conquistas_por_pagina - 1) // conquistas_por_pagina
                    if pagina_conquistas < total_paginas - 1:
                        pagina_conquistas += 1
                        tocar_botao()

        # TELA CONTROLES (Feature: Teclado Customizável)
        elif estado_Atual == TELA_CONTROLES:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    tocar_botao()
                    estado_Atual = OPCOES

        # TELA DESAFIO (Feature: Desafios Diários)
        elif estado_Atual == TELA_DESAFIO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    tocar_botao()
                    estado_Atual = OPCOES
                # Navegação de páginas
                elif evento.key == pygame.K_a:
                    desafios_por_pagina = 5
                    total_paginas_desafios = (len(desafios_hoje) + desafios_por_pagina - 1) // desafios_por_pagina
                    if pagina_desafios > 0:
                        pagina_desafios -= 1
                        tocar_botao()
                elif evento.key == pygame.K_d:
                    desafios_por_pagina = 5
                    total_paginas_desafios = (len(desafios_hoje) + desafios_por_pagina - 1) // desafios_por_pagina
                    if pagina_desafios < total_paginas_desafios - 1:
                        pagina_desafios += 1
                        tocar_botao()

        # MENU DE DIFICULDADE (Feature: Sistema de Dificuldade)
        elif estado_Atual == MENU_DIFICULDADE:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    opcao_dificuldade = (opcao_dificuldade - 1) % 3
                    tocar_botao()
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    opcao_dificuldade = (opcao_dificuldade + 1) % 3
                    tocar_botao()
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    # Feature: Aplicar dificuldade selecionada e iniciar jogo
                    dificuldades = [NivelDificuldade.FACIL, NivelDificuldade.NORMAL, NivelDificuldade.DIFICIL]
                    nomes_dificuldade = ["FACIL", "NORMAL", "DIFICIL"]
                    gerenciador_dificuldade.definir_dificuldade(dificuldades[opcao_dificuldade])
                    config_dif = gerenciador_dificuldade.obter_config()
                    sistema_pontos.resetar_partida(config_dif.__dict__, nomes_dificuldade[opcao_dificuldade])
                    
                    # Feature: Resetar variáveis de powerups
                    multiplicador_powerup_ativo = 1.0
                    escudo_ativo = False
                    opcoes_removidas = []
                    gerenciador_powerups.limpar_powerups()
                    
                    desafio = logic.obter_novo_desafio(sistema_pontos.combo)
                    tempo_restante = sistema_pontos.calcular_tempo_limite()
                    deslocamento_y = 0
                    deslocamento_x = 0
                    
                    # Feature: Rastrear tempo de início
                    tempo_partida_inicio = time.time()
                    
                    # Feature: Verificar desafio diário
                    sistema_pontos.verificar_desafio_diario()
                    
                    # Feature: Iniciar transição
                    animador_transicao.iniciar("fade")
                    
                    tocar_botao()
                    estado_Atual = jogando
                    parar_menu()
                elif evento.key == pygame.K_ESCAPE:
                    tocar_botao()
                    estado_Atual = menu

        # TUTORIAL (Feature: Tutorial Interativo)
        elif estado_Atual == TUTORIAL:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if not gerenciador_tutorial.proximo_passo():
                        tocar_botao()
                        estado_Atual = menu
                    else:
                        tocar_botao()
                elif evento.key == pygame.K_ESCAPE:
                    gerenciador_tutorial.pular_tutorial()
                    tocar_botao()
                    estado_Atual = menu

        # PAUSA (Feature: Pausa no Jogo)
        elif estado_Atual == PAUSADO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    opcao_pausa = (opcao_pausa - 1) % 2
                    tocar_botao()
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    opcao_pausa = (opcao_pausa + 1) % 2
                    tocar_botao()
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    if opcao_pausa == 0:  # Retomar
                        tocar_botao()
                        estado_Atual = jogando
                    else:  # Sair para menu
                        tocar_botao()
                        parar_gameplay()
                        estado_Atual = menu
                        # Encerrar tutorial se estiver ativo
                        if tutorial_in_game_ativo:
                            tutorial_in_game_ativo = False
                            tutorial_mostrar = False
                elif evento.key == pygame.K_ESCAPE:
                    tocar_botao()
                    estado_Atual = jogando

        # JOGO
        elif estado_Atual == jogando:
            if evento.type == pygame.KEYDOWN:
                # Feature: Teclado Customizável - Usar mapeador ao invés de verificar direto
                acao = mapeador_controles.verificar_acao(evento.key)
                escolha = None
                
                if acao == "CIMA":
                    escolha = "CIMA"
                    alvo_y = -300
                elif acao == "BAIXO":
                    escolha = "BAIXO"
                    alvo_y = 300  
                elif acao == "ESQUERDA":
                    escolha = "ESQUERDA"
                    alvo_x = -350
                elif acao == "DIREITA":
                    escolha = "DIREITA"
                    alvo_x = 350
                elif acao == "PAUSAR":
                    # Feature: Pausa no Jogo
                    estado_Atual = PAUSADO
                    opcao_pausa = 0
                    tocar_botao()

                # Pausa direta com ESC (garantir que funcione)
                elif evento.key == pygame.K_ESCAPE:
                    estado_Atual = PAUSADO
                    opcao_pausa = 0
                    tocar_botao()

                # Feature: Powerups - Teclas para usar powerups (com cooldown)
                elif evento.key == pygame.K_1:
                    # Verificar cooldown e se tem powerups
                    if time.time() - ultimo_uso_powerup >= cooldown_powerup and gerenciador_powerups.obter_quantidade() > 0:
                        # Usar primeiro powerup
                        powerup = gerenciador_powerups.usar_powerup(0, time.time())
                        if powerup:
                            aplicar_efeito_powerup(powerup.tipo)
                            gerenciador_powerups.remover_powerup(0)
                            ultimo_uso_powerup = time.time()
                elif evento.key == pygame.K_2:
                    # Verificar cooldown e se tem powerups
                    if time.time() - ultimo_uso_powerup >= cooldown_powerup and gerenciador_powerups.obter_quantidade() > 1:
                        # Usar segundo powerup
                        powerup = gerenciador_powerups.usar_powerup(1, time.time())
                        if powerup:
                            aplicar_efeito_powerup(powerup.tipo)
                            gerenciador_powerups.remover_powerup(1)
                            ultimo_uso_powerup = time.time()
                elif evento.key == pygame.K_3:
                    # Verificar cooldown e se tem powerups
                    if time.time() - ultimo_uso_powerup >= cooldown_powerup and gerenciador_powerups.obter_quantidade() > 2:
                        # Usar terceiro powerup
                        powerup = gerenciador_powerups.usar_powerup(2, time.time())
                        if powerup:
                            aplicar_efeito_powerup(powerup.tipo)
                            gerenciador_powerups.remover_powerup(2)
                            ultimo_uso_powerup = time.time()

                # Tutorial In-Game - Avançar com ESPAÇO
                elif evento.key == pygame.K_SPACE and tutorial_in_game_ativo:
                    avancar_tutorial()
                
                if escolha:
                    if logic.validar_jogada(escolha, desafio["corretas"]):
                        tocar_acerto()
                        # Feature: Sistema de Dificuldade + Pontuação
                        config_dif = gerenciador_dificuldade.obter_config()
                        sistema_pontos.registrar_acerto(multiplicador_powerup_ativo)
                        
                        # Feature: Sistema de Combo Visual - Efeitos visuais ao aumentar combo
                        if sistema_pontos.combo % 5 == 0:  # A cada 5 de combo
                            # Partículas coloridas baseadas no combo
                            cor_combo = min(255, sistema_pontos.combo * 5)
                            gerador_particulas.criar_explosao(largura // 2, altura // 2, (cor_combo, 255 - cor_combo // 2, 100), 20)
                        
                        # Feature: Sistema de Níveis - Adicionar XP
                        xp_ganho = int(10 * sistema_pontos.multiplicador)
                        if gerenciador_niveis.adicionar_xp(xp_ganho):
                            mostrar_popup_conquista(f"SUBIU PARA NÍVEL {gerenciador_niveis.nivel}!")
                        
                        # Feature: Achievements - Verificar conquistas (expandido)
                        if sistema_pontos.combo == 500:
                            if gerenciador_achievements.desbloquear("combo_500"):
                                mostrar_popup_conquista("COMBO 500!")
                        if sistema_pontos.combo == 1000:
                            if gerenciador_achievements.desbloquear("combo_1000"):
                                mostrar_popup_conquista("COMBO 1000!")
                        if sistema_pontos.acertos_totais == 20:
                            if gerenciador_achievements.desbloquear("20_acertos"):
                                mostrar_popup_conquista("20 ACERTOS!")
                        if sistema_pontos.acertos_totais == 50:
                            if gerenciador_achievements.desbloquear("50_acertos"):
                                mostrar_popup_conquista("50 ACERTOS!")
                        if sistema_pontos.acertos_totais == 10 and sistema_pontos.erros_totais == 0:
                            if gerenciador_achievements.desbloquear("sem_erros_10"):
                                mostrar_popup_conquista("SEM ERROS 10!")
                        if sistema_pontos.score > sistema_pontos.high_score:
                            if gerenciador_achievements.desbloquear("recordista"):
                                mostrar_popup_conquista("RECORDISTA!")
                        
                        # Feature: Powerups - Chance de aparecer powerup
                        if gerenciador_powerups.deveria_aparecer_powerup():
                            tipo_powerup = gerenciador_powerups.gerar_powerup_aleatorio()
                            gerenciador_powerups.adicionar_powerup(tipo_powerup)
                            mostrar_popup_powerup(tipo_powerup)
                        
                        # Feature: Animações - Criar efeito de acerto
                        gerador_particulas.criar_trail(largura // 2, altura // 2, (0, 255, 100), 10)
                        
                        desafio = logic.obter_novo_desafio(sistema_pontos.combo)
                        tempo_restante = sistema_pontos.calcular_tempo_limite()
                    else:
                        # Feature: Sistema de Vidas + Escudo
                        if escudo_ativo:
                            # Escudo protege de 1 erro
                            escudo_ativo = False
                            gerador_particulas.criar_explosao(largura // 2, altura // 2, (255, 100, 200), 15)
                        else:
                            sistema_pontos.registrar_erro()
                            gerador_particulas.criar_explosao(largura // 2, altura // 2, (255, 50, 50), 20)
                        
                        if sistema_pontos.perdeu_todas_vidas():
                            # Feature: Histórico + Desafio Diário
                            tempo_total_partida = time.time() - tempo_partida_inicio
                            gerenciador_historico.registrar_partida(
                                score=sistema_pontos.score,
                                combo_maximo=sistema_pontos.combo,
                                dificuldade=gerenciador_dificuldade.obter_nome(),
                                duracao=tempo_total_partida,
                                acertos=sistema_pontos.acertos_totais,
                                erros=sistema_pontos.erros_totais
                            )
                            
                            # Feature: Achievements - Verificar conquistas de fim de partida
                            if sistema_pontos.score > 0:
                                if gerenciador_achievements.desbloquear("5_partidas"):
                                    mostrar_popup_conquista("5 PARTIDAS!")
                            if gerenciador_historico.obter_estatisticas_gerais().get("total_partidas", 0) >= 50:
                                if gerenciador_achievements.desbloquear("50_partidas"):
                                    mostrar_popup_conquista("50 PARTIDAS!")

                            # Feature: Desafio Diário - Completar se atingir meta
                            if sistema_pontos.score >= 1000 and not sistema_pontos.desafio_diario_completado:
                                sistema_pontos.completar_desafio_diario()
                                if gerenciador_achievements.desbloquear("velocista"):
                                    mostrar_popup_conquista("VELOCISTA!")

                            if sistema_pontos.verificar_novo_recorde():
                                if gerenciador_achievements.desbloquear("primeiro_recorde"):
                                    mostrar_popup_conquista("PRIMEIRO RECORDE!")
                                estado_Atual = REGISTRANDO
                            else:
                                estado_Atual = GAME_OVER
                            tocar_erro()
                            parar_gameplay()
                            gerenciador_powerups.limpar_powerups()

         # GAME OVER
        elif estado_Atual == GAME_OVER:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:    
                    sistema_pontos.resetar_partida()
                    desafio = logic.obter_novo_desafio(sistema_pontos.combo)
                    tempo_restante = sistema_pontos.calcular_tempo_limite()
                    estado_Atual = jogando
                    deslocamento_y = 0
                    deslocamento_x = 0

                elif evento.key == pygame.K_ESCAPE:
                    estado_Atual = menu
                    parar_erro()

        # REGISTRO
        elif estado_Atual == REGISTRANDO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    if len(nome_input) == 3:
                        sistema_pontos.salvar_no_ranking(nome_input)
                        nome_input = ""
                        estado_Atual = GAME_OVER
                        

                elif evento.key == pygame.K_BACKSPACE:
                    nome_input = nome_input[:-1]

                elif len(nome_input) < 3:
                    if evento.unicode.isalpha():
                        nome_input += evento.unicode.upper()

        # TIME ATTACK
        elif estado_Atual == TIME_ATTACK:
            if evento.type == pygame.KEYDOWN:
                acao = mapeador_controles.verificar_acao(evento.key)
                escolha = None

                if acao == "CIMA":
                    escolha = "CIMA"
                    alvo_y = -300
                elif acao == "BAIXO":
                    escolha = "BAIXO"
                    alvo_y = 300
                elif acao == "ESQUERDA":
                    escolha = "ESQUERDA"
                    alvo_x = -350
                elif acao == "DIREITA":
                    escolha = "DIREITA"
                    alvo_x = 350
                elif acao == "PAUSAR":
                    estado_Atual = PAUSADO
                    opcao_pausa = 0
                    tocar_botao()

                # Pausa no Time Attack também
                elif evento.key == pygame.K_ESCAPE:
                    estado_Atual = PAUSADO
                    opcao_pausa = 0
                    tocar_botao()

                if escolha:
                    if logic.validar_jogada(escolha, desafio["corretas"]):
                        tocar_acerto()
                        time_attack_acertos += 1
                        time_attack_desafios_completados += 1
                        sistema_pontos.registrar_acerto(multiplicador_powerup_ativo)
                        gerador_particulas.criar_trail(largura // 2, altura // 2, (0, 255, 100), 10)
                        desafio = logic.obter_novo_desafio(time_attack_acertos)
                    else:
                        time_attack_acertos = 0  # Reseta combo no Time Attack
                        sistema_pontos.score = 0  # Reseta pontos ao errar
                        sistema_pontos.combo = 0
                        gerador_particulas.criar_explosao(largura // 2, altura // 2, (255, 50, 50), 20)
                        desafio = logic.obter_novo_desafio(time_attack_acertos)

                # Powerups no Time Attack
                elif evento.key == pygame.K_1:
                    if time.time() - ultimo_uso_powerup >= cooldown_powerup and gerenciador_powerups.obter_quantidade() > 0:
                        powerup = gerenciador_powerups.usar_powerup(0, time.time())
                        if powerup:
                            aplicar_efeito_powerup(powerup.tipo)
                            gerenciador_powerups.remover_powerup(0)
                            ultimo_uso_powerup = time.time()

    # Lógica de retorno da imagem
    # Faz a imagem voltar suavemente para o centro (0, 0) a cada frame

    if estado_Atual == jogando or estado_Atual == TIME_ATTACK:

        # --- Lógica de Retorno da Imagem ---
        velocidade_retorno = 4.5
        
        if abs(deslocamento_x) < velocidade_retorno:
            deslocamento_x = 0
        elif deslocamento_x > 0:
            deslocamento_x -= velocidade_retorno
        elif deslocamento_x < 0:
            deslocamento_x += velocidade_retorno
            
        if abs(deslocamento_y) < velocidade_retorno:
            deslocamento_y = 0
        elif deslocamento_y > 0:
            deslocamento_y -= velocidade_retorno
        elif deslocamento_y < 0:
            deslocamento_y += velocidade_retorno

    # CRONÔMETRO
    if estado_Atual == jogando or estado_Atual == TIME_ATTACK:
        # Não diminuir tempo se estiver no tutorial
        if not tutorial_in_game_ativo:
            tempo_restante -= relogio.get_time() / 1000.0

        # Game Over no Time Attack quando tempo acaba
        if estado_Atual == TIME_ATTACK and tempo_restante <= 0:
            estado_Atual = GAME_OVER
            tocar_erro()

    # Verificar se multiplicador congelado expirou
    if multiplicador_congelado:
        if time.time() - multiplicador_congelado_tempo_inicio >= multiplicador_congelado_duracao:
            multiplicador_congelado = False

    # Atualizar tutorial in-game
    if estado_Atual == jogando:
        atualizar_tutorial()

        if tempo_restante <= 0:
            # Feature: Histórico
            tempo_total_partida = time.time() - tempo_partida_inicio
            gerenciador_historico.registrar_partida(
                score=sistema_pontos.score,
                combo_maximo=sistema_pontos.combo,
                dificuldade=gerenciador_dificuldade.obter_nome(),
                duracao=tempo_total_partida,
                acertos=sistema_pontos.acertos_totais,
                erros=sistema_pontos.erros_totais
            )
            
            if sistema_pontos.verificar_novo_recorde():
                estado_Atual = REGISTRANDO
            else:
                estado_Atual = GAME_OVER
                tocar_erro()

    # RENDER
    if estado_Atual == menu:
        exibir_menu_principal(tela, desenhar_texto, fontes_jogo, opcao_menu)

    elif estado_Atual == TUTORIAL:
        # Renderizar menu de seleção de tutorial
        tela.fill(PRETO)
        desenhar_texto("ESCOLHA O TUTORIAL", BRANCO, -200, fontes_jogo['grande'])

        opcoes_tutorial = ["TUTORIAL IN-GAME", "TUTORIAL WEB"]
        for i, opcao in enumerate(opcoes_tutorial):
            cor = AMARELO if i == tutorial_opcao_selecionada else BRANCO
            pos_y = -50 + (i * 80)
            desenhar_texto(f"[{opcao}]", cor, pos_y, fontes_jogo['media'])

        desenhar_texto("Pressione ESC para voltar", CINZA_CLARO, 200, fontes_jogo['pequena'])

    elif estado_Atual == jogando:
        exibir_gameplay(tela, desenhar_texto, fontes_jogo, desafio, sistema_pontos, tempo_restante, imagem_gameplay, animacao_perso, (deslocamento_x, deslocamento_y), opcoes_removidas, gerenciador_niveis.nivel, gerenciador_niveis.obter_percentual_nivel())

        # HUD com fundo para melhor visibilidade
        hud_x = 20
        hud_y = 20
        hud_largura = 300
        hud_altura = 180

        pygame.draw.rect(tela, (0, 0, 0, 180), (hud_x, hud_y, hud_largura, hud_altura))
        pygame.draw.rect(tela, (100, 100, 255), (hud_x, hud_y, hud_largura, hud_altura), 2)

        # Feature: Mostrar vidas
        vidas_cor = VERDE_VIBRANTE if sistema_pontos.obter_vidas() > 1 else VERMELHO_VIVO
        fonte_hud = pygame.font.Font(CAMINHO_FONTE, 16)
        texto_vidas = fonte_hud.render(f"VIDAS: {sistema_pontos.obter_vidas()}", True, vidas_cor)
        tela.blit(texto_vidas, (hud_x + 10, hud_y + 10))

        # Feature: Sistema de Níveis - Mostrar nível
        texto_nivel = fonte_hud.render(f"NÍVEL: {gerenciador_niveis.nivel}", True, (255, 215, 0))
        tela.blit(texto_nivel, (hud_x + 10, hud_y + 30))

        # Barra de XP
        largura_barra_xp = hud_largura - 20
        altura_barra_xp = 5
        x_barra_xp = hud_x + 10
        y_barra_xp = hud_y + 50
        percentual_xp = gerenciador_niveis.obter_percentual_nivel()
        pygame.draw.rect(tela, (50, 50, 50), (x_barra_xp, y_barra_xp, largura_barra_xp, altura_barra_xp))
        pygame.draw.rect(tela, (255, 215, 0), (x_barra_xp, y_barra_xp, int(largura_barra_xp * percentual_xp / 100), altura_barra_xp))

        # Mostrar score
        texto_score = fonte_hud.render(f"SCORE: {sistema_pontos.score}", True, AMARELO)
        tela.blit(texto_score, (hud_x + 10, hud_y + 60))

        # Mostrar combo
        texto_combo = fonte_hud.render(f"COMBO: {sistema_pontos.combo}", True, (255, 100, 200))
        tela.blit(texto_combo, (hud_x + 10, hud_y + 80))

        # Mostrar tempo apenas se não for tutorial
        if not tutorial_in_game_ativo:
            texto_tempo = fonte_hud.render(f"TEMPO: {tempo_restante:.1f}s", True, (100, 200, 255))
            tela.blit(texto_tempo, (hud_x + 10, hud_y + 100))

        # Powerups disponíveis
        powerups_disponiveis = gerenciador_powerups.obter_quantidade()
        if powerups_disponiveis > 0:
            texto_powerups = fonte_hud.render(f"POWERUPS: {powerups_disponiveis}", True, (255, 150, 50))
            if tutorial_in_game_ativo:
                tela.blit(texto_powerups, (hud_x + 10, hud_y + 100))
            else:
                tela.blit(texto_powerups, (hud_x + 10, hud_y + 120))

            # Mostrar powerups específicos disponíveis
            fonte_desc = pygame.font.Font(CAMINHO_FONTE, 11)
            powerups_lista = gerenciador_powerups.obter_powerups_ativos()
            y_offset = 135 if not tutorial_in_game_ativo else 115
            for i, powerup in enumerate(powerups_lista[:3]):  # Mostrar até 3 powerups
                info = gerenciador_powerups.obter_info_powerup(powerup.tipo)
                nome = info.get("nome", "Powerup")
                tecla = i + 1
                texto = f"{tecla}: {nome}"
                cor = info.get("cor", (200, 200, 200))
                desc_texto = fonte_desc.render(texto, True, cor)
                tela.blit(desc_texto, (hud_x + 10, hud_y + y_offset))
                y_offset += 13

        # Feedback visual de powerup
        if powerup_feedback_ativo:
            tempo_decorrido = time.time() - powerup_feedback_tempo_inicio
            if tempo_decorrido >= powerup_feedback_duracao:
                powerup_feedback_ativo = False
            else:
                # Desenhar feedback no centro da tela
                fonte_feedback = pygame.font.Font(CAMINHO_FONTE, 32)
                texto_feedback = fonte_feedback.render(powerup_feedback_texto, True, (255, 255, 100))
                feedback_rect = texto_feedback.get_rect(center=(largura // 2, altura // 2 - 100))
                tela.blit(texto_feedback, feedback_rect)

        # Tutorial In-Game - Mostrar mensagem
        if tutorial_mostrar and tutorial_in_game_ativo:
            # Desenhar caixa do tutorial com design melhorado
            largura_tutorial = 1300
            altura_tutorial = 100
            x_tutorial = largura // 2 - largura_tutorial // 2
            y_tutorial = altura - 120

            # Fundo com gradiente simulado
            pygame.draw.rect(tela, (20, 30, 60), (x_tutorial, y_tutorial, largura_tutorial, altura_tutorial))
            pygame.draw.rect(tela, (50, 100, 200), (x_tutorial, y_tutorial, largura_tutorial, altura_tutorial), 3)
            pygame.draw.rect(tela, (100, 150, 255), (x_tutorial + 5, y_tutorial + 5, largura_tutorial - 10, altura_tutorial - 10), 1)

            # Texto do tutorial com efeito de digitação
            fonte_tutorial = pygame.font.Font(CAMINHO_FONTE, 18)
            texto_tutorial = fonte_tutorial.render(tutorial_mensagem_visivel, True, (255, 255, 255))
            tela.blit(texto_tutorial, (x_tutorial + 25, y_tutorial + 20))

            # Instruções
            fonte_instrucao = pygame.font.Font(CAMINHO_FONTE, 14)
            texto_instrucao = fonte_instrucao.render("Pressione ESPAÇO para pular", True, (150, 200, 255))
            tela.blit(texto_instrucao, (x_tutorial + 25, y_tutorial + 70))

    elif estado_Atual == TIME_ATTACK:
        exibir_gameplay(tela, desenhar_texto, fontes_jogo, desafio, sistema_pontos, tempo_restante, imagem_gameplay, animacao_perso, (deslocamento_x, deslocamento_y), opcoes_removidas, gerenciador_niveis.nivel, gerenciador_niveis.obter_percentual_nivel())

        # HUD do Time Attack com fundo
        hud_x = 20
        hud_y = 20
        hud_largura = 300
        hud_altura = 180

        pygame.draw.rect(tela, (0, 0, 0, 180), (hud_x, hud_y, hud_largura, hud_altura))
        pygame.draw.rect(tela, (255, 50, 50), (hud_x, hud_y, hud_largura, hud_altura), 2)

        fonte_hud = pygame.font.Font(CAMINHO_FONTE, 16)

        # Título
        texto_titulo = fonte_hud.render("TIME ATTACK", True, VERMELHO_VIVO)
        tela.blit(texto_titulo, (hud_x + 10, hud_y + 10))

        # Desafios
        texto_desafios = fonte_hud.render(f"DESAFIOS: {time_attack_desafios_completados}", True, AMARELO)
        tela.blit(texto_desafios, (hud_x + 10, hud_y + 35))

        # Combo
        texto_combo = fonte_hud.render(f"COMBO: {time_attack_acertos}", True, (100, 200, 255))
        tela.blit(texto_combo, (hud_x + 10, hud_y + 60))

        # Score
        texto_score = fonte_hud.render(f"SCORE: {sistema_pontos.score}", True, (255, 100, 200))
        tela.blit(texto_score, (hud_x + 10, hud_y + 85))

        # Tempo
        texto_tempo = fonte_hud.render(f"TEMPO: {tempo_restante:.1f}s", True, (100, 255, 100))
        tela.blit(texto_tempo, (hud_x + 10, hud_y + 110))

        # Powerups disponíveis
        powerups_disponiveis = gerenciador_powerups.obter_quantidade()
        if powerups_disponiveis > 0:
            texto_powerups = fonte_hud.render(f"POWERUPS: {powerups_disponiveis}", True, (255, 150, 50))
            tela.blit(texto_powerups, (hud_x + 10, hud_y + 135))

            # Mostrar powerups específicos disponíveis
            fonte_desc = pygame.font.Font(CAMINHO_FONTE, 11)
            powerups_lista = gerenciador_powerups.obter_powerups_ativos()
            y_offset = 150
            for i, powerup in enumerate(powerups_lista[:3]):  # Mostrar até 3 powerups
                info = gerenciador_powerups.obter_info_powerup(powerup.tipo)
                nome = info.get("nome", "Powerup")
                tecla = i + 1
                texto = f"{tecla}: {nome}"
                cor = info.get("cor", (200, 200, 200))
                desc_texto = fonte_desc.render(texto, True, cor)
                tela.blit(desc_texto, (hud_x + 10, hud_y + y_offset))
                y_offset += 13

        # Feedback visual de powerup
        if powerup_feedback_ativo:
            tempo_decorrido = time.time() - powerup_feedback_tempo_inicio
            if tempo_decorrido >= powerup_feedback_duracao:
                powerup_feedback_ativo = False
            else:
                # Desenhar feedback no centro da tela
                fonte_feedback = pygame.font.Font(CAMINHO_FONTE, 32)
                texto_feedback = fonte_feedback.render(powerup_feedback_texto, True, (255, 255, 100))
                feedback_rect = texto_feedback.get_rect(center=(largura // 2, altura // 2 - 100))
                tela.blit(texto_feedback, feedback_rect)
        
        # Feature: Animações - Desenhar partículas
        gerador_particulas.atualizar()
        gerador_particulas.desenhar(tela)
        
        # Feature: Animações - Desenhar transição se ativa
        if animador_transicao.esta_ativa():
            animador_transicao.atualizar()
            animador_transicao.desenhar_overlay_fade(tela)

    elif estado_Atual == PAUSADO:
        # Feature: Pausa - Renderizar menu
        from src.ui.pausa import exibir_menu_pausa
        exibir_menu_pausa(tela, desenhar_texto, fontes_jogo, opcao_pausa)

    elif estado_Atual == OPCOES:
        from src.ui.menus import exibir_opcoes
        exibir_opcoes(tela, desenhar_texto, fontes_jogo, opcao_opcoes, resolucoes, indice_resolucao, som.musica_ativada, som.som_efeitos_ativado)

    elif estado_Atual == MENU_DIFICULDADE:
        # Feature: Menu de Dificuldade
        tela.fill(PRETO)
        desenhar_texto("SELECIONE DIFICULDADE", BRANCO, -150, fontes_jogo['grande'])

        dificuldades = ["FÁCIL", "NORMAL", "DIFÍCIL"]
        for i, dif in enumerate(dificuldades):
            cor = AMARELO if i == opcao_dificuldade else BRANCO
            pos_y = -50 + (i * 80)
            desenhar_texto(dif, cor, pos_y, fontes_jogo['media'])

    elif estado_Atual == TELA_HISTORICO:
        # Feature: Tela de Histórico de Partidas
        tela.fill(PRETO)
        desenhar_texto("HISTÓRICO DE PARTIDAS", BRANCO, -250, fontes_jogo['grande'])

        try:
            stats = gerenciador_historico.obter_estatisticas_gerais()
            if stats is None:
                stats = {}
            total_partidas = stats.get('total_partidas', 0) if stats else 0
            score_medio = stats.get('score_medio', 0) if stats else 0
            melhor_score = stats.get('melhor_score', 0) if stats else 0

            desenhar_texto(f"Total de Partidas: {total_partidas}", BRANCO, -150, fontes_jogo['media'])
            desenhar_texto(f"Score Médio: {score_medio:.1f}", BRANCO, -100, fontes_jogo['media'])
            desenhar_texto(f"Melhor Score: {melhor_score}", BRANCO, -50, fontes_jogo['media'])

            desenhar_texto("ÚLTIMAS 5 PARTIDAS:", AMARELO, 20, fontes_jogo['media'])
            try:
                historico = gerenciador_historico.obter_ultimas(5)
                if historico is None:
                    historico = []
                y_pos = 70
                for partida in historico:
                    timestamp = partida.timestamp if hasattr(partida, 'timestamp') else ''
                    score = partida.score if hasattr(partida, 'score') else 0
                    combo = partida.combo_maximo if hasattr(partida, 'combo_maximo') else 0
                    texto = f"{timestamp[:10] if timestamp else 'N/A'} - Score: {score} - Combo: {combo}"
                    desenhar_texto(texto, CINZA_CLARO, y_pos, fontes_jogo['pequena'])
                    y_pos += 30
            except:
                desenhar_texto("Nenhuma partida registrada", CINZA, 70, fontes_jogo['media'])
        except Exception as e:
            desenhar_texto("Erro ao carregar histórico", VERMELHO_VIVO, 0, fontes_jogo['media'])

        desenhar_texto("Pressione ESC para voltar", CINZA, 280, fontes_jogo['pequena'])

    elif estado_Atual == TELA_CONQUISTAS:
        # Feature: Tela de Conquistas
        tela.fill((15, 15, 40))  # Fundo azul escuro mais claro
        desenhar_texto("CONQUISTAS", DOURADO, -300, fontes_jogo['grande'])

        total_desbloqueadas = gerenciador_achievements.obter_total_desbloqueadas()
        percentual = gerenciador_achievements.obter_percentual_desbloqueio()

        # Barra de progresso
        largura_barra = 500
        altura_barra = 25
        x_barra = largura // 2 - largura_barra // 2
        y_barra = altura // 2 - 200
        pygame.draw.rect(tela, (30, 30, 50), (x_barra, y_barra, largura_barra, altura_barra))
        pygame.draw.rect(tela, VERDE_VIBRANTE, (x_barra, y_barra, int(largura_barra * percentual / 100), altura_barra))
        pygame.draw.rect(tela, DOURADO, (x_barra, y_barra, largura_barra, altura_barra), 3)

        desenhar_texto(f"Desbloqueadas: {total_desbloqueadas} ({percentual:.1f}%)", VERDE_VIBRANTE, -160, fontes_jogo['media'])

        # Mostrar conquistas com paginação
        conquistas = list(gerenciador_achievements.achievements.values())
        fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 12)
        
        # Variáveis de paginação
        conquistas_por_pagina = 8
        total_paginas = (len(conquistas) + conquistas_por_pagina - 1) // conquistas_por_pagina
        
        # Calcular índice inicial e final
        inicio = pagina_conquistas * conquistas_por_pagina
        fim = min(inicio + conquistas_por_pagina, len(conquistas))
        
        # Calcular altura total para centralizar
        altura_total_conquistas = (fim - inicio) * 25
        y_inicio = -altura_total_conquistas // 2
        
        for i in range(inicio, fim):
            conquista = conquistas[i]
            cor_texto = DOURADO if conquista.desbloqueada else CINZA
            texto = f"{'★' if conquista.desbloqueada else ' '} {conquista.nome}"
            
            texto_surface = fonte_pequena.render(texto, True, cor_texto)
            texto_rect = texto_surface.get_rect(center=(largura // 2, altura // 2 + y_inicio))
            tela.blit(texto_surface, texto_rect)
            
            y_inicio += 25
        
        # Mostrar indicador de página
        if total_paginas > 1:
            texto_pagina = fonte_pequena.render(f"Página {pagina_conquistas + 1}/{total_paginas}", True, (200, 200, 200))
            tela.blit(texto_pagina, (largura // 2 - texto_pagina.get_width() // 2, altura // 2 + y_inicio + 10))
            
            # Instruções de navegação
            if pagina_conquistas > 0:
                texto_anterior = fonte_pequena.render("← Anterior (A)", True, (150, 150, 150))
                tela.blit(texto_anterior, (largura // 2 - 150, altura // 2 + y_inicio + 30))
            if pagina_conquistas < total_paginas - 1:
                texto_proximo = fonte_pequena.render("Próximo (D) →", True, (150, 150, 150))
                tela.blit(texto_proximo, (largura // 2 + 50, altura // 2 + y_inicio + 30))

        desenhar_texto("Pressione ESC para voltar", CINZA_CLARO, 300, fontes_jogo['pequena'])

    elif estado_Atual == TELA_CONTROLES:
        # Feature: Tela de Controles Customizáveis
        tela.fill(PRETO)
        desenhar_texto("CONTROLES CUSTOMIZÁVEIS", BRANCO, -250, fontes_jogo['grande'])

        desenhar_texto("CIMA: Seta Cima ou W", BRANCO, -150, fontes_jogo['media'])
        desenhar_texto("BAIXO: Seta Baixo ou S", BRANCO, -100, fontes_jogo['media'])
        desenhar_texto("ESQUERDA: Seta Esquerda ou A", BRANCO, -50, fontes_jogo['media'])
        desenhar_texto("DIREITA: Seta Direita ou D", BRANCO, 0, fontes_jogo['media'])
        desenhar_texto("PAUSAR: ESC", BRANCO, 50, fontes_jogo['media'])
        desenhar_texto("POWERUP 1: Tecla 1", BRANCO, 100, fontes_jogo['media'])
        desenhar_texto("POWERUP 2: Tecla 2", BRANCO, 150, fontes_jogo['media'])
        desenhar_texto("POWERUP 3: Tecla 3", BRANCO, 200, fontes_jogo['media'])

        desenhar_texto("Pressione ESC para voltar", CINZA, 280, fontes_jogo['pequena'])

    elif estado_Atual == TELA_DESAFIO:
        # Feature: Tela de Desafios Diários (Infinitos, resetam diariamente)
        tela.fill((15, 15, 35))  # Fundo azul escuro
        desenhar_texto("DESAFIOS DIÁRIOS", DOURADO, -280, fontes_jogo['grande'])

        # Gerar desafios baseados na data atual
        from datetime import datetime
        hoje = datetime.now()
        dia_do_ano = hoje.timetuple().tm_yday

        # Lista de desafios possíveis com descrições detalhadas
        desafios_possiveis = [
            {"meta": 500, "nome": "500 Pontos", "descricao": "Alcançar 500 pontos em uma partida", "recompensa": "100 XP", "tipo": "pontos"},
            {"meta": 1000, "nome": "1000 Pontos", "descricao": "Alcançar 1000 pontos em uma partida", "recompensa": "200 XP", "tipo": "pontos"},
            {"meta": 2000, "nome": "2000 Pontos", "descricao": "Alcançar 2000 pontos em uma partida", "recompensa": "400 XP", "tipo": "pontos"},
            {"meta": 3000, "nome": "3000 Pontos", "descricao": "Alcançar 3000 pontos em uma partida", "recompensa": "600 XP", "tipo": "pontos"},
            {"meta": 5000, "nome": "5000 Pontos", "descricao": "Alcançar 5000 pontos em uma partida", "recompensa": "1000 XP", "tipo": "pontos"},
            {"meta": 10000, "nome": "10000 Pontos", "descricao": "Alcançar 10000 pontos em uma partida", "recompensa": "2000 XP", "tipo": "pontos"},
            {"meta": 100, "nome": "Combo 100", "descricao": "Alcançar 100 de combo em uma partida", "recompensa": "Conquista 'Combo Iniciante'", "tipo": "combo"},
            {"meta": 500, "nome": "Combo 500", "descricao": "Alcançar 500 de combo em uma partida", "recompensa": "Conquista 'Combo Mestre'", "tipo": "combo"},
            {"meta": 1000, "nome": "Combo 1000", "descricao": "Alcançar 1000 de combo em uma partida", "recompensa": "Conquista 'Combo Supremo'", "tipo": "combo"},
            {"meta": 10, "nome": "10 Acertos Sem Erros", "descricao": "Acertar 10 desafios consecutivos sem errar", "recompensa": "Conquista 'Precisão'", "tipo": "acertos_sem_erro"},
            {"meta": 20, "nome": "20 Acertos Sem Erros", "descricao": "Acertar 20 desafios consecutivos sem errar", "recompensa": "Conquista 'Perfeição'", "tipo": "acertos_sem_erro"},
            {"meta": 50, "nome": "50 Acertos Totais", "descricao": "Acertar 50 desafios no total", "recompensa": "Conquista 'Veterano'", "tipo": "acertos_totais"},
            {"meta": 100, "nome": "100 Acertos Totais", "descricao": "Acertar 100 desafios no total", "recompensa": "Conquista 'Mestre Absoluto'", "tipo": "acertos_totais"},
            {"meta": 5, "nome": "5 Partidas Jogadas", "descricao": "Completar 5 partidas", "recompensa": "Conquista 'Gamer Casual'", "tipo": "partidas"},
            {"meta": 10, "nome": "10 Partidas Jogadas", "descricao": "Completar 10 partidas", "recompensa": "Conquista 'Gamer Regular'", "tipo": "partidas"},
            {"meta": 50, "nome": "50 Partidas Jogadas", "descricao": "Completar 50 partidas", "recompensa": "Conquista 'Gamer Dedicado'", "tipo": "partidas"},
            {"meta": 100, "nome": "100 Partidas Jogadas", "descricao": "Completar 100 partidas", "recompensa": "Conquista 'Gamer Veterano'", "tipo": "partidas"},
            {"meta": 30, "nome": "30 Desafios Time Attack", "descricao": "Completar 30 desafios no modo Time Attack", "recompensa": "Conquista 'Time Attack Iniciante'", "tipo": "time_attack"},
            {"meta": 50, "nome": "50 Desafios Time Attack", "descricao": "Completar 50 desafios no modo Time Attack", "recompensa": "Conquista 'Time Attack Mestre'", "tipo": "time_attack"},
            {"meta": 5, "nome": "Usar 5 Powerups", "descricao": "Usar 5 powerups durante partidas", "recompensa": "Conquista 'Coletor Iniciante'", "tipo": "powerups"},
            {"meta": 10, "nome": "Usar 10 Powerups", "descricao": "Usar 10 powerups durante partidas", "recompensa": "Conquista 'Coletor'", "tipo": "powerups"},
            {"meta": 25, "nome": "Usar 25 Powerups", "descricao": "Usar 25 powerups durante partidas", "recompensa": "Conquista 'Mestre dos Powerups'", "tipo": "powerups"},
        ]

        # Selecionar 5 desafios baseados no dia do ano (rotação infinita)
        desafios_hoje = []
        for i in range(5):
            indice = (dia_do_ano + i * 7) % len(desafios_possiveis)  # Pula 7 para mais variedade
            desafios_hoje.append(desafios_possiveis[indice])

        # Verificar progresso de cada desafio
        try:
            stats = gerenciador_historico.obter_estatisticas_gerais()
            total_partidas = stats.get("total_partidas", 0) if stats else 0
        except:
            total_partidas = 0

        conquistas_desbloqueadas = gerenciador_achievements.obter_desbloqueadas()
        conquistas_ids = [c.id for c in conquistas_desbloqueadas]

        # Mostrar data atual
        data_formatada = hoje.strftime("%d/%m/%Y")
        desenhar_texto(f"Data: {data_formatada}", CINZA_CLARO, -200, fontes_jogo['pequena'])

        # Paginação dos desafios
        desafios_por_pagina = 5
        total_paginas_desafios = (len(desafios_hoje) + desafios_por_pagina - 1) // desafios_por_pagina
        
        inicio_desafios = pagina_desafios * desafios_por_pagina
        fim_desafios = min(inicio_desafios + desafios_por_pagina, len(desafios_hoje))

        # Calcular altura total para centralizar
        altura_total_desafios = (fim_desafios - inicio_desafios) * 30
        y_pos = -altura_total_desafios // 2
        
        for i in range(inicio_desafios, fim_desafios):
            desafio = desafios_hoje[i]
            # Verificar se o desafio está completo
            completo = False
            progresso_atual = 0

            if desafio["tipo"] == "pontos":
                progresso_atual = sistema_pontos.score
                completo = sistema_pontos.score >= desafio["meta"]
            elif desafio["tipo"] == "combo":
                progresso_atual = sistema_pontos.combo
                completo = sistema_pontos.combo >= desafio["meta"]
            elif desafio["tipo"] == "acertos_sem_erro":
                progresso_atual = sistema_pontos.acertos_totais if sistema_pontos.erros_totais == 0 else 0
                completo = desafio["meta"] <= progresso_atual
            elif desafio["tipo"] == "acertos_totais":
                progresso_atual = sistema_pontos.acertos_totais
                completo = sistema_pontos.acertos_totais >= desafio["meta"]
            elif desafio["tipo"] == "partidas":
                progresso_atual = total_partidas
                completo = total_partidas >= desafio["meta"]
            elif desafio["tipo"] == "time_attack":
                progresso_atual = time_attack_desafios_completados
                completo = time_attack_desafios_completados >= desafio["meta"]
            elif desafio["tipo"] == "powerups":
                progresso_atual = gerenciador_powerups.total_usado
                completo = gerenciador_powerups.total_usado >= desafio["meta"]

            # Texto do desafio (simples)
            fonte_desafio = pygame.font.Font(CAMINHO_FONTE, 14)
            cor_texto = VERDE_VIBRANTE if completo else BRANCO
            texto = f"{i + 1}. {desafio['nome']} - Progresso: {progresso_atual}/{desafio['meta']}"
            texto_surface = fonte_desafio.render(texto, True, cor_texto)
            texto_rect = texto_surface.get_rect(center=(largura // 2, altura // 2 + y_pos))
            tela.blit(texto_surface, texto_rect)

            y_pos += 30

        # Mostrar indicador de página dos desafios
        if total_paginas_desafios > 1:
            fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 12)
            texto_pagina = fonte_pequena.render(f"Página {pagina_desafios + 1}/{total_paginas_desafios}", True, (200, 200, 200))
            tela.blit(texto_pagina, (largura // 2 - texto_pagina.get_width() // 2, altura // 2 + y_pos + 10))
            
            # Instruções de navegação
            if pagina_desafios > 0:
                texto_anterior = fonte_pequena.render("← Anterior (A)", True, (150, 150, 150))
                tela.blit(texto_anterior, (largura // 2 - 150, altura // 2 + y_pos + 30))
            if pagina_desafios < total_paginas_desafios - 1:
                texto_proximo = fonte_pequena.render("Próximo (D) →", True, (150, 150, 150))
                tela.blit(texto_proximo, (largura // 2 + 50, altura // 2 + y_pos + 30))

        desenhar_texto("Pressione ESC para voltar", CINZA_CLARO, 280, fontes_jogo['pequena'])

    elif estado_Atual == TUTORIAL:
        # Feature: Tutorial Interativo
        from src.ui.tutorial import exibir_tutorial
        exibir_tutorial(tela, desenhar_texto, fontes_jogo, gerenciador_tutorial)

    elif estado_Atual == GAME_OVER:
        exibir_game_over(tela, desenhar_texto, fontes_jogo, sistema_pontos.score, sistema_pontos.ranking, sistema_pontos.dificuldade_atual)

    elif estado_Atual == REGISTRANDO:
        from src.ui.menus import exibir_registro_recorde
        exibir_registro_recorde(tela, desenhar_texto, fontes_jogo, nome_input)
    
    gerenciador_eggs.atualizar_e_desenhar(tela)

    # Feature: Popup de Conquistas (estilo Xbox)
    if popup_conquista_ativo:
        tempo_decorrido = time.time() - popup_conquista_tempo_inicio
        if tempo_decorrido >= popup_conquista_duracao:
            popup_conquista_ativo = False
        else:
            # Desenhar popup estilo Xbox
            largura_popup = 400
            altura_popup = 60
            x_popup = largura - largura_popup - 20
            y_popup = 20

            # Fundo do popup (gradiente verde escuro)
            pygame.draw.rect(tela, (0, 50, 0), (x_popup, y_popup, largura_popup, altura_popup))
            pygame.draw.rect(tela, (0, 100, 0), (x_popup, y_popup, largura_popup, altura_popup), 2)

            # Texto "CONQUISTA DESBLOQUEADA"
            fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 14)
            texto_titulo = fonte_pequena.render("CONQUISTA DESBLOQUEADA", True, (255, 255, 255))
            tela.blit(texto_titulo, (x_popup + 10, y_popup + 5))

            # Nome da conquista
            fonte_media = pygame.font.Font(CAMINHO_FONTE, 20)
            texto_conquista = fonte_media.render(popup_conquista_texto, True, (255, 215, 0))
            tela.blit(texto_conquista, (x_popup + 10, y_popup + 30))

    # Feature: Popup de Powerup
    if popup_powerup_ativo:
        tempo_decorrido = time.time() - popup_powerup_tempo_inicio
        if tempo_decorrido >= popup_powerup_duracao:
            popup_powerup_ativo = False
        else:
            # Desenhar popup de powerup
            largura_popup = 350
            altura_popup = 50
            x_popup = largura - largura_popup - 20
            y_popup = 90

            # Fundo do popup (azul escuro)
            pygame.draw.rect(tela, (0, 0, 100), (x_popup, y_popup, largura_popup, altura_popup))
            pygame.draw.rect(tela, (0, 0, 150), (x_popup, y_popup, largura_popup, altura_popup), 2)

            # Texto "POWERUP"
            fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 12)
            texto_titulo = fonte_pequena.render("POWERUP OBTIDO", True, (255, 255, 255))
            tela.blit(texto_titulo, (x_popup + 10, y_popup + 5))

            # Nome do powerup
            fonte_media = pygame.font.Font(CAMINHO_FONTE, 18)
            texto_powerup = fonte_media.render(popup_powerup_texto, True, (0, 255, 255))
            tela.blit(texto_powerup, (x_popup + 10, y_popup + 25))


    pygame.display.flip()
    relogio.tick(60)