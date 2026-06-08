# FEATURES - Documentação Técnica

##  Sumário das Features Implementadas

Este documento descreve todas as features implementadas no jogo ! IndexError.

---

## 1. Intro Melhorada com Animações 

### Integrado em: `main.py`

**Descrição:** Intro animada com fade-in, texto aparecendo letra por letra e partículas.

**Funcionalidades:**
- Fade-in do logo TupãStudios
- Texto "! INDEXERROR" aparecendo letra por letra
- Partículas animadas no fundo
- Transição suave para o menu principal
- Música própria da intro
- Pode pular com ESPAÇO

---

## 2. Modo Time Attack 

### Integrado em: `main.py`

**Descrição:** Modo de jogo onde você tem 60 segundos para completar o máximo de desafios.

**Funcionalidades:**
- 60 segundos de tempo fixo
- Conta desafios completados e combo atual
- Erros resetam o combo e os pontos
- Powerups funcionam normalmente
- HUD dedicado mostrando progresso
- Pausa com ESC
- Game over quando tempo acaba

---

## 3. Tutorial Interativo 

### Integrado em: `main.py`

**Descrição:** Tutorial interativo com opção de In-Game ou Web.

**Funcionalidades:**
- Menu de seleção (In-Game ou Web)
- 7 passos explicativos no In-Game
- Texto aparece letra por letra automaticamente
- Pode pular com ESPAÇO
- Caixa estilizada no fundo da tela
- Sem limite de tempo no tutorial
- Encerra quando acabarem as frases ou ao sair para o menu
- Ensina: movimento, acertos, vidas, powerups, pausa

---

## 4. Desafios Diários Infinitos 

### Integrado em: `main.py` e `src/ui/menus.py`

**Descrição:** Sistema de desafios diários que rotacionam baseados na data do ano.

**Funcionalidades:**
- 15 desafios diferentes disponíveis
- 5 desafios mostrados por dia
- Rotacionam baseados no dia do ano (1-365)
- Resetam automaticamente a cada dia
- Janelinha no menu principal mostrando 3 desafios
- Tela dedicada com todos os 5 desafios do dia
- Descrições mais detalhadas dos desafios

---

## 5. Sistema de Popup de Conquistas 

### Integrado em: `main.py`

**Descrição:** Popups estilo Xbox ao desbloquear conquistas.

**Funcionalidades:**
- Popup aparece quando conquista é desbloqueada
- Duração de 3 segundos
- Som de notificação
- Design estilizado com fundo e borda

---

## 6. Sistema de Popup de Powerups 

### Integrado em: `main.py`

**Descrição:** Popups ao obter powerups durante o jogo.

**Funcionalidades:**
- Popup aparece quando powerup é obtido
- Duração de 2 segundos
- Som de notificação
- Mapeamento de tipos para nomes amigáveis

---

## 7. HUD Melhorado 

### Integrado em: `main.py`

**Descrição:** Painel com fundo para melhor visibilidade de informações do jogo.

**Funcionalidades:**
- Fundo escuro com borda colorida
- Mostra vidas, score, combo, tempo
- Mostra powerups disponíveis
- Design consistente entre modos
- Posicionado no canto superior esquerdo

---

## 8. Sistema de Dificuldade 

### Arquivo: `src/logic/dificuldade.py`

**Descrição:** Sistema de 3 níveis de dificuldade com configurações distintas.

**Níveis:**
- **FÁCIL**: Tempo inicial 20s, multiplicador mais lento, 3 acertos para level-up
- **NORMAL**: Tempo inicial 15s, multiplicador padrão, 5 acertos para level-up
- **DIFÍCIL**: Tempo inicial 10s, multiplicador mais rápido, 7 acertos para level-up

---

## 8.1 Sistema de Ranking por Dificuldade 

### Arquivo: `src/logic/pontuacao.py`

**Descrição:** Sistema de ranking separado por nível de dificuldade para pontuação justa.

**Funcionalidades:**
- Ranking separado para FÁCIL, NORMAL e DIFÍCIL
- Cada dificuldade tem seu próprio Top 3
- High score rastreado por dificuldade
- Tela de Game Over mostra ranking da dificuldade atual
- Conversão automática de ranking antigo (formato único) para novo formato
- Pontuação justa: jogadores de diferentes níveis competem separadamente

---

## 8.2 Sistema de Achievements 

### Arquivo: `src/logic/achievements.py`

**Descrição:** Sistema de badges/conquistas desbloqueáveis.

**Conquistas Disponíveis:**
- Combo Mestre (500+)
- Combo Supremo (1000+)
- Velocista (< 2s)
- Recordista
- 20/50 Acertos
- Perfeição (10 acertos sem errar)

---

## 9. Histórico de Partidas 

### Arquivo: `src/logic/historico.py`

**Descrição:** Rastreia as últimas 50 partidas com estatísticas detalhadas.

**Dados Rastreados:**
- Score, Combo máximo, Dificuldade
- Duração, Acertos, Erros
- Data/Hora de cada partida

---

## 10. Teclado Customizável 

### Arquivo: `src/logic/controles.py`

**Descrição:** Sistema de remapeamento de teclas.

**Ações Customizáveis:**
- CIMA, BAIXO, ESQUERDA, DIREITA
- MENU_UP, MENU_DOWN
- SELECIONAR, VOLTAR, PAUSAR

---

## 11. Sistema de Powerups 

### Arquivo: `src/logic/powerups.py`

**Descrição:** Sistema de powerups para melhorar desempenho durante o jogo.

**Tipos de Powerups:**
- **Tempo Extra**: +5 segundos
- **Congelar Multiplicador**: Mantém mult por 30s
- **Remover Opção**: Remove 1 opção errada
- **Escudo**: Protege de 1 erro
- **Multiplicador x2**: Dobra pontos por 15s

---

## 12. Sistema de Vidas 

### Integrado em: `src/logic/pontuacao.py`

**Descrição:** Jogador começa com 3 vidas em vez de game over na primeira falha.

**Funcionalidades:**
- Começa com 3 vidas
- Perde 1 vida por erro
- Game over quando vidas = 0
- Pode ganhar vida com powerups

---

## 13. Pausa no Jogo 

### Arquivo: `src/ui/pausa.py`

**Descrição:** Menu de pausa com opção de retomar ou sair.

**Funcionalidades:**
- Pausa o jogo com ESC (configurável)
- Menu com "Retomar" e "Sair"
- Navegação com setas

---

## 14. Sistema de Níveis e XP 

### Arquivo: `src/logic/niveis.py`

**Descrição:** Sistema de progressão de jogador com XP e níveis.

**Funcionalidades:**
- XP ganho ao acertar (10 * multiplicador)
- Níveis progressivos (cada nível requer 1.5x mais XP)
- Barra de XP visual no HUD principal
- Popup ao subir de nível
- Persistência em JSON (data/niveis.json)

**Uso:**
```python
from src.logic.niveis import GerenciadorNiveis

niveis = GerenciadorNiveis()
xp_ganho = 10 * multiplicador
if niveis.adicionar_xp(xp_ganho):
    print(f"Subiu para nível {niveis.nivel}!")
percentual = niveis.obter_percentual_nivel()
```

---

## 15. Sistema de Combo Visual 

### Integrado em: `main.py`

**Descrição:** Efeitos visuais ao aumentar o combo.

**Funcionalidades:**
- Efeitos visuais a cada 5 de combo
- Partículas coloridas baseadas no valor do combo
- Explosões visuais no centro da tela
- Cores mudam conforme o combo aumenta

---

## 16. Opção Removida Visual 

### Integrado em: `main.py` e `src/ui/tela_jogo.py`

**Descrição:** Visualização da opção removida pelo powerup.

**Funcionalidades:**
- Opções removidas aparecem em vermelho com `[X]` prefixo
- Mostradas abaixo do tempo na tela de jogo
- Feedback visual claro de quais opções foram removidas

---

## 17. Powerups Não Acumulando 

### Integrado em: `main.py`

**Descrição:** Powerups são limpos automaticamente ao terminar partida.

**Funcionalidades:**
- `gerenciador_powerups.limpar_powerups()` chamado ao terminar jogo
- Powerups não persistem entre partidas
- Reset automático ao entrar em GAME_OVER

---

## 18. Música no Time Attack 

### Integrado em: `main.py`

**Descrição:** Música de gameplay toca no modo Time Attack.

**Funcionalidades:**
- Música inicia ao entrar no TIME_ATTACK
- Mesma música do modo normal
- Controle de música funciona normalmente

---

## 19. UI/UX Conquistas - Paginação 

### Integrado em: `main.py`

**Descrição:** Sistema de paginação para tela de conquistas.

**Funcionalidades:**
- 8 conquistas por página
- Navegação com teclas A (anterior) e D (próximo)
- Indicador de página "Página X/Y"
- Textos centralizados verticalmente
- Instruções de navegação visíveis

---

## 20. UI/UX Desafios Diários - Paginação 

### Integrado em: `main.py`

**Descrição:** Sistema de paginação para tela de desafios diários.

**Funcionalidades:**
- 5 desafios por página
- Navegação com teclas A (anterior) e D (próximo)
- Indicador de página "Página X/Y"
- Textos centralizados verticalmente
- Instruções de navegação visíveis
- Dados coletados corretamente (pontos, combo, acertos, partidas, etc.)

---

## 21. Tutorial 

### Arquivo: `src/ui/tutorial.py`

**Descrição:** Tutorial interativo de 6 etapas ensinando mecânicas.

**Etapas:**
1. Bem-vindo
2. Mecânica do Jogo
3. Sistema de Combo
4. Vidas e Dificuldade
5. Powerups
6. Início do Jogo

---

## 15. Animações Aprimoradas 

### Arquivo: `src/logic/animacoes.py`

**Descrição:** Sistema profissional de partículas e transições.

**Componentes:**
- **Partículas**: Efeitos de explosão e trail
- **Animador de Transição**: Fades e slides suaves

---

##  Estrutura de Dados Persistentes

Os seguintes arquivos são salvos em `data/`:

```
data/
├── ranking.json                 # Top 3 recordistas
├── achievements.json            # Conquistas desbloqueadas
├── historico_partidas.json      # Últimas 50 partidas
├── controles.json              # Controles customizados
└── desafio_diario.json         # Status do desafio diário
```

---

##  Menu Principal

O menu principal possui 5 opções:
1. **JOGAR** - Inicia o jogo normal com seleção de dificuldade
2. **CONFIGURACOES** - Configurações de resolução, música, som, controles, histórico, conquistas, desafios
3. **TUTORIAL** - Tutorial interativo (In-Game ou Web)
4. **SAIR** - Fecha o jogo
5. **TIME ATTACK** - Modo de 60 segundos para completar desafios (exibido como texto)

### UI/UX Melhorada
- **Botões Visuais**: Os botões do menu principal agora utilizam imagens (Play_of.png, Config_of.png, Quit_of.png) posicionadas no lado esquerdo da tela
- **Mão Seletora**: Uma mãozinha seletora (mao_seletora.png) indica a opção atualmente selecionada
- **Layout Responsivo**: Os botões são escalonados proporcionalmente ao tamanho da tela
- **TIME ATTACK**: Exibido como texto entre Tutorial e Config, já que não possui imagem específica
- **Navegação**: Suporte a mouse (hover e clique) e teclado (setas e ENTER)

---

##  Notas de Desenvolvimento

- Todos os módulos têm comentários profissionais em português
- Código segue PEP 8
- Uso de type hints para melhor legibilidade
- Persistência de dados em JSON
- Tratamento de exceções apropriado
- Fullscreen como padrão ao abrir o jogo

### Arquivo: `src/logic/dificuldade.py`

**Descrição:** Sistema de 3 níveis de dificuldade com configurações distintas.

**Níveis:**
- **FÁCIL**: Tempo inicial 20s, multiplicador mais lento, 3 acertos para level-up
- **NORMAL**: Tempo inicial 15s, multiplicador padrão, 5 acertos para level-up  
- **DIFÍCIL**: Tempo inicial 10s, multiplicador mais rápido, 7 acertos para level-up

