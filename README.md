# NOT NOT Booleano Tupã 

![Python](https://img.shields.io/badge/Python-3.12-blue.svg?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg?style=flat-square)
![USJT](https://img.shields.io/badge/USJT-3º_Semestre-red.svg?style=flat-square)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow.svg?style=flat-square)

## Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Como Jogar](#-como-jogar)
- [Instalação e Execução](#-instalação-e-execução)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Equipe Tupã](#-equipe-tupã)

## Sobre o Projeto
**NOT NOT Booleano Tupã** é um jogo de raciocínio lógico acelerado, desenvolvido como projeto acadêmico pela equipe Tupã (3º Semestre - USJT). Inspirado no clássico *Not Not*, o jogo testa a velocidade de interpretação de **Lógica Booleana** do jogador sob extrema pressão de tempo.

## Funcionalidades (Atuais)

### Modos de Jogo
* **JOGAR:** Modo principal com seleção de dificuldade (Fácil, Normal, Difícil)
* **TIME ATTACK:** Modo de 60 segundos para completar o máximo de desafios
* **TUTORIAL:** Tutorial interativo (In-Game ou Web)

### Sistema de Jogo
* **Motor Lógico Dinâmico:** Geração de desafios booleanos em 5 níveis de dificuldade
* **Sistema de Dificuldade:** 3 níveis (Fácil, Normal, Difícil) com configurações distintas
* **Sistema de Vidas:** Começa com 3 vidas, perde 1 por erro
* **Sistema de Combo e Multiplicador:** Recompensa acertos consecutivos
* **Sistema de Níveis e XP:** Progressão de jogador com XP ganho ao acertar, níveis progressivos e barra de XP visual
* **Sistema de Combo Visual:** Efeitos visuais de partículas coloridas a cada 5 de combo
* **Powerups:** 5 tipos diferentes (Tempo Extra, Congelar Multiplicador, Remover Opção, Escudo, Multiplicador x2)
  * **Remover Opção:** Remove visualmente uma opção errada do desafio atual
  * **Powerups não acumulam:** São limpos automaticamente ao terminar uma partida
* **Sistema de Pausa:** Pausa o jogo com ESC

### Progressão e Conquistas
* **Sistema de Achievements:** Conquistas desbloqueáveis (Combo 500, Combo 1000, Perfeccionista, etc.)
* **Desafios Diários Infinitos:** 15 desafios que rotacionam diariamente
* **Histórico de Partidas:** Rastreia as últimas 50 partidas
* **Ranking por Dificuldade:** Top 3 recordistas separados por nível (Fácil, Normal, Difícil) para pontuação justa

### Interface e Usabilidade
* **Intro Animada:** Fade-in, texto aparecendo letra por letra, partículas, música própria
* **Menu Principal com Botões Visuais:** Botões com imagens (Play, Config, Quit) no lado esquerdo da tela
* **Mão Seletora:** Indicador visual da opção selecionada no menu principal
* **Layout Responsivo:** Botões escalonados proporcionalmente ao tamanho da tela
* **Popups de Conquistas:** Notificações estilo Xbox ao desbloquear conquistas
* **Popups de Powerups:** Notificações ao obter powerups
* **Teclado Customizável:** Sistema de remapeamento de teclas
* **Janelinha de Desafios:** Mostra desafios diários no menu principal
* **HUD Melhorado:** Painel com fundo para melhor visibilidade de pontos, combo, tempo, nível e powerups
* **Tela de Conquistas:** Paginação (8 por página), navegação A/D, textos centralizados
* **Tela de Desafios Diários:** Paginação (5 por página), navegação A/D, textos centralizados
* **Nível no HUD:** Exibido em dourado com barra de XP visual no HUD principal

### Configurações
* **Resolução:** 4 opções (800x600, 1280x720, 1920x1080, Fullscreen)
* **Controle de Música:** Ativar/desativar música de fundo
* **Controle de Som:** Ativar/desativar efeitos sonoros
* **Controles Customizados:** Remapear teclas
* **Tela de Histórico:** Ver estatísticas das últimas partidas
* **Tela de Conquistas:** Ver todas as conquistas desbloqueadas
* **Tela de Desafios:** Ver desafios diários completos

### Persistência de Dados
* Salvamento automático via JSON
* Arquivos: ranking.json, achievements.json, historico_partidas.json, controles.json, desafio_diario.json

## Como Jogar
O cubo (ou texto central) exibirá uma instrução lógica (Ex: `! (UP OR DOWN)`). Você tem frações de segundo para processar a informação e pressionar a seta correspondente à direção **verdadeira** antes que o tempo esgote.
* **Setas do Teclado (`⬆️ ⬇️ ⬅️ ➡️`):** Movem o personagem/respondem ao desafio.
* **ENTER:** Inicia a partida.
* **R:** Reinicia após o Game Over.
* **ESC:** Retorna ao menu principal.

## Instalação e Execução

### Pré-requisitos
* Python 3.12 ou superior.
* Gerenciador de pacotes `pip`.

### Passo a passo
1. Clone o repositório:
   ```bash
   git clone [https://github.com/3-semestre-USJT/NOT-NOT-booleano-Tup-.git](https://github.com/3-semestre-USJT/NOT-NOT-booleano-Tup-.git)

 2. Crie e ative um ambiente virtual (Recomendado):
    python -m venv .venv
    source .venv/bin/activate  # No Windows use: .venv\Scripts\activate

3. Instale as dependências:
    pip install -r requirements.txt

4. Inicie o jogo: 
    python main.py

## Equipe Tupã
Projeto desenvolvido por 7 estudantes de Ciência da Computação / Análise e Desenvolvimento de Sistemas da Universidade São Judas Tadeu.