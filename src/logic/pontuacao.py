import json
import os
from datetime import datetime, timedelta


class GerenciadorPontuacao:
    """
    Responsável por toda a lógica numérica, multiplicadores, vidas e persistência de recordes.
    Gerencia pontuação, combo, sistema de vidas e ranking top 3.
    """
    
    def __init__(self):
        # Gerenciamento de caminhos para a pasta 'data'
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        raiz_projeto = os.path.dirname(os.path.dirname(base_dir))
        self.caminho_ranking = os.path.join(raiz_projeto, "data", "ranking.json")
        self.caminho_desafio_diario = os.path.join(raiz_projeto, "data", "desafio_diario.json")
        
        # Estado atual da partida
        self.score = 0
        self.combo = 0
        self.multiplicador = 1
        self.vidas = 3  # Sistema de vidas
        self.acertos_totais = 0  # Total de acertos na partida
        self.erros_totais = 0  # Total de erros na partida
        self.tempo_total_partida = 0.0  # Tempo total de jogo
        self.dificuldade_atual = "NORMAL"  # Rastreia a dificuldade da partida atual
        
        # Configurações de Balanceamento
        self.PONTOS_BASE = 100
        self.ACERTOS_PARA_LEVEL_UP = 5
        self.TEMPO_INICIAL = 15.0
        self.TEMPO_MINIMO = 5.0
        self.VIDAS_INICIAIS = 3  # Número de vidas no início
        
        # Carrega o ranking separado por dificuldade e define o high_score
        self.ranking = self.carregar_ranking()
        self.high_score = self.obter_high_score_dificuldade("NORMAL")
        
        # Desafio diário
        self.desafio_diario_completado = False
        self.verificar_desafio_diario()

    def registrar_acerto(self, multiplicador_powerup: float = 1.0):
        """
        Incrementa pontos e gerencia o multiplicador de combo.
        
        Args:
            multiplicador_powerup: Multiplicador adicional de powerup
        """
        self.combo += 1
        self.acertos_totais += 1
        
        # A cada N acertos, o multiplicador aumenta (1x -> 2x -> 3x...)
        if self.combo % self.ACERTOS_PARA_LEVEL_UP == 0:
            self.multiplicador += 1
        
        # Calcula pontos com multiplicador base e powerup
        pontos_ganhos = int(self.PONTOS_BASE * self.multiplicador * multiplicador_powerup)
        self.score += pontos_ganhos

    def registrar_erro(self):
        """Registra um erro e reduz vidas."""
        self.combo = 0  # Reseta combo ao errar
        self.erros_totais += 1
        self.vidas -= 1

    def obter_vidas(self) -> int:
        """Retorna o número de vidas atual."""
        return self.vidas

    def perdeu_todas_vidas(self) -> bool:
        """Verifica se o jogador perdeu todas as vidas."""
        return self.vidas <= 0

    def ganhar_vida(self) -> bool:
        """
        Ganha uma vida (máximo VIDAS_INICIAIS).
        
        Returns:
            True se ganhou vida, False se já estava no máximo
        """
        if self.vidas < self.VIDAS_INICIAIS:
            self.vidas += 1
            return True
        return False

    def calcular_tempo_limite(self) -> float:
        """
        Calcula o tempo disponível para a próxima jogada.
        A dificuldade aumenta (tempo diminui) conforme o score sobe.
        Reduz 1.5s a cada 1000 pontos acumulados
        """
        reducao = (self.score // 1000) * 1.5
        tempo_calculado = self.TEMPO_INICIAL - reducao
        
        return max(tempo_calculado, self.TEMPO_MINIMO)

    def carregar_ranking(self) -> dict:
        """
        Lê o ranking do arquivo JSON separado por dificuldade.
        Retorna dicionário padrão se não existir.
        """
        if not os.path.exists(self.caminho_ranking):
            return {
                "FACIL": [
                    {"nome": "---", "pontos": 0},
                    {"nome": "---", "pontos": 0},
                    {"nome": "---", "pontos": 0}
                ],
                "NORMAL": [
                    {"nome": "---", "pontos": 0},
                    {"nome": "---", "pontos": 0},
                    {"nome": "---", "pontos": 0}
                ],
                "DIFICIL": [
                    {"nome": "---", "pontos": 0},
                    {"nome": "---", "pontos": 0},
                    {"nome": "---", "pontos": 0}
                ]
            }
            
        try:
            with open(self.caminho_ranking, 'r') as arquivo:
                dados = json.load(arquivo)
                # Se for o formato antigo (lista única), converter para novo formato
                # Mantém o ranking antigo apenas em NORMAL, inicializa outros vazios
                if isinstance(dados, list):
                    return {
                        "FACIL": [
                            {"nome": "---", "pontos": 0},
                            {"nome": "---", "pontos": 0},
                            {"nome": "---", "pontos": 0}
                        ],
                        "NORMAL": dados,
                        "DIFICIL": [
                            {"nome": "---", "pontos": 0},
                            {"nome": "---", "pontos": 0},
                            {"nome": "---", "pontos": 0}
                        ]
                    }
                return dados
        except (json.JSONDecodeError, IOError):
            return {
                "FACIL": [{"nome": "---", "pontos": 0}] * 3,
                "NORMAL": [{"nome": "---", "pontos": 0}] * 3,
                "DIFICIL": [{"nome": "---", "pontos": 0}] * 3
            }
    
    def obter_high_score_dificuldade(self, dificuldade: str) -> int:
        """
        Retorna o high score para uma dificuldade específica.
        
        Args:
            dificuldade: "FACIL", "NORMAL", ou "DIFICIL"
        
        Returns:
            High score da dificuldade especificada
        """
        if dificuldade in self.ranking and len(self.ranking[dificuldade]) > 0:
            return self.ranking[dificuldade][0]['pontos']
        return 0

    def verificar_novo_recorde(self) -> bool:
        """Retorna True se o score atual entrar no Top 3 da dificuldade atual"""
        dificuldade = self.dificuldade_atual
        if dificuldade not in self.ranking:
            return True
        return self.score > self.ranking[dificuldade][-1]['pontos']

    def salvar_no_ranking(self, nome_iniciais):
        """
        Adiciona o novo recorde na dificuldade atual, ordena o Top 3 e salva no disco.
        """
        dificuldade = self.dificuldade_atual
        
        # Adiciona a nova pontuação à lista da dificuldade atual
        self.ranking[dificuldade].append({"nome": nome_iniciais.upper(), "pontos": self.score})
        
        # Ordena do maior para o menor e mantém apenas os 3 melhores
        self.ranking[dificuldade] = sorted(self.ranking[dificuldade], key=lambda x: x['pontos'], reverse=True)[:3]
        
        # Atualiza o high_score histórico para bater com o novo 1º lugar da dificuldade atual
        self.high_score = self.ranking[dificuldade][0]['pontos']
        
        try:
            # Garante que a pasta 'data' existe antes de salvar
            os.makedirs(os.path.dirname(self.caminho_ranking), exist_ok=True)
            with open(self.caminho_ranking, 'w') as arquivo:
                json.dump(self.ranking, arquivo, indent=4)
        except IOError as erro:
            print(f"Erro ao salvar ranking: {erro}")

    def resetar_partida(self, nova_dificuldade_config: dict = None, dificuldade: str = "NORMAL"):
        """
        Reseta os valores para uma nova rodada.
        Mantém o recorde intacto.
        
        Args:
            nova_dificuldade_config: Configurações de dificuldade opcional
            dificuldade: Nome da dificuldade ("FACIL", "NORMAL", "DIFICIL")
        """
        self.score = 0
        self.combo = 0
        self.multiplicador = 1
        self.vidas = self.VIDAS_INICIAIS
        self.acertos_totais = 0
        self.erros_totais = 0
        self.tempo_total_partida = 0.0
        self.dificuldade_atual = dificuldade
        
        # Atualiza o high_score para a dificuldade atual
        self.high_score = self.obter_high_score_dificuldade(dificuldade)
        
        # Aplica configurações de dificuldade se fornecidas
        if nova_dificuldade_config:
            self.ACERTOS_PARA_LEVEL_UP = nova_dificuldade_config.get("acertos_para_levelup", 5)
            self.TEMPO_INICIAL = nova_dificuldade_config.get("tempo_inicial", 15.0)
            self.TEMPO_MINIMO = nova_dificuldade_config.get("tempo_minimo", 5.0)

    def verificar_desafio_diario(self):
        """Verifica se o desafio diário foi completado hoje."""
        try:
            if os.path.exists(self.caminho_desafio_diario):
                with open(self.caminho_desafio_diario, 'r') as arquivo:
                    dados = json.load(arquivo)
                    data_ultimo = datetime.fromisoformat(dados.get("data", ""))
                    hoje = datetime.now().date()
                    
                    # Se for o mesmo dia, mantém o status
                    if data_ultimo.date() == hoje:
                        self.desafio_diario_completado = dados.get("completado", False)
                    else:
                        # Novo dia, reseta o desafio
                        self.desafio_diario_completado = False
        except (json.JSONDecodeError, IOError, ValueError):
            self.desafio_diario_completado = False

    def completar_desafio_diario(self):
        """Marca o desafio diário como completado."""
        self.desafio_diario_completado = True
        try:
            os.makedirs(os.path.dirname(self.caminho_desafio_diario), exist_ok=True)
            dados = {
                "data": datetime.now().isoformat(),
                "completado": True,
                "score": self.score,
                "combo_maximo": self.combo
            }
            with open(self.caminho_desafio_diario, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)
        except IOError as erro:
            print(f"Erro ao salvar desafio diário: {erro}")

    def obter_taxa_acerto(self) -> float:
        """
        Calcula a taxa de acerto da partida.
        
        Returns:
            Percentual de acertos (0-100)
        """
        total = self.acertos_totais + self.erros_totais
        if total == 0:
            return 0.0
        return (self.acertos_totais / total) * 100
