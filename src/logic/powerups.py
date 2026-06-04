"""
Módulo de Sistema de Powerups.

Fornece diferentes powerups que podem ser coletados durante o jogo para
melhorar o desempenho do jogador.
"""

from enum import Enum
import random


class TipoPowerup(Enum):
    """Enumeração dos tipos de powerups disponíveis."""
    TEMPO_EXTRA = "tempo_extra"
    CONGELAR_MULTIPLICADOR = "congelar_mult"
    REMOVER_OPCAO = "remover_opcao"
    ESCUDO = "escudo"
    MULTIPLICADOR_DOBRADO = "mult_dobrado"


class Powerup:
    """
    Representa um powerup individual.
    
    Atributos:
        tipo: Tipo do powerup
        duracao: Duração em segundos (None = permanente até uso)
        ativo: Se está ativo
    """
    
    def __init__(self, tipo: TipoPowerup, duracao: float = None):
        self.tipo = tipo
        self.duracao = duracao
        self.tempo_ativacao = 0
        self.ativo = False
    
    def ativar(self, tempo_atual: float):
        """Ativa o powerup."""
        self.ativo = True
        self.tempo_ativacao = tempo_atual
    
    def desativar(self):
        """Desativa o powerup."""
        self.ativo = False
    
    def expirou(self, tempo_atual: float) -> bool:
        """Verifica se a duração do powerup expirou."""
        if self.duracao is None:
            return False
        return (tempo_atual - self.tempo_ativacao) > self.duracao


class GerenciadorPowerups:
    """Gerencia os powerups ativos do jogador."""
    
    # Taxa de aparecimento de powerups (quanto menor, mais frequente)
    CHANCE_POWERUP = 0.15  # 15% de chance
    
    # Configurações de cada powerup
    CONFIGS = {
        TipoPowerup.TEMPO_EXTRA: {
            "nome": "Tempo Extra",
            "descricao": "+5 segundos",
            "valor": 5.0,
            "duracao": None,
            "cor": (0, 255, 100)  # Verde
        },
        TipoPowerup.CONGELAR_MULTIPLICADOR: {
            "nome": "Congelar Multiplicador",
            "descricao": "Mantém o multiplicador por 30s",
            "duracao": 30.0,
            "cor": (0, 150, 255)  # Azul
        },
        TipoPowerup.REMOVER_OPCAO: {
            "nome": "Remover Opção",
            "descricao": "Remove 1 opção errada",
            "duracao": None,
            "cor": (255, 200, 0)  # Amarelo
        },
        TipoPowerup.ESCUDO: {
            "nome": "Escudo",
            "descricao": "Protege de 1 erro",
            "duracao": None,
            "cor": (255, 100, 200)  # Rosa
        },
        TipoPowerup.MULTIPLICADOR_DOBRADO: {
            "nome": "Multiplicador x2",
            "descricao": "Dobra pontos por 15s",
            "duracao": 15.0,
            "valor": 2.0,
            "cor": (255, 100, 100)  # Vermelho
        }
    }
    
    def __init__(self):
        """Inicializa o gerenciador de powerups."""
        self.powerups_ativos = []
        self.total_usado = 0
    
    def gerar_powerup_aleatorio(self) -> TipoPowerup:
        """Gera um powerup aleatório."""
        return random.choice(list(TipoPowerup))
    
    def deveria_aparecer_powerup(self) -> bool:
        """Determina se um powerup deve aparecer."""
        return random.random() < self.CHANCE_POWERUP
    
    def adicionar_powerup(self, tipo: TipoPowerup):
        """
        Adiciona um powerup ao inventário.
        
        Args:
            tipo: Tipo do powerup a adicionar
        """
        duracao = self.CONFIGS[tipo].get("duracao")
        powerup = Powerup(tipo, duracao)
        self.powerups_ativos.append(powerup)
    
    def usar_powerup(self, indice: int, tempo_atual: float = 0) -> Powerup:
        """
        Usa um powerup do inventário.
        
        Args:
            indice: Índice do powerup na lista
            tempo_atual: Tempo atual para duração
            
        Returns:
            O powerup usado ou None
        """
        if 0 <= indice < len(self.powerups_ativos):
            powerup = self.powerups_ativos[indice]
            powerup.ativar(tempo_atual)
            self.total_usado += 1
            return powerup
        return None
    
    def remover_powerup(self, indice: int):
        """Remove um powerup do inventário."""
        if 0 <= indice < len(self.powerups_ativos):
            self.powerups_ativos.pop(indice)
    
    def atualizar_powerups(self, tempo_atual: float):
        """
        Atualiza o estado dos powerups (remove os expirados).
        
        Args:
            tempo_atual: Tempo atual do jogo
        """
        self.powerups_ativos = [
            p for p in self.powerups_ativos
            if not p.expirou(tempo_atual)
        ]
    
    def obter_info_powerup(self, tipo: TipoPowerup) -> dict:
        """Retorna informações sobre um tipo de powerup."""
        return self.CONFIGS.get(tipo, {})
    
    def obter_powerups_ativos(self) -> list:
        """Retorna lista de powerups ativos."""
        return self.powerups_ativos
    
    def obter_quantidade(self) -> int:
        """Retorna quantidade de powerups no inventário."""
        return len(self.powerups_ativos)
    
    def limpar_powerups(self):
        """Remove todos os powerups."""
        self.powerups_ativos = []
