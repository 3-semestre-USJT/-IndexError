from math import sin
from src.ui.cores import *
import pygame
import cv2
from src.ui import botoes

def escala_tela(imagem, tela):
    largura_tela, altura_tela = tela.get_size()
    
    # Irá Redimensionar a imagem forçando ela a ter o tamanho exato da tela
    # smoothscale é utilizado para a imagem não ficar muito pixelada ao esticar
    return pygame.transform.smoothscale(imagem, (largura_tela, altura_tela))


    # Toca o video da intro
def exibir_video_intro(tela, caminho_video):
    
    #Carrega o video utilizando OpenCV
    cap = cv2.VideoCapture(caminho_video)
    relogio = pygame.time.Clock()
    fps = cap.get(cv2.CAP_PROP_FPS)

    rodando = True
    ir_para_menu = True

    while rodando and cap.isOpened():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                ir_para_menu = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tamanho = frame_rgb.shape[1::-1]
        surface_frame = pygame.image.frombuffer(frame_rgb.tobytes(),tamanho,"RGB")
        # Redimenciona o video para cobrir a tela inteira
        surface_frame = escala_tela(surface_frame,tela)

        # Mostra o video na tela
        tela.blit(surface_frame, (0,0)) 
        pygame.display.flip()
        relogio.tick(fps)

    cap.release()
    pygame.display.set_mode(tela.get_size())
    return ir_para_menu


def exibir_menu_principal(tela, desenhar_texto_func, fontes, opcao_selecionada):
    # Desenha a tela inicial do jogo com botões visuais
    desenhar_texto_func("TupãStudios", BRANCO, -250, fontes['media'])
    desenhar_texto_func("! INDEXERROR", BRANCO, -150, fontes['grande'])

    # Obter botões escalonados e imagem da mão seletora
    play_button, tutorial_button, time_attack_button, config_button, quit_button, img_mao = botao_escalonado(tela)
    
    # Exibir todos os botões com imagem
    play_button.exibir_botao(tela)
    tutorial_button.exibir_botao(tela)
    time_attack_button.exibir_botao(tela)
    config_button.exibir_botao(tela)
    quit_button.exibir_botao(tela)
    
    # Lista de botões para posicionamento da mão seletora
    botoes = [play_button, tutorial_button, time_attack_button, config_button, quit_button]
    
    # Posicionar a mão seletora ao lado do botão selecionado
    if opcao_selecionada < len(botoes):
        botao_selecionado = botoes[opcao_selecionada]
        x_mao = botao_selecionado.rect.right + 10
        y_mao = botao_selecionado.rect.centery - img_mao.get_height() // 2
        tela.blit(img_mao, (x_mao, y_mao))

    # Janelinha de desafios diários (canto inferior direito)
    largura_tela, altura_tela = tela.get_size()
    largura_janela = 320
    altura_janela = 140
    x_janela = largura_tela - largura_janela - 20
    y_janela = altura_tela - altura_janela - 20

    # Fundo com gradiente simulado e bordas
    pygame.draw.rect(tela, (15, 25, 50), (x_janela, y_janela, largura_janela, altura_janela))
    pygame.draw.rect(tela, (50, 120, 200), (x_janela, y_janela, largura_janela, altura_janela), 3)
    pygame.draw.rect(tela, (80, 160, 255), (x_janela + 4, y_janela + 4, largura_janela - 8, altura_janela - 8), 1)

    # Título com destaque
    fonte_titulo = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
    texto_titulo = fonte_titulo.render("DESAFIOS DIÁRIOS", True, (255, 220, 100))
    tela.blit(texto_titulo, (x_janela + 15, y_janela + 8))

    # Desafios do dia (baseados na data)
    from datetime import datetime
    hoje = datetime.now()
    dia_do_ano = hoje.timetuple().tm_yday

    desafios_possiveis = [
        "Alcançar 500 pontos",
        "Alcançar 1000 pontos",
        "Alcançar 2000 pontos",
        "Alcançar 3000 pontos",
        "Alcançar 5000 pontos",
        "Fazer combo de 100",
        "Fazer combo de 500",
        "Fazer combo de 1000",
        "10 acertos sem errar",
        "20 acertos sem errar",
        "Completar 50 acertos",
        "Completar 100 acertos",
        "Jogar 5 partidas",
        "Jogar 10 partidas",
        "Jogar 20 partidas"
    ]

    # Selecionar 3 desafios do dia
    desafios_hoje = []
    for i in range(3):
        indice = (dia_do_ano + i) % len(desafios_possiveis)
        desafios_hoje.append(f"{i+1}. {desafios_possiveis[indice]}")

    # Desafios com design melhorado
    fonte_desafio = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 11)
    for i, desafio in enumerate(desafios_hoje):
        # Cor alternada para cada desafio
        cor_desafio = (100, 200, 255) if i % 2 == 0 else (150, 220, 255)
        texto_desafio = fonte_desafio.render(desafio, True, cor_desafio)
        tela.blit(texto_desafio, (x_janela + 15, y_janela + 30 + (i * 28)))


    

