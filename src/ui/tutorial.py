"""
Módulo de Tutorial Interativo.

Oferece um tutorial in-game para ensinar os controles e mecânicas ao jogador.
"""


class GerenciadorTutorial:
    """Gerencia o estado e exibição do tutorial."""
    
    ESTAPAS_TUTORIAL = [
        {
            "titulo": "Bem-vindo ao ! IndexError",
            "mensagem": "Este é um jogo de desafios rápidos. Pressione ESPAÇO para continuar.",
            "dica": "Use SETAS ou WASD para responder"
        },
        {
            "titulo": "Mecânica do Jogo",
            "mensagem": "Leia a palavra e escolha a direção correspondente rapidamente!",
            "dica": "CIMA = ↑ | BAIXO = ↓ | ESQUERDA = ← | DIREITA = →"
        },
        {
            "titulo": "Sistema de Combo",
            "mensagem": "Acertos consecutivos aumentam o combo e seus multiplicadores!",
            "dica": "A cada 5 acertos, o multiplicador aumenta em 1x"
        },
        {
            "titulo": "Vidas e Dificuldade",
            "mensagem": "Comece com 3 vidas. Erre para perder uma vida.",
            "dica": "Você pode configurar a dificuldade no menu"
        },
        {
            "titulo": "Powerups",
            "mensagem": "Colete powerups especiais para melhorar seu desempenho!",
            "dica": "Tempo Extra, Escudo, Multiplicador x2 e muito mais"
        },
        {
            "titulo": "Pronto para Jogar?",
            "mensagem": "Boa sorte! Pressione ENTER para começar.",
            "dica": "Você sempre pode consultar os controles no menu de opções"
        }
    ]
    
    def __init__(self):
        """Inicializa o gerenciador de tutorial."""
        self.etapa_atual = 0
        self.tutorial_ativo = False
        self.tutorial_concluido = False
    
    def iniciar_tutorial(self):
        """Inicia o tutorial."""
        self.tutorial_ativo = True
        self.etapa_atual = 0
        self.tutorial_concluido = False
    
    def proximo_passo(self) -> bool:
        """
        Avança para o próximo passo do tutorial.
        
        Returns:
            True se há próximo passo, False se tutorial acabou
        """
        self.etapa_atual += 1
        if self.etapa_atual >= len(self.ESTAPAS_TUTORIAL):
            self.tutorial_concluido = True
            self.tutorial_ativo = False
            return False
        return True
    
    def obter_etapa_atual(self) -> dict:
        """Retorna os dados da etapa atual."""
        if self.etapa_atual < len(self.ESTAPAS_TUTORIAL):
            return self.ESTAPAS_TUTORIAL[self.etapa_atual]
        return {}
    
    def obter_numero_etapas(self) -> int:
        """Retorna o número total de etapas."""
        return len(self.ESTAPAS_TUTORIAL)
    
    def obter_etapa_numero(self) -> int:
        """Retorna o número da etapa atual (1-indexed)."""
        return self.etapa_atual + 1
    
    def pular_tutorial(self):
        """Pula o tutorial."""
        self.tutorial_ativo = False
        self.tutorial_concluido = True


def exibir_tutorial(tela, desenhar_texto_func, fontes, gerenciador_tutorial):
    """
    Exibe a tela de tutorial.
    
    Args:
        tela: Surface do pygame
        desenhar_texto_func: Função para desenhar texto
        fontes: Dicionário com as fontes
        gerenciador_tutorial: Instância do gerenciador de tutorial
    """
    from src.ui.cores import BRANCO, AZUL_CIANO, CINZA_CLARO, PRETO
    import pygame
    
    tela.fill(PRETO)
    
    etapa = gerenciador_tutorial.obter_etapa_atual()
    numero_etapa = gerenciador_tutorial.obter_etapa_numero()
    total_etapas = gerenciador_tutorial.obter_numero_etapas()
    
    if not etapa:
        return
    
    # Título da etapa
    desenhar_texto_func(etapa["titulo"], AZUL_CIANO, -150, fontes['grande'])
    
    # Mensagem principal
    desenhar_texto_func(etapa["mensagem"], BRANCO, -50, fontes['media'])
    
    # Dica
    desenhar_texto_func(f"💡 {etapa['dica']}", CINZA_CLARO, 80, fontes['pequena'])
    
    # Progresso
    progresso = f"({numero_etapa}/{total_etapas})"
    desenhar_texto_func(progresso, CINZA_CLARO, 200, fontes['pequena'])
    
    # Instruções
    if numero_etapa < total_etapas:
        instrucao = "Pressione ESPAÇO para continuar"
    else:
        instrucao = "Pressione ENTER para começar o jogo"
    desenhar_texto_func(instrucao, BRANCO, 250, fontes['pequena'])