**Uso:**
```python
from src.logic.dificuldade import GerenciadorDificuldade, NivelDificuldade

gerenciador = GerenciadorDificuldade()
gerenciador.definir_dificuldade(NivelDificuldade.DIFICIL)
config = gerenciador.obter_config()
print(config.tempo_inicial)  # 10.0
```

---

## 2. Sistema de Achievements 

### Arquivo: `src/logic/achievements.py`

**Descrição:** Sistema de badges/conquistas desbloqueáveis.

**Conquistas Disponíveis:**
- Combo Mestre (500+)
- Combo Supremo (1000+)
- Velocista (< 2s)
- Recordista
- 20/50 Acertos
- Perfeição (10 acertos sem errar)
- E mais...

**Uso:**
```python
from src.logic.achievements import GerenciadorAchievements

achievements = GerenciadorAchievements()
achievements.desbloquear("combo_500")
total = achievements.obter_total_desbloqueadas()
percentual = achievements.obter_percentual_desbloqueio()
```

---

## 3. Histórico de Partidas 

### Arquivo: `src/logic/historico.py`

**Descrição:** Rastreia as últimas 50 partidas com estatísticas detalhadas.

**Dados Rastreados:**
- Score, Combo máximo, Dificuldade
- Duração, Acertos, Erros
- Data/Hora de cada partida

**Uso:**
```python
from src.logic.historico import GerenciadorHistorico

historico = GerenciadorHistorico()
historico.registrar_partida(
    score=5000,
    combo_maximo=150,
    dificuldade="NORMAL",
    duracao=45.5,
    acertos=30,
    erros=2
)

stats = historico.obter_estatisticas_gerais()
```

---

## 4. Teclado Customizável ⌨

### Arquivo: `src/logic/controles.py`

**Descrição:** Sistema de remapeamento de teclas.

**Ações Customizáveis:**
- CIMA, BAIXO, ESQUERDA, DIREITA
- MENU_UP, MENU_DOWN
- SELECIONAR, VOLTAR, PAUSAR

**Uso:**
```python
from src.logic.controles import MapeadorControles
import pygame

mapeador = MapeadorControles()
acao = mapeador.verificar_acao(evento.key)  # Retorna ação ou None
nome_tecla = mapeador.obter_nome_tecla(pygame.K_w)  # "W"
mapeador.remapear("CIMA", [pygame.K_UP, pygame.K_w])
mapeador.resetar_padrao()
```

---

## 5. Desafios Diários 

### Integrado em: `src/logic/pontuacao.py`

**Descrição:** Um desafio especial que reseta a cada dia.

**Funcionalidades:**
- Reseta automaticamente à meia-noite
- Rastreia se foi completado
- Salva em `data/desafio_diario.json`

**Uso:**
```python
sistema_pontos = GerenciadorPontuacao()
sistema_pontos.verificar_desafio_diario()
if not sistema_pontos.desafio_diario_completado:
    print("Complete o desafio diário!")
    sistema_pontos.completar_desafio_diario()
```

---

## 6. Sistema de Powerups 

### Arquivo: `src/logic/powerups.py`

**Descrição:** Sistema de powerups para melhorar desempenho durante o jogo.

**Tipos de Powerups:**
- **Tempo Extra**: +5 segundos
- **Congelar Multiplicador**: Mantém mult por 30s
- **Remover Opção**: Remove 1 opção errada
- **Escudo**: Protege de 1 erro
- **Multiplicador x2**: Dobra pontos por 15s

**Uso:**
```python
from src.logic.powerups import GerenciadorPowerups, TipoPowerup

powerups = GerenciadorPowerups()
if powerups.deveria_aparecer_powerup():
    tipo = powerups.gerar_powerup_aleatorio()
    powerups.adicionar_powerup(tipo)

powerup_usado = powerups.usar_powerup(0, tempo_atual)
powerups.atualizar_powerups(tempo_atual)
```

---

## 7. Sistema de Vidas 

### Integrado em: `src/logic/pontuacao.py`

**Descrição:** Jogador começa com 3 vidas em vez de game over na primeira falha.