def botao_escalonado(tela):
    largura_tela, altura_tela = tela.get_size()

    # Calcula a escala
    escala_x = largura_tela / 1280
    escala_y = altura_tela / 720

    fator_reducao = 0.30 

    # Pega as dimensões e já aplica a redução + a escala da tela
    largura_final = int(botoes.botao_play.get_width() * escala_x * fator_reducao)
    altura_final = int(botoes.botao_play.get_height() * escala_y * fator_reducao)

    # Redimensiona as imagens dos botões para não ficarem minúsculas
    img_play = pygame.transform.smoothscale(botoes.botao_play, (largura_final, altura_final))
    img_config = pygame.transform.smoothscale(botoes.botao_config, (largura_final, altura_final))
    img_tutorial = pygame.transform.smoothscale(botoes.botao_tutorial, (largura_final, altura_final))
    img_time_attack = pygame.transform.smoothscale(botoes.botao_time_attack, (largura_final, altura_final))
    img_quit = pygame.transform.smoothscale(botoes.botao_sair, (largura_final, altura_final)) 
   
    # Redimensionando a mãozinha seletora
    proporcao = botoes.mao_seletora.get_width() / botoes.mao_seletora.get_height()
    altura_alvo = int(img_play.get_height() * 0.5)
    largura_alvo = int(altura_alvo * proporcao)
    img_mao = pygame.transform.smoothscale(botoes.mao_seletora, (largura_alvo, altura_alvo))

    #Transforma posições fixas em porcentagens (posições relativas)
    x = largura_tela * 0.05

    # Transforma o Y para 5 botões (distribuídos uniformemente)
    y_inicial = altura_tela * 0.35
    espacamento = altura_tela * 0.10

    y_play = y_inicial
    y_tutorial = y_inicial + espacamento
    y_time_attack = y_inicial + (espacamento * 2)
    y_config = y_inicial + (espacamento * 3)
    y_quit = y_inicial + (espacamento * 4)

    # Cria e retorna as instâncias dos botões na posição certa e tamanho certo
    play_button = botoes.botao(x, y_play, img_play)
    tutorial_button = botoes.botao(x, y_tutorial, img_tutorial)
    time_attack_button = botoes.botao(x, y_time_attack, img_time_attack)
    config_button = botoes.botao(x, y_config, img_config)
    quit_button = botoes.botao(x, y_quit, img_quit)
    
    return play_button, tutorial_button, time_attack_button, config_button, quit_button, img_mao

def obter_botao_clicado(pos, tela): 
    # Obter botões escalonados
    play_button, tutorial_button, time_attack_button, config_button, quit_button, _ = botao_escalonado(tela)
    
    # Verificar clique em cada botão
    if play_button.clicado(pos):
        return "play"
    elif tutorial_button.clicado(pos):
        return "tutorial"
    elif time_attack_button.clicado(pos):
        return "time_attack"
    elif config_button.clicado(pos):
        return "config"
    elif quit_button.clicado(pos):
        return "quit"
    
    return None

def exibir_opcoes(tela, desenhar_texto_func, fontes, opcao_selecionada, resolucoes, indice_resolucao, musica_ativada, som_efeitos_ativado):
    """
    Exibe o menu de configurações com 7 opções:
    0 = Resolução, 1 = Música, 2 = Som de Efeitos, 3 = Controles, 4 = Histórico, 5 = Conquistas, 6 = Desafio Diário
    """
    largura_tela, altura_tela = tela.get_size()
    tela.fill(PRETO)
    escala = altura_tela / 720

    desenhar_texto_func("CONFIGURAÇÕES", BRANCO, int(-280 * escala), fontes['grande'])

    # Definir cores com base na seleção
    cores_opcoes = [AMARELO if opcao_selecionada == i else BRANCO for i in range(7)]

    # Resolução (Opção 0)
    desenhar_texto_func("RESOLUÇÃO", cores_opcoes[0], int(-200 * escala), fontes['media'])
    if resolucoes[indice_resolucao] == "FULLSCREEN":
        texto_res = "FULLSCREEN"
    else:
        texto_res = f"{resolucoes[indice_resolucao][0]} x {resolucoes[indice_resolucao][1]}"
    desenhar_texto_func(f"> {texto_res} <", VERDE_VIBRANTE, int(-160 * escala), fontes['pequena'])

    # Música (Opção 1)
    desenhar_texto_func("MÚSICA", cores_opcoes[1], int(-100 * escala), fontes['media'])
    status_musica = "SIM" if musica_ativada else "NAO"
    cor_status_mus = VERDE_VIBRANTE if musica_ativada else VERMELHO_VIVO
    desenhar_texto_func(f"> {status_musica} <", cor_status_mus, int(-60 * escala), fontes['pequena'])

    # Som de Efeitos (Opção 2)
    desenhar_texto_func("SOM DE EFEITOS", cores_opcoes[2], int(0 * escala), fontes['media'])
    status_som = "SIM" if som_efeitos_ativado else "NAO"
    cor_status_som = VERDE_VIBRANTE if som_efeitos_ativado else VERMELHO_VIVO
    desenhar_texto_func(f"> {status_som} <", cor_status_som, int(40 * escala), fontes['pequena'])

    # Controles (Opção 3)
    desenhar_texto_func("CONTROLES", cores_opcoes[3], int(80 * escala), fontes['media'])
    desenhar_texto_func("> VER CONTROLES <", AZUL, int(110 * escala), fontes['pequena'])

    # Histórico (Opção 4)
    desenhar_texto_func("HISTÓRICO", cores_opcoes[4], int(150 * escala), fontes['media'])
    desenhar_texto_func("> VER HISTÓRICO <", AZUL, int(180 * escala), fontes['pequena'])

    # Conquistas (Opção 5)
    desenhar_texto_func("CONQUISTAS", cores_opcoes[5], int(220 * escala), fontes['media'])
    desenhar_texto_func("> VER CONQUISTAS <", AZUL, int(250 * escala), fontes['pequena'])

    # Desafio Diário (Opção 6)
    desenhar_texto_func("DESAFIO DIÁRIO", cores_opcoes[6], int(290 * escala), fontes['media'])
    desenhar_texto_func("> VER DESAFIO <", AZUL, int(320 * escala), fontes['pequena'])

    # Instruções
    desenhar_texto_func("SETAS para navegar | ESQUERDA/DIREITA para mudar | ENTER para ver | ESC para voltar",
                       CINZA_CLARO, int(380 * escala), fontes['pequena']) 

def exibir_game_over(tela, desenhar_texto_func, fontes, score, ranking, dificuldade="NORMAL"):
    tela.fill(VERMELHO_MORTE)

    desenhar_texto_func("GAME OVER", VERMELHO_VIVO, -180, fontes['grande'])
    desenhar_texto_func(f"Score Final: {score}", BRANCO, -120, fontes['media'])
    desenhar_texto_func(f"Dificuldade: {dificuldade}", (200, 200, 255), -80, fontes['pequena'])

    desenhar_texto_func(f"TOP 3 - {dificuldade}", ROSA_PASTEL, -30, fontes['media'])

    # Obter ranking da dificuldade específica
    ranking_dificuldade = ranking.get(dificuldade, ranking.get("NORMAL", []))
    
    y_pos = 20
    for i, dados in enumerate(ranking_dificuldade):
        texto_ranking = f"{i + 1}. {dados['nome']} - {dados['pontos']}"

        if i == 0:
            cor = DOURADO
        elif i == 1:
            cor = PRATA
        else:
            cor = BRONZE

        desenhar_texto_func(texto_ranking, cor, y_pos, fontes['pequena'])
        y_pos += 40

    desenhar_texto_func("Pressione R para tentar de novo", CINZA, 180, fontes['pequena'])


def exibir_registro_recorde(tela, desenhar_texto_func, fontes, nome_atual):
    tela.fill(PRETO)
    desenhar_texto_func("NOVO RECORDE!", AMARELO, -150, fontes['grande'])
    desenhar_texto_func("DIGITE AS INICIAIS", BRANCO, -50, fontes['media'])

    letras_display = nome_atual.ljust(3, "_")
    letras_espacadas = " ".join(letras_display)

    desenhar_texto_func(letras_espacadas, VERDE_VIBRANTE, 50, fontes['grande'])
    desenhar_texto_func("Pressione ENTER para salvar", CINZA_CLARO, 150, fontes['pequena'])