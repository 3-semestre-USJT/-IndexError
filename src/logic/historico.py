"""
Módulo de Histórico de Partidas.

Armazena e gerencia o histórico das últimas partidas jogadas, incluindo
estatísticas e análise de progresso.
"""

import json
import os
from datetime import datetime


class RegistroPartida:
    """
    Representa uma partida individual no histórico.
    
    Atributos:
        timestamp: Data/hora da partida
        score: Pontuação final
        combo_maximo: Maior combo alcançado
        dificuldade: Nível de dificuldade
        duracao_segundos: Duração da partida
        acertos: Quantidade de acertos
        erros: Quantidade de erros
    """
    
    def __init__(self, score: int, combo_maximo: int, dificuldade: str,
                 duracao: float, acertos: int, erros: int):
        self.timestamp = datetime.now().isoformat()
        self.score = score
        self.combo_maximo = combo_maximo
        self.dificuldade = dificuldade
        self.duracao_segundos = duracao
        self.acertos = acertos
        self.erros = erros
    
    def para_dict(self) -> dict:
        """Converte o registro para dicionário."""
        return {
            "timestamp": self.timestamp,
            "score": self.score,
            "combo_maximo": self.combo_maximo,
            "dificuldade": self.dificuldade,
            "duracao_segundos": self.duracao_segundos,
            "acertos": self.acertos,
            "erros": self.erros
        }
    
    @staticmethod
    def de_dict(dados: dict) -> 'RegistroPartida':
        """Cria um registro a partir de um dicionário."""
        registro = RegistroPartida(
            score=dados["score"],
            combo_maximo=dados["combo_maximo"],
            dificuldade=dados["dificuldade"],
            duracao=dados["duracao_segundos"],
            acertos=dados["acertos"],
            erros=dados["erros"]
        )
        registro.timestamp = dados["timestamp"]
        return registro


class GerenciadorHistorico:
    """Gerencia o histórico de partidas do jogador."""
    
    LIMITE_PARTIDAS = 50  # Mantém no máximo 50 partidas no histórico
    
    def __init__(self):
        """Inicializa o gerenciador de histórico."""
        self.partidas = []
        self.caminho_arquivo = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "historico_partidas.json"
        )
        self.carregar_historico()
    
    def registrar_partida(self, score: int, combo_maximo: int, dificuldade: str,
                         duracao: float, acertos: int, erros: int):
        """
        Registra uma nova partida no histórico.
        
        Args:
            score: Pontuação obtida
            combo_maximo: Maior combo da partida
            dificuldade: Nível de dificuldade
            duracao: Duração da partida em segundos
            acertos: Total de acertos
            erros: Total de erros
        """
        registro = RegistroPartida(score, combo_maximo, dificuldade, duracao, acertos, erros)
        self.partidas.insert(0, registro)  # Insere no início (mais recente)
        
        # Limita o histórico ao máximo de partidas
        if len(self.partidas) > self.LIMITE_PARTIDAS:
            self.partidas = self.partidas[:self.LIMITE_PARTIDAS]
        
        self.salvar_historico()
    
    def obter_ultimas(self, quantidade: int = 10) -> list:
        """Retorna as últimas N partidas."""
        return self.partidas[:quantidade]
    
    def obter_estatisticas_gerais(self) -> dict:
        """
        Calcula estatísticas gerais do histórico.
        
        Returns:
            Dicionário com estatísticas como média de score, melhor combo, etc.
        """
        if not self.partidas:
            return {
                "total_partidas": 0,
                "score_medio": 0,
                "combo_maximo_geral": 0,
                "acertos_totais": 0,
                "taxa_acerto": 0.0
            }
        
        total = len(self.partidas)
        scores = [p.score for p in self.partidas]
        combos = [p.combo_maximo for p in self.partidas]
        acertos_totais = sum(p.acertos for p in self.partidas)
        erros_totais = sum(p.erros for p in self.partidas)
        
        taxa_acerto = (acertos_totais / (acertos_totais + erros_totais) * 100) if (acertos_totais + erros_totais) > 0 else 0
        
        return {
            "total_partidas": total,
            "score_medio": sum(scores) / total,
            "score_maximo": max(scores),
            "score_minimo": min(scores),
            "combo_maximo_geral": max(combos),
            "acertos_totais": acertos_totais,
            "erros_totais": erros_totais,
            "taxa_acerto": taxa_acerto
        }
    
    def salvar_historico(self):
        """Salva histórico no arquivo JSON."""
        try:
            os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
            dados = [p.para_dict() for p in self.partidas]
            with open(self.caminho_arquivo, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)
        except IOError as erro:
            print(f"Erro ao salvar histórico: {erro}")
    
    def carregar_historico(self):
        """Carrega histórico do arquivo JSON."""
        if not os.path.exists(self.caminho_arquivo):
            return
        
        try:
            with open(self.caminho_arquivo, 'r') as arquivo:
                dados = json.load(arquivo)
                self.partidas = [RegistroPartida.de_dict(d) for d in dados]
        except (json.JSONDecodeError, IOError) as erro:
            print(f"Erro ao carregar histórico: {erro}")
    
    def limpar_historico(self):
        """Limpa todo o histórico."""
        self.partidas = []
        self.salvar_historico()
