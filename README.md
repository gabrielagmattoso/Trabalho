# Bolo da Lara
Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

## Integrantes do grupo
- Gabriela Gomes Mattoso
- Livia Hilbert de Oliveira
- Isabella Oliveira Araújo Barbosa Moreira
- Giovanna Brito Silva Ribeiro

## Estrutura do projeto
- `main.py`: ponto de entrada da aplicação.
- `testesdeverificacao`: testes do jogo.
- `docs/proposta.md`: proposta inicial do projeto.
- `recordes_bolo_lara.json`: arquivo gerado automaticamente ao salvar um recorde (não é necessário incluir no repositório).

## Descrição do jogo
Bolo da Lara é um jogo de cliques rápidos em que o jogador segue uma receita de bolo passo a passo, guiado pelo personagem Lara. O jogador deve selecionar ingredientes, misturar a massa, assar e decorar o bolo na ordem correta. A pontuação final depende da precisão e da velocidade em cada etapa.

## Objetivo do jogador
Completar as 4 etapas da receita — selecionar ingredientes, misturar, assar e decorar — da forma mais eficiente possível, acumulando o máximo de pontos e conquistando 5 estrelas ao final.

## Regras do jogo
- Seguir a receita na ordem correta.
- O jogo é dividido em 4 etapas: ingredientes, misturar, assar e decorar.
- Não é possível avançar de etapa sem concluir a anterior.
- Clicar em um ingrediente errado desconta 40 pontos.
- Cada etapa tem um timer; esgotar o tempo desconta 50 pontos.
- Elementos ainda não desbloqueados não respondem à interação.
- Erros não encerram o jogo — apenas reduzem a pontuação.
- No final, a pontuação é exibida com estrelas (0 a 5) e uma frase personalizada da Lara.

## Controles
- **Mouse**: único controle do jogo.
  - Arrastar: mover ingredientes e a massa para o forno.
  - Girar o mouse dentro da tigela: misturar a massa.
  - Clicar: selecionar decorações, confirmar ações e navegar pelos menus.

## Como executar o projeto
```bash
git clone https://github.com/gabrielagmattoso/Trabalho.git
cd Trabalho
pip install pygame
python main.py
```

## Como executar os testes
```bash
python testesdeverificacao
```

## Testes implementados
- Clique nos ingredientes: verifica se o desconto de pontos ocorre corretamente ao errar o ingrediente.
- Ordem das etapas: verifica se o jogo impede avançar sem concluir a etapa anterior.
- Bloqueio de elementos: confirma que elementos não desbloqueados não respondem à interação.
- Sistema de pontuação: valida soma de pontos, desconto por erro e cálculo de estrelas.
- Limite de tentativas: verifica a pontuação mínima após esgotar tentativas.
- Troca de cena: valida a transição correta entre as 4 etapas.
- Encerramento: verifica se a tela final exibe corretamente pontuação, estrelas e frase da Lara.
- Pausa: confirma que o pause interrompe o jogo sem perder o estado atual.

