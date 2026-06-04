"""
Módulo de Gerenciamento de Controles Customizáveis.

Permite que o jogador remappe as teclas de controle do jogo.
"""

import json
import os
import pygame


class MapeadorControles:
    """
    Gerencia o mapeamento de controles e customização de teclas.
    
    Atributos:
        mapa: Dicionário com mapeamento de ações para teclas
    """
    
    # Mapeamento padrão de controles
    CONTROLES_PADRAO = {
        "CIMA": [pygame.K_UP, pygame.K_w],
        "BAIXO": [pygame.K_DOWN, pygame.K_s],
        "ESQUERDA": [pygame.K_LEFT, pygame.K_a],
        "DIREITA": [pygame.K_RIGHT, pygame.K_d],
        "MENU_UP": [pygame.K_UP, pygame.K_w],
        "MENU_DOWN": [pygame.K_DOWN, pygame.K_s],
        "SELECIONAR": [pygame.K_RETURN, pygame.K_KP_ENTER],
        "VOLTAR": [pygame.K_ESCAPE],
        "PAUSAR": [pygame.K_ESCAPE, pygame.K_p]
    }
    
    # Nomes legíveis das teclas
    NOMES_TECLAS = {
        pygame.K_UP: "↑",
        pygame.K_DOWN: "↓",
        pygame.K_LEFT: "←",
        pygame.K_RIGHT: "→",
        pygame.K_w: "W",
        pygame.K_a: "A",
        pygame.K_s: "S",
        pygame.K_d: "D",
        pygame.K_RETURN: "ENTER",
        pygame.K_KP_ENTER: "KP_ENTER",
        pygame.K_ESCAPE: "ESC",
        pygame.K_p: "P",
        pygame.K_SPACE: "SPACE"
    }
    
    def __init__(self):
        """Inicializa o mapeador de controles."""
        self.mapa = self.CONTROLES_PADRAO.copy()
        self.caminho_arquivo = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "controles.json"
        )
        self.carregar_controles()
    
    def obter_teclas(self, acao: str) -> list:
        """
        Retorna as teclas configuradas para uma ação.
        
        Args:
            acao: Nome da ação
            
        Returns:
            Lista de códigos de tecla
        """
        return self.mapa.get(acao, [])
    
    def verificar_acao(self, evento_key: int) -> str:
        """
        Verifica qual ação corresponde a uma tecla pressionada.
        
        Args:
            evento_key: Código da tecla pressionada
            
        Returns:
            Nome da ação ou None
        """
        for acao, teclas in self.mapa.items():
            if evento_key in teclas:
                return acao
        return None
    
    def remapear(self, acao: str, teclas: list):
        """
        Remapeia uma ação para novas teclas.
        
        Args:
            acao: Nome da ação
            teclas: Lista de códigos de tecla
        """
        if acao in self.mapa:
            self.mapa[acao] = teclas
            self.salvar_controles()
    
    def resetar_padrao(self):
        """Reseta todos os controles para o padrão."""
        self.mapa = self.CONTROLES_PADRAO.copy()
        self.salvar_controles()
    
    def obter_nome_tecla(self, codigo_tecla: int) -> str:
        """Retorna o nome legível de uma tecla."""
        return self.NOMES_TECLAS.get(codigo_tecla, f"KEY_{codigo_tecla}")
    
    def salvar_controles(self):
        """Salva controles customizados no arquivo."""
        try:
            os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
            dados = {acao: teclas for acao, teclas in self.mapa.items()}
            with open(self.caminho_arquivo, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)
        except IOError as erro:
            print(f"Erro ao salvar controles: {erro}")
    
    def carregar_controles(self):
        """Carrega controles customizados do arquivo."""
        if not os.path.exists(self.caminho_arquivo):
            return
        
        try:
            with open(self.caminho_arquivo, 'r') as arquivo:
                dados = json.load(arquivo)
                for acao, teclas in dados.items():
                    if acao in self.mapa:
                        self.mapa[acao] = teclas
        except (json.JSONDecodeError, IOError) as erro:
            print(f"Erro ao carregar controles: {erro}")
