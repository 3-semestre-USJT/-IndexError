import pygame

class EasterEggTeclado:
    def __init__(self, palavra_chave, caminho_imagem, funcao_audio=None, duracao_piscada=200):
        try:
            self.imagem = pygame.image.load(caminho_imagem).convert_alpha()
        except pygame.error:
            self.imagem = pygame.Surface((300, 400))
            self.imagem.fill((128, 0, 128))

        self.palavra_chave = palavra_chave.lower()
        self.buffer = ""
        self.mostrar = False
        self.tempo_inicial = 0
        self.duracao = duracao_piscada
        self.funcao_audio = funcao_audio 

    def registrar_tecla(self, evento):
        if evento.type == pygame.KEYDOWN:
            letra = evento.unicode.lower()
            
            if letra.isalpha(): 
                self.buffer += letra
                
                if len(self.buffer) > len(self.palavra_chave):
                    self.buffer = self.buffer[-len(self.palavra_chave):]
                
                if self.buffer == self.palavra_chave:
                    self.mostrar = True
                    self.tempo_inicial = pygame.time.get_ticks()
                    self.buffer = "" 
                
                    if self.funcao_audio:
                        self.funcao_audio() 

    def atualizar_e_desenhar(self, superficie_tela):
        if self.mostrar:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_inicial > self.duracao:
                self.mostrar = False
                return 

            pos_x = (superficie_tela.get_width() - self.imagem.get_width()) // 2
            pos_y = (superficie_tela.get_height() - self.imagem.get_height()) // 2
            
            superficie_tela.blit(self.imagem, (pos_x, pos_y))


class GerenciadorEasterEggs:
    def __init__(self):
        self.lista_eggs = []

    def adicionar(self, egg):
        # Adiciona um novo Easter Egg ao gerenciador
        self.lista_eggs.append(egg)

    def processar_eventos(self, evento):
        # No loop de eventos
        for egg in self.lista_eggs:
            egg.registrar_tecla(evento)

    def atualizar_e_desenhar(self, superficie_tela):
        # No render
        for egg in self.lista_eggs:
            egg.atualizar_e_desenhar(superficie_tela)
