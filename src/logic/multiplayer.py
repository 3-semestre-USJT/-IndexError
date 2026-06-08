"""
Módulo de Modo Multiplayer Local.

Permite que dois jogadores compitam na mesma máquina, com pontuações separadas.
"""


class JogadorMultiplayer:
    """
    Representa um jogador no modo multiplayer.
    
    Atributos:
        numero: Número do jogador (1 ou 2)
        score: Pontuação do jogador
        combo: Combo atual
        multiplicador: Multiplicador de combo
        vidas: Vidas restantes
    """
    
    def __init__(self, numero: int):
        self.numero = numero
        self.score = 0
        self.combo = 0
        self.multiplicador = 1
        self.vidas = 3
        self.acertos = 0
        self.erros = 0
        self.ativo = True  # Se ainda está no jogo (vidas > 0)
    
    def registrar_acerto(self, pontos_base: int, acertos_para_levelup: int):
        """Registra um acerto para este jogador."""
        self.combo += 1
        self.acertos += 1
        
        if self.combo % acertos_para_levelup == 0:
            self.multiplicador += 1
        
        self.score += int(pontos_base * self.multiplicador)
    
    def registrar_erro(self):
        """Registra um erro para este jogador."""
        self.combo = 0
        self.erros += 1
        self.vidas -= 1
        
        if self.vidas <= 0:
            self.ativo = False
    
    def resetar(self):
        """Reseta as estatísticas do jogador."""
        self.score = 0
        self.combo = 0
        self.multiplicador = 1
        self.vidas = 3
        self.acertos = 0
        self.erros = 0
        self.ativo = True


class GerenciadorMultiplayer:
    """Gerencia o modo multiplayer para 2 jogadores."""
    
    def __init__(self):
        """Inicializa o gerenciador de multiplayer."""
        self.jogador1 = JogadorMultiplayer(1)
        self.jogador2 = JogadorMultiplayer(2)
        self.jogador_atual = self.jogador1
        self.modo_ativo = False
    
    def iniciar_modo(self):
        """Inicia o modo multiplayer."""
        self.modo_ativo = True
        self.jogador1.resetar()
        self.jogador2.resetar()
        self.jogador_atual = self.jogador1
    
    def alternar_jogador(self):
        """Alterna para o próximo jogador."""
        self.jogador_atual = self.jogador2 if self.jogador_atual == self.jogador1 else self.jogador1
    
    def obter_jogador_atual(self) -> JogadorMultiplayer:
        """Retorna o jogador atual."""
        return self.jogador_atual
    
    def ambos_inativos(self) -> bool:
        """Verifica se ambos os jogadores perderam todas as vidas."""
        return not self.jogador1.ativo and not self.jogador2.ativo
    
    def obter_vencedor(self) -> JogadorMultiplayer:
        """
        Determina o vencedor baseado no score.
        
        Returns:
            JogadorMultiplayer: O jogador vencedor
        """
        if self.jogador1.score > self.jogador2.score:
            return self.jogador1
        elif self.jogador2.score > self.jogador1.score:
            return self.jogador2
        else:
            return None  # Empate
    
    def obter_placar(self) -> dict:
        """Retorna o placar atual."""
        return {
            "jogador1": {
                "numero": 1,
                "score": self.jogador1.score,
                "combo": self.jogador1.combo,
                "vidas": self.jogador1.vidas,
                "ativo": self.jogador1.ativo
            },
            "jogador2": {
                "numero": 2,
                "score": self.jogador2.score,
                "combo": self.jogador2.combo,
                "vidas": self.jogador2.vidas,
                "ativo": self.jogador2.ativo
            }
        }
    
    def terminar_modo(self):
        """Encerra o modo multiplayer."""
        self.modo_ativo = False
