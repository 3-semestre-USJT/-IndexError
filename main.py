import pygame 
import os     # Padroniza caminhos de arquivos p/ que o jogo rode em qualquer computador sem dar erro de 'Pasta não encontrada'
import sys    # Biblioteca usada para fechar a janela do jogo
import src.logic.logic as logic  # Importa a ponte de lógica que criamos
from src.ui.som import *   # Importa a ponte de som que criamos
from src.logic.pontuacao import GerenciadorPontuacao 
from src.ui.cores import * # Para organizar a interface
from src.ui.menus import exibir_menu_principal, exibir_game_over, exibir_video_intro, obter_botao_clicado, escala_tela
from src.ui.tela_jogo import exibir_gameplay, escalonar_animacao

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FONTE = os.path.join(BASE_DIR, "assets", "fonts", "PressStart2P-Regular.ttf")

pygame.init()

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
intro, menu, jogando, GAME_OVER, REGISTRANDO, OPCOES = 'INTRO','MENU', 'JOGANDO', 'GAME_OVER', 'REGISTRANDO', 'OPCOES'

nome_input = "" # Variável para guardar as 3 letras que o jogador vai digitar
estado_Atual = intro #Estado Inicial do jogo
opcao_menu= 0
opcao_opcoes = 0
pontos = 0
desafio = None # A variavel precisa existir, por isso 'None' que vai ser substituido depois

sistema_pontos = GerenciadorPontuacao()
tempo_restante = 0



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

def desenhar_texto(texto, cor, y_offset, fonte_base, max_largura=750):
    tamanho_atual = fonte_base.get_height()
    nova_fonte = fonte_base

    while nova_fonte.size(texto)[0] > max_largura and tamanho_atual > 10:
        tamanho_atual -= 2
        nova_fonte = pygame.font.Font(CAMINHO_FONTE, tamanho_atual)

    surface = nova_fonte.render(texto, True, cor)
    rect = surface.get_rect(center=(largura // 2, altura // 2 + y_offset))
    tela.blit(surface, rect)


# Loop principal
while True:
    if estado_Atual == intro:
        canal_intro = som_intro.play()
        tocar_intro()
        deve_continuar = exibir_video_intro(tela, "assets/videos/intro_teste.mp4")
        canal_intro.stop()
        if deve_continuar:
            estado_Atual = menu
        else:
            pygame.quit()
            sys.exit()
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

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # MENU
        if estado_Atual == menu:
            
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    tocar_botao()
                    opcao_menu = (opcao_menu - 1) % 3 # 3 pois são 3 botoes

                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s: # Adicionei o DOWN para você conseguir navegar pela setinha tbm
                    opcao_menu = (opcao_menu + 1) % 3
                    tocar_botao()

                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER: # Navegação no menu usando as setinhas
                
                    if opcao_menu == 0:  # primeiro botao
                        tocar_botao()
                        sistema_pontos.resetar_partida()    
                        desafio = logic.obter_novo_desafio(sistema_pontos.combo)
                        tempo_restante = sistema_pontos.calcular_tempo_limite()
                        deslocamento_y = 0
                        deslocamento_x = 0
                        estado_Atual = jogando
                    elif opcao_menu == 1:  # segundo botao
                        tocar_botao()
                        estado_Atual = OPCOES
                    elif opcao_menu == 2:
                          # terceiro botao
                        tocar_botao()
                        pygame.quit()
                        sys.exit()

                # Se o mouse estiver sobre um botão, a mãozinha pula para ele
            elif evento.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                acao = obter_botao_clicado(pos, tela)
                opcao_anterior = opcao_menu

            
                if acao == "play":                   
                    opcao_menu = 0                  
                elif acao == "config":
                    opcao_menu = 1                    
                elif acao == "quit":
                    opcao_menu = 2      

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
                    opcao_opcoes = (opcao_opcoes - 1) % len(resolucoes)

                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    tocar_botao()
                    opcao_opcoes = (opcao_opcoes + 1) % len(resolucoes)

                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    tocar_botao()
                    aplicar_resolucao(resolucoes[opcao_opcoes])

                elif evento.key == pygame.K_ESCAPE:
                    tocar_botao()
                    estado_Atual = menu

        # JOGO
        elif estado_Atual == jogando:
            if evento.type == pygame.KEYDOWN:
                escolha = None
                if evento.key == pygame.K_UP or evento.key == pygame.K_w: 
                    escolha = "CIMA"
                    alvo_y = -300
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s: 
                    escolha = "BAIXO"
                    alvo_y = 300  
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a: 
                    escolha = "ESQUERDA"
                    alvo_x = -350
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d: 
                    escolha = "DIREITA"
                    alvo_x = 350

               
                
                if escolha:
                    if logic.validar_jogada(escolha, desafio["corretas"]):
                        tocar_acerto()
                        sistema_pontos.registrar_acerto()
                        desafio = logic.obter_novo_desafio(sistema_pontos.combo)
                        tempo_restante = sistema_pontos.calcular_tempo_limite()
                    else:
                        if sistema_pontos.verificar_novo_recorde():
                            estado_Atual = REGISTRANDO
                        else:
                            estado_Atual = GAME_OVER
                        tocar_erro()

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

    # Lógica de retorno da imagem
    # Faz a imagem voltar suavemente para o centro (0, 0) a cada frame

    if estado_Atual == jogando:
    
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
    if estado_Atual == jogando:
        tempo_restante -= relogio.get_time() / 1000.0

        if tempo_restante <= 0:
            if sistema_pontos.verificar_novo_recorde():
                estado_Atual = REGISTRANDO
            else:
                estado_Atual = GAME_OVER
                tocar_erro()

    # RENDER
    if estado_Atual == menu:
        exibir_menu_principal(tela, desenhar_texto, fontes_jogo, opcao_menu)

    elif estado_Atual == jogando:
        exibir_gameplay(tela, desenhar_texto, fontes_jogo, desafio, sistema_pontos, tempo_restante, imagem_gameplay, animacao_perso, (deslocamento_x, deslocamento_y))

    elif estado_Atual == OPCOES:
        from src.ui.menus import exibir_opcoes
        exibir_opcoes(tela, desenhar_texto, fontes_jogo, opcao_opcoes, resolucoes)

    elif estado_Atual == GAME_OVER:
        exibir_game_over(tela, desenhar_texto, fontes_jogo, sistema_pontos.score, sistema_pontos.ranking)

    elif estado_Atual == REGISTRANDO:
        from src.ui.menus import exibir_registro_recorde
        exibir_registro_recorde(tela, desenhar_texto, fontes_jogo, nome_input)

    pygame.display.flip()
    relogio.tick(60)