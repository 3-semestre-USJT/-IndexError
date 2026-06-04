import random 

# Dicionário e obter_simbolo (mantidos como você já fez)
REPRESENTACOES = {
    "NOT": ["NOT", "!", "¬", "~", "NÃO"],
    "OR": ["OR", "V", "||", "+", "OU"],
    "AND": ["AND", "^", "&&", "*", "E"], 
    "DIR": ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]
}

def obter_simbolo(categoria):
    return random.choice(REPRESENTACOES[categoria])

def sortear_desafio(nivel):
    s_not = obter_simbolo("NOT")
    s_or = obter_simbolo("OR")
    s_and = obter_simbolo("AND")
    todas = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]

    # Sorteia 3 direções únicas da lista 'todas'
    selecao = random.sample(todas, k=3)
    d1, d2, d3 = selecao[0], selecao[1], selecao[2]

    if nivel == 1:
        pergunta = f"{s_not} {d1}"
        resposta = [d for d in todas if d != d1]

    elif nivel == 2:
        pergunta = f"{d1} {s_or} {d2}"
        resposta = list(set([d1, d2])) # set remove duplicatas se d1 == d2

    elif nivel == 3:
        pergunta = f"{s_not}({d1} {s_or} {d2})"
        resposta = [d for d in todas if d != d1 and d != d2]

    elif nivel == 4: 
        pergunta = f"{d1} {s_and} {s_not} {d2}"
        resposta = [d1] if d1 != d2 else []

    elif nivel == 5:
        # Mistura complexa: NOT(d1 OR d2) AND NOT(d3)
        pergunta = f"{s_not}({d1} {s_or} {d2}) {s_and} {s_not} {d3}"
        # A resposta são direções que não sejam d1, nem d2, nem d3
        resposta = [d for d in todas if d not in [d1, d2, d3]]

    # Validação anti exressão impossível
    if not resposta:
        return sortear_desafio(nivel)

    return {
        "texto": pergunta,
        "corretas": resposta
    }