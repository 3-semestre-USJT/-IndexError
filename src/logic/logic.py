from .gerador import sortear_desafio # O ponto significa "nesta mesma pasta"
from .validador import verificar_resposta # O ponto significa "nesta mesma pasta"

def obter_novo_desafio(combo):
    # Calcula o nível (1 a 5) a cada 5 acertos (combo)
    nivel_atual = min((combo // 5) + 1, 5)
    return sortear_desafio(nivel=nivel_atual)

def validar_jogada(tecla, corretas):
    # Faz a ponte com o validador
    return verificar_resposta(tecla, corretas)

