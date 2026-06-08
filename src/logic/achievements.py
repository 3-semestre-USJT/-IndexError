"""
Módulo de Gerenciamento de Achievements/Conquistas.

Sistema que rastreia e gerencia badges e conquistas desbloqueáveis do jogador.
"""

import json
import os
from datetime import datetime


class Achievement:
    """
    Representa uma conquista/badge único.
    
    Atributos:
        id: Identificador único
        nome: Nome da conquista
        descricao: Descrição da conquista
        desbloqueada: Se foi desbloqueada
        data_desbloqueio: Data de quando foi desbloqueada
    """
    
    def __init__(self, id_: str, nome: str, descricao: str):
        self.id = id_
        self.nome = nome
        self.descricao = descricao
        self.desbloqueada = False
        self.data_desbloqueio = None
    
    def desbloquear(self):
        """Marca a conquista como desbloqueada."""
        if not self.desbloqueada:
            self.desbloqueada = True
            self.data_desbloqueio = datetime.now().isoformat()
    
    def para_dict(self) -> dict:
        """Converte a conquista para dicionário (para JSON)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "desbloqueada": self.desbloqueada,
            "data_desbloqueio": self.data_desbloqueio
        }


class GerenciadorAchievements:
    """Gerencia todas as conquistas do jogador."""
    
    # Definição de todas as possíveis conquistas
    CONQUISTAS_PADRAO = [
        ("combo_100", "Combo Iniciante", "Alcançar 100 de combo em uma partida"),
        ("combo_500", "Combo Mestre", "Alcançar 500 de combo em uma partida"),
        ("combo_1000", "Combo Supremo", "Alcançar 1000 de combo em uma partida"),
        ("combo_2000", "Combo Lendário", "Alcançar 2000 de combo em uma partida"),
        ("combo_5000", "Combo Divino", "Alcançar 5000 de combo em uma partida"),
        ("velocista", "Velocista", "Completar um desafio em menos de 2 segundos"),
        ("recordista", "Recordista", "Bater o high score"),
        ("10_acertos", "Iniciante", "Acertar 10 desafios em uma partida"),
        ("20_acertos", "Veterano", "Acertar 20 desafios em uma partida"),
        ("50_acertos", "Lenda", "Acertar 50 desafios em uma partida"),
        ("100_acertos", "Mestre Absoluto", "Acertar 100 desafios em uma partida"),
        ("200_acertos", "Deus do Jogo", "Acertar 200 desafios em uma partida"),
        ("primeiro_recorde", "Primeiro Recorde", "Salvar o primeiro recorde"),
        ("5_partidas", "Gamer Casual", "Completar 5 partidas"),
        ("10_partidas", "Gamer Regular", "Completar 10 partidas"),
        ("50_partidas", "Gamer Dedicado", "Completar 50 partidas"),
        ("100_partidas", "Gamer Veterano", "Completar 100 partidas"),
        ("200_partidas", "Gamer Lendário", "Completar 200 partidas"),
        ("500_partidas", "Gamer Mítico", "Completar 500 partidas"),
        ("sem_erros_5", "Precisão", "Acertar 5 desafios sem errar"),
        ("sem_erros_10", "Perfeição", "Acertar 10 desafios sem errar"),
        ("sem_erros_20", "Deus da Precisão", "Acertar 20 desafios sem errar"),
        ("sem_erros_30", "Perfeição Absoluta", "Acertar 30 desafios sem errar"),
        ("dificil_50_pontos", "Dificuldade Alta", "Alcançar 50 pontos em Difícil"),
        ("dificil_100_pontos", "Dificuldade Extrema", "Alcançar 100 pontos em Difícil"),
        ("dificil_200_pontos", "Impossível", "Alcançar 200 pontos em Difícil"),
        ("dificil_500_pontos", "Desafio Supremo", "Alcançar 500 pontos em Difícil"),
        ("facil_100_pontos", "Caminho Fácil", "Alcançar 100 pontos em Fácil"),
        ("facil_500_pontos", "Mestre do Fácil", "Alcançar 500 pontos em Fácil"),
        ("powerup_5", "Coletor Iniciante", "Usar 5 powerups em partidas"),
        ("powerup_10", "Coletor", "Usar 10 powerups em partidas"),
        ("powerup_25", "Mestre dos Powerups", "Usar 25 powerups em partidas"),
        ("powerup_50", "Senhor dos Powerups", "Usar 50 powerups em partidas"),
        ("powerup_100", "Deus dos Powerups", "Usar 100 powerups em partidas"),
        ("score_1000", "Mil Pontos", "Alcançar 1000 pontos em uma partida"),
        ("score_5000", "Cinco Mil Pontos", "Alcançar 5000 pontos em uma partida"),
        ("score_10000", "Dez Mil Pontos", "Alcançar 10000 pontos em uma partida"),
        ("score_25000", "Vinte e Cinco Mil", "Alcançar 25000 pontos em uma partida"),
        ("score_50000", "Cinquenta Mil", "Alcançar 50000 pontos em uma partida"),
        ("score_100000", "Cem Mil", "Alcançar 100000 pontos em uma partida"),
        ("time_attack_30", "Time Attack Iniciante", "Completar 30 desafios no Time Attack"),
        ("time_attack_50", "Time Attack Mestre", "Completar 50 desafios no Time Attack"),
        ("time_attack_75", "Time Attack Lendário", "Completar 75 desafios no Time Attack"),
        ("time_attack_100", "Time Attack Supremo", "Completar 100 desafios no Time Attack"),
        ("sobrevivente", "Sobrevivente", "Ter 1 vida restante ao terminar"),
        ("invencivel", "Invencível", "Ter 3 vidas restantes ao terminar"),
        ("nivel_10", "Nível 10", "Alcançar nível 10"),
        ("nivel_25", "Nível 25", "Alcançar nível 25"),
        ("nivel_50", "Nível 50", "Alcançar nível 50"),
        ("nivel_100", "Nível 100", "Alcançar nível 100"),
        ("combo_perfeito_10", "Combo Perfeito 10", "Manter combo 10 com 0 erros"),
        ("combo_perfeito_25", "Combo Perfeito 25", "Manter combo 25 com 0 erros"),
        ("combo_perfeito_50", "Combo Perfeito 50", "Manter combo 50 com 0 erros"),
        ("desafio_diario_7", "Semana de Desafios", "Completar 7 desafios diários"),
        ("desafio_diario_30", "Mês de Desafios", "Completar 30 desafios diários"),
        ("tempo_10s", "Relâmpago", "Completar desafio em menos de 10s"),
        ("tempo_5s", "Supersônico", "Completar desafio em menos de 5s"),
        ("tempo_3s", "Luz", "Completar desafio em menos de 3s"),
    ]
    
    def __init__(self):
        """Inicializa o gerenciador de achievements."""
        self.achievements = {}
        self._inicializar_achievements()
        self.caminho_arquivo = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "achievements.json"
        )
        self.carregar_achievements()
    
    def _inicializar_achievements(self):
        """Cria todas as conquistas possíveis."""
        for id_, nome, desc in self.CONQUISTAS_PADRAO:
            self.achievements[id_] = Achievement(id_, nome, desc)
    
    def desbloquear(self, id_achievement: str) -> bool:
        """
        Desbloqueia uma conquista se existir.
        
        Args:
            id_achievement: ID da conquista
            
        Returns:
            True se foi desbloqueada, False se já estava desbloqueada
        """
        if id_achievement in self.achievements:
            achievement = self.achievements[id_achievement]
            if not achievement.desbloqueada:
                achievement.desbloquear()
                self.salvar_achievements()
                return True
        return False
    
    def obter_desbloqueadas(self) -> list:
        """Retorna lista de conquistas desbloqueadas."""
        return [a for a in self.achievements.values() if a.desbloqueada]
    
    def obter_total_desbloqueadas(self) -> int:
        """Retorna quantidade de conquistas desbloqueadas."""
        return len(self.obter_desbloqueadas())
    
    def obter_percentual_desbloqueio(self) -> float:
        """Retorna percentual de conquistas desbloqueadas."""
        total = len(self.achievements)
        if total == 0:
            return 0.0
        return (self.obter_total_desbloqueadas() / total) * 100
    
    def salvar_achievements(self):
        """Salva achievements no arquivo JSON."""
        try:
            os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
            dados = {id_: ach.para_dict() for id_, ach in self.achievements.items()}
            with open(self.caminho_arquivo, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)
        except IOError as erro:
            print(f"Erro ao salvar achievements: {erro}")
    
    def carregar_achievements(self):
        """Carrega achievements do arquivo JSON."""
        if not os.path.exists(self.caminho_arquivo):
            return
        
        try:
            with open(self.caminho_arquivo, 'r') as arquivo:
                dados = json.load(arquivo)
                for id_, info in dados.items():
                    if id_ in self.achievements:
                        if info.get("desbloqueada", False):
                            self.achievements[id_].desbloquear()
        except (json.JSONDecodeError, IOError) as erro:
            print(f"Erro ao carregar achievements: {erro}")
