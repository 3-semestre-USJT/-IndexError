# Guia de Contribuição - Equipe Tupã

Bem-vindo ao guia de desenvolvimento do nosso projeto! Para mantermos o código organizado, livre de bugs e rastreável, **todos os membros devem seguir as regras abaixo.**

## 1. Regras de Branching (Ramificação)
NUNCA comite diretamente na branch `main`. A `main` deve conter apenas código que funciona 100%.
Para cada nova tarefa do Jira, crie uma branch a partir da `main` seguindo o padrão:
`feature/CHAVE-DO-JIRA-NOME-DA-TAREFA` ou `bugfix/CHAVE-DO-JIRA-NOME-DO-BUG`

**Exemplo:**
```bash
git checkout main
git pull origin main
git checkout -b feature/SCRUM-12-MUSICA-MENU
```

## 2. Padrão de Commits (Smart Commits)
O Jira está integrado ao nosso GitHub. Para que ele rastreie o nosso trabalho, TODO commit deve começar com a chave da tarefa, seguido do padrão Conventional Commits (feat, fix, docs, refactor).

Exemplos corretos:

git commit -m "SCRUM-10: feat: adiciona sistema de pontuacao e combo"

git commit -m "SCRUM-5: docs: atualiza o README com novas instrucoes"

git commit -m "SCRUM-15: fix: corrige o bug das letras sobrepostas na tela"

## 3. Regra de Ouro (Testes e Merge)
Codifique sua funcionalidade.

Faça os testes rodarem localmente antes de enviar.

Envie sua branch para o GitHub (git push -u origin nome-da-branch).

Abra um Pull Request (PR) apontando para a main.

Solicite que pelo menos 1 membro da equipe revise seu código.

Apenas faça o Merge na main após a revisão e aprovação.

## 4. Limite de Trabalho (WIP - Work In Progress)
Para não travar o projeto, temos um limite estrito no Jira:
* Ninguém pode ter mais de 2 cards em andamento (coluna "In Progress") ao mesmo tempo. 
* Termine o seu código atual antes de puxar uma nova tarefa.

## 5. O Fluxo de Revisão (QA)
O seu código não vai direto para o jogo principal.
* Quando terminar a programação, mova o card para a coluna "Em Revisão / QA" no Jira.
* Ele indica que o trabalho foi feito, mas o Luiz ou o Dias (PM) precisam testar no Pygame.
* Somente após a aprovação deles o código vai para "Done" e é integrado ao jogo oficial.

## 6. Proibição de Commits "Vazios"
O histórico do nosso repositório servirá para auditoria[cite: 107].
* É estritamente proibido criar mensagens de commit vazias ou sem sentido.
* **NUNCA FAÇA ISSO:** `git commit -m "arrumando coisas"` ou `git commit -m "update"`.
* Use sempre a Chave do Jira e seja claro sobre o que alterou.

## 7. Protocolo de Conflitos (Merge Conflict)
Com 7 pessoas programando juntas, conflitos vão acontecer.
* Se o GitHub acusar um "Merge Conflict" (duas pessoas alteraram a mesma linha), **não tente forçar a resolução sozinho** se não tiver segurança.
* Pare o que está fazendo e notifique a gerência do projeto para resolver o conflito juntos, sem perder a lógica de ninguém.

## 8. Arquitetura e .gitignore
* **A Regra do Lixo:** Nossos computadores geram pastas ocultas (`__pycache__` ou `.venv`) que são pesadas e causam conflitos.
* O arquivo `.gitignore` bloqueia isso. [cite_start]Jamais apague ou ignore este arquivo.
* **Respeite as Pastas:** Siga a estrutura definida.
* Códigos visuais e do Pygame vão dentro de `src/ui/`.
* A "Engine" matemática vai em `src/logic/`.
* Músicas e imagens vão em `assets/`.