**Funcionalidades:**
- Começa com 3 vidas
- Perde 1 vida por erro
- Game over quando vidas = 0
- Pode ganhar vida com powerups

**Uso:**
```python
sistema_pontos = GerenciadorPontuacao()
print(sistema_pontos.obter_vidas())  # 3

# Ao errar
sistema_pontos.registrar_erro()
print(sistema_pontos.obter_vidas())  # 2

if sistema_pontos.perdeu_todas_vidas():
    print("Game Over!")
```

---

## 8. Pausa no Jogo 

### Arquivo: `src/ui/pausa.py`

**Descrição:** Menu de pausa com opção de retomar ou sair.

**Funcionalidades:**
- Pausa o jogo com ESC (configurável)
- Menu com "Retomar" e "Sair"
- Navegação com setas

**Uso:**
```python
from src.ui.pausa import exibir_menu_pausa

# No loop de eventos
if evento.key == pygame.K_ESCAPE and estado == 'jogando':
    estado = 'pausado'
    opcao_pausa = 0

# Ao renderizar
if estado == 'pausado':
    exibir_menu_pausa(tela, desenhar_texto, fontes, opcao_pausa)
```

---

## 9. Tutorial Interativo 

### Arquivo: `src/ui/tutorial.py`

**Descrição:** Tutorial interativo de 6 etapas ensinando mecânicas.

**Etapas:**
1. Bem-vindo
2. Mecânica do Jogo
3. Sistema de Combo
4. Vidas e Dificuldade
5. Powerups
6. Início do Jogo

**Uso:**
```python
from src.ui.tutorial import GerenciadorTutorial, exibir_tutorial

tutorial = GerenciadorTutorial()
tutorial.iniciar_tutorial()

# No loop
if estado == 'tutorial':
    exibir_tutorial(tela, desenhar_texto, fontes, tutorial)
    
    if evento.key == pygame.K_SPACE:
        if not tutorial.proximo_passo():
            estado = 'menu'  # Tutorial concluído
```

---

## 8. Sistema de Achievements �

### Arquivo: `src/logic/animacoes.py`

**Descrição:** Sistema profissional de partículas e transições.

**Componentes:**
- **Partículas**: Efeitos de explosão e trail
- **Animador de Transição**: Fades e slides suaves

**Uso:**
```python
from src.logic.animacoes import GeradorParticulas, AnimadorTransicao

# Partículas
particulas = GeradorParticulas()
particulas.criar_explosao(x=640, y=360, cor=(255, 100, 100), quantidade=30)
particulas.criar_trail(x=100, y=100, cor=(0, 255, 100))

# No loop
particulas.atualizar()
particulas.desenhar(tela)

# Transições
transicao = AnimadorTransicao(duracao=30)
transicao.iniciar("fade")
if transicao.atualizar():
    print("Transição concluída!")
transicao.desenhar_overlay_fade(tela)
```

---

## Atualizações em Arquivos Existentes

### `src/logic/pontuacao.py`
-  Adicionado sistema de vidas
-  Adicionado desafios diários
-  Novos contadores: acertos_totais, erros_totais, tempo_total_partida
-  Método `registrar_erro()` com redução de vidas
-  Taxa de acerto calculada

### `src/ui/som.py`
-  Controle de música: `musica_ativada`
-  Controle de som de efeitos: `som_efeitos_ativado`
-  Funções: `alternar_musica()`, `alternar_som_efeitos()`

### `src/ui/menus.py`
-  Menu de opções expandido para 3 opções (Resolução, Música, Som)

### `main.py`
-  Importações atualizadas
-  Suporte a 4 botões no menu principal
-  Lógica de controles remapeável

---

## Estrutura de Dados Persistentes

Os seguintes arquivos são salvos em `data/`:

```
data/
├── ranking.json                 # Top 3 recordistas
├── achievements.json            # Conquistas desbloqueadas
├── historico_partidas.json      # Últimas 50 partidas
├── controles.json              # Controles customizados
├── desafio_diario.json         # Status do desafio diário
└── som_config.json             # (Futuro) Configuração de som/música
```

---

