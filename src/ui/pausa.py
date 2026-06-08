"""
Módulo de Sistema de Pausa.

Fornece UI e controle para pausar e retomar o jogo.
"""

import pygame


def exibir_menu_pausa(tela, desenhar_texto_func, fontes, opcao_selecionada):
    """
    Exibe o menu de pausa na tela.
    
    Args:
        tela: Surface do pygame
        desenhar_texto_func: Função para desenhar texto
        fontes: Dicionário com as fontes disponíveis
        opcao_selecionada: Índice da opção selecionada (0=Retomar, 1=Sair)
    """
    from src.ui.cores import BRANCO, AMARELO, PRETO, CINZA_CLARO
    
    largura_tela, altura_tela = tela.get_size()
    
    # Desenha um fundo semi-transparente
    overlay = pygame.Surface((largura_tela, altura_tela))
    overlay.set_alpha(128)
    overlay.fill(PRETO)
    tela.blit(overlay, (0, 0))
    
    # Título
    desenhar_texto_func("PAUSADO", BRANCO, -120, fontes['grande'])
    
    # Opções
    opcoes = ["RETOMAR", "MENU PRINCIPAL"]
    
    for i, opcao in enumerate(opcoes):
        cor = AMARELO if i == opcao_selecionada else BRANCO
        pos_y = -20 + (i * 80)
        desenhar_texto_func(opcao, cor, pos_y, fontes['media'])
    
    desenhar_texto_func("SETAS para navegar | ENTER para selecionar", CINZA_CLARO, 150, fontes['pequena'])
