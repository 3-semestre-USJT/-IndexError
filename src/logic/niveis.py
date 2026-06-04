"""
Módulo de Sistema de Níveis e XP.

Gerencia o progresso do jogador através de níveis, XP e recompensas.
"""

import json
import os


class GerenciadorNiveis:
    """Gerencia o sistema de níveis e XP do jogador."""
    
    # Configurações de XP por nível
    XP_BASE = 100
    XP_MULTIPLICADOR = 1.5  # Cada nível requer 1.5x mais XP que o anterior
    
    def __init__(self):
        """Inicializa o gerenciador de níveis."""
        self.nivel = 1
        self.xp_atual = 0
        self.xp_total = 0
        self.caminho_arquivo = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "niveis.json"
        )
        self.carregar_niveis()
    
    def obter_xp_para_nivel(self, nivel: int) -> int:
        """
        Calcula o XP necessário para atingir um nível específico.
        
        Args:
            nivel: Nível alvo
            
        Returns:
            XP necessário
        """
        return int(self.XP_BASE * (self.XP_MULTIPLICADOR ** (nivel - 1)))
    
    def obter_xp_para_proximo_nivel(self) -> int:
        """
        Calcula o XP necessário para o próximo nível.
        
        Returns:
            XP necessário
        """
        return self.obter_xp_para_nivel(self.nivel + 1)
    
    def adicionar_xp(self, quantidade: int) -> bool:
        """
        Adiciona XP ao jogador e verifica se subiu de nível.
        
        Args:
            quantidade: Quantidade de XP a adicionar
            
        Returns:
            True se subiu de nível, False caso contrário
        """
        self.xp_atual += quantidade
        self.xp_total += quantidade
        
        subiu_nivel = False
        while self.xp_atual >= self.obter_xp_para_proximo_nivel():
            self.xp_atual -= self.obter_xp_para_proximo_nivel()
            self.nivel += 1
            subiu_nivel = True
        
        if subiu_nivel:
            self.salvar_niveis()
        
        return subiu_nivel
    
    def obter_percentual_nivel(self) -> float:
        """
        Calcula o percentual de progresso para o próximo nível.
        
        Returns:
            Percentual (0-100)
        """
        xp_necessario = self.obter_xp_para_proximo_nivel()
        if xp_necessario == 0:
            return 100.0
        return (self.xp_atual / xp_necessario) * 100
    
    def salvar_niveis(self):
        """Salva o progresso de níveis no arquivo JSON."""
        try:
            os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
            dados = {
                "nivel": self.nivel,
                "xp_atual": self.xp_atual,
                "xp_total": self.xp_total
            }
            with open(self.caminho_arquivo, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)
        except IOError as erro:
            print(f"Erro ao salvar níveis: {erro}")
    
    def carregar_niveis(self):
        """Carrega o progresso de níveis do arquivo JSON."""
        if not os.path.exists(self.caminho_arquivo):
            return
        
        try:
            with open(self.caminho_arquivo, 'r') as arquivo:
                dados = json.load(arquivo)
                self.nivel = dados.get("nivel", 1)
                self.xp_atual = dados.get("xp_atual", 0)
                self.xp_total = dados.get("xp_total", 0)
        except (json.JSONDecodeError, IOError) as erro:
            print(f"Erro ao carregar níveis: {erro}")
    
    def resetar_niveis(self):
        """Reseta o progresso de níveis."""
        self.nivel = 1
        self.xp_atual = 0
        self.xp_total = 0
        self.salvar_niveis()
