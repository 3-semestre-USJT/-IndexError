"""
Módulo de Sistema de Animações Aprimoradas.

Utiliza pygame.sprite para gerenciar animações, efeitos de partículas e
transições mais fluidas no jogo.
"""

import pygame
import random
import math


class Particula(pygame.sprite.Sprite):
    """
    Representa uma partícula individual no sistema de partículas.
    
    Atributos:
        x, y: Posição da partícula
        vx, vy: Velocidade da partícula
        vida: Tempo de vida em frames
        vida_max: Tempo máximo de vida
        cor: Cor da partícula
    """
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 cor: tuple, vida: int = 30):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.cor = cor
        self.vida = vida
        self.vida_max = vida
        self.tamanho = 5
        
        # Cria a imagem da partícula
        self.atualizar_imagem()
    
    def atualizar_imagem(self):
        """Atualiza a imagem com base na vida restante."""
        # Fade out baseado na vida
        alpha = int((self.vida / self.vida_max) * 255)
        self.image = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)
        cor_com_alpha = (*self.cor, alpha)
        pygame.draw.circle(self.image, cor_com_alpha, (self.tamanho // 2, self.tamanho // 2), self.tamanho // 2)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
    
    def update(self):
        """Atualiza a posição e vida da partícula."""
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        self.atualizar_imagem()
        
        # Remove quando a vida acaba
        if self.vida <= 0:
            self.kill()


class GeradorParticulas:
    """
    Gerencia a criação e atualização de efeitos de partículas.
    """
    
    def __init__(self):
        """Inicializa o gerador de partículas."""
        self.grupo_particulas = pygame.sprite.Group()
    
    def criar_explosao(self, x: float, y: float, cor: tuple = (255, 100, 100), 
                       quantidade: int = 20, velocidade_max: float = 5.0):
        """
        Cria um efeito de explosão.
        
        Args:
            x, y: Posição da explosão
            cor: Cor das partículas
            quantidade: Número de partículas
            velocidade_max: Velocidade máxima das partículas
        """
        for _ in range(quantidade):
            angulo = random.uniform(0, 2 * math.pi)
            velocidade = random.uniform(0, velocidade_max)
            vx = velocidade * math.cos(angulo)
            vy = velocidade * math.sin(angulo)
            
            particula = Particula(x, y, vx, vy, cor, vida=random.randint(20, 40))
            self.grupo_particulas.add(particula)
    
    def criar_trail(self, x: float, y: float, cor: tuple = (0, 255, 100), 
                    quantidade: int = 5):
        """
        Cria um efeito de rastro (trail).
        
        Args:
            x, y: Posição
            cor: Cor do trail
            quantidade: Número de partículas
        """
        for _ in range(quantidade):
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 2)
            particula = Particula(x, y, vx, vy, cor, vida=15)
            self.grupo_particulas.add(particula)
    
    def atualizar(self):
        """Atualiza todas as partículas."""
        self.grupo_particulas.update()
    
    def desenhar(self, tela: pygame.Surface):
        """Desenha todas as partículas."""
        self.grupo_particulas.draw(tela)
    
    def obter_quantidade(self) -> int:
        """Retorna a quantidade de partículas ativas."""
        return len(self.grupo_particulas)
    
    def limpar(self):
        """Limpa todas as partículas."""
        self.grupo_particulas.empty()


class AnimadorTransicao:
    """
    Gerencia transições suaves entre estados/telas.
    """
    
    def __init__(self, duracao: int = 30):
        """
        Inicializa o animador de transição.
        
        Args:
            duracao: Duração da transição em frames
        """
        self.duracao = duracao
        self.progresso = 0
        self.ativa = False
        self.tipo_transicao = "fade"  # fade, slide_left, slide_right, etc
    
    def iniciar(self, tipo: str = "fade"):
        """Inicia uma transição."""
        self.ativa = True
        self.progresso = 0
        self.tipo_transicao = tipo
    
    def atualizar(self) -> bool:
        """
        Atualiza a transição.
        
        Returns:
            True se a transição terminou
        """
        if not self.ativa:
            return False
        
        self.progresso += 1
        
        if self.progresso >= self.duracao:
            self.ativa = False
            return True
        
        return False
    
    def obter_alpha(self) -> int:
        """Retorna o valor de alpha (0-255) baseado no progresso."""
        if self.tipo_transicao == "fade":
            return int((self.progresso / self.duracao) * 255)
        return 0
    
    def obter_offset_x(self) -> float:
        """Retorna o deslocamento X para transições slide."""
        progresso_norm = self.progresso / self.duracao
        
        if self.tipo_transicao == "slide_left":
            return -1280 * progresso_norm
        elif self.tipo_transicao == "slide_right":
            return 1280 * (1 - progresso_norm)
        
        return 0
    
    def esta_ativa(self) -> bool:
        """Verifica se a transição está ativa."""
        return self.ativa
    
    def desenhar_overlay_fade(self, tela: pygame.Surface):
        """Desenha um overlay de fade."""
        if not self.ativa or self.tipo_transicao != "fade":
            return
        
        overlay = pygame.Surface(tela.get_size())
        overlay.set_alpha(self.obter_alpha())
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))
