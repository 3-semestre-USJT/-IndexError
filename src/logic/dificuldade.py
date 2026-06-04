"""
Módulo de Gerenciamento de Dificuldades do Jogo.

Fornece classes e funções para gerenciar os diferentes níveis de dificuldade,
incluindo configurações de tempo, multiplicadores e balanceamento.
"""

from enum import Enum


class NivelDificuldade(Enum):
    """Enumeração dos níveis de dificuldade disponíveis."""
    FACIL = "FÁCIL"
    NORMAL = "NORMAL"
    DIFICIL = "DIFÍCIL"


class ConfigDificuldade:
    """
    Configurações específicas de cada nível de dificuldade.
    
    Atributos:
        nome: Nome legível do nível
        tempo_inicial: Tempo inicial em segundos
        tempo_minimo: Tempo mínimo permitido
        taxa_reducao_tempo: Redução de tempo por 1000 pontos
        acertos_para_levelup: Acertos necessários para aumentar multiplicador
        velocidade_combo: Multiplicador de velocidade de ganho de combo
    """
    
    def __init__(self, nome: str, tempo_inicial: float, tempo_minimo: float,
                 taxa_reducao: float, acertos_levelup: int, vel_combo: float):
        self.nome = nome
        self.tempo_inicial = tempo_inicial
        self.tempo_minimo = tempo_minimo
        self.taxa_reducao_tempo = taxa_reducao
        self.acertos_para_levelup = acertos_levelup
        self.velocidade_combo = vel_combo


# Pré-configurações de dificuldade
DIFICULDADES = {
    NivelDificuldade.FACIL: ConfigDificuldade(
        nome="FÁCIL",
        tempo_inicial=20.0,
        tempo_minimo=8.0,
        taxa_reducao=1.0,
        acertos_levelup=3,
        vel_combo=1.2
    ),
    NivelDificuldade.NORMAL: ConfigDificuldade(
        nome="NORMAL",
        tempo_inicial=15.0,
        tempo_minimo=5.0,
        taxa_reducao=1.5,
        acertos_levelup=5,
        vel_combo=1.0
    ),
    NivelDificuldade.DIFICIL: ConfigDificuldade(
        nome="DIFÍCIL",
        tempo_inicial=10.0,
        tempo_minimo=3.0,
        taxa_reducao=2.0,
        acertos_levelup=7,
        vel_combo=0.8
    )
}


class GerenciadorDificuldade:
    """Gerencia a dificuldade atual e suas configurações."""
    
    def __init__(self, dificuldade_inicial: NivelDificuldade = NivelDificuldade.NORMAL):
        """
        Inicializa o gerenciador de dificuldade.
        
        Args:
            dificuldade_inicial: Nível de dificuldade inicial (padrão: NORMAL)
        """
        self.dificuldade_atual = dificuldade_inicial
        self.config = DIFICULDADES[dificuldade_inicial]
    
    def definir_dificuldade(self, nivel: NivelDificuldade):
        """Define um novo nível de dificuldade."""
        self.dificuldade_atual = nivel
        self.config = DIFICULDADES[nivel]
    
    def obter_config(self) -> ConfigDificuldade:
        """Retorna a configuração do nível atual."""
        return self.config
    
    def obter_nome(self) -> str:
        """Retorna o nome do nível atual."""
        return self.config.nome
