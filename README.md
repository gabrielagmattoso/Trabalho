# Bolo da Lara

Jogo de cliques interativo desenvolvido com Python e Pygame, inspirado no Sara's Red Velvet Cake (Friv Jogos).

---

## Equipe

- Gabriela Gomes Mattoso
- Livia Hilbert de Oliveira
- Isabella Oliveira Araújo Barbosa Moreira
- Giovanna Brito Silva Ribeiro

---

## Sobre o Jogo

Bolo da Lara é um jogo de cliques rápidos em que o jogador segue uma receita de bolo passo a passo. A receita aparece na tela e o jogador deve clicar nos ingredientes certos, na ordem certa, para preparar o bolo corretamente.

O jogo é dividido em 4 etapas: selecionar ingredientes, misturar, assar e decorar.

---

## Objetivo

Interagir com o ambiente — ingredientes, utensílios e eletrodomésticos — no momento correto, seguindo os passos da receita, buscando atingir a pontuação máxima através da eficiência.

---

## Regras

- Seguir a receita na ordem correta
- Controle exclusivamente pelo mouse
- Não é possível avançar de etapa sem concluir a anterior
- Elementos bloqueados não respondem a cliques
- Elementos decorativos do ambiente não são interativos
- Clicar no ingrediente errado desconta pontos
- Cada etapa possui um número limitado de tentativas; após atingir o limite de erros, o jogador recebe a pontuação mínima da fase
- Erros não encerram o jogo

---

## Sistema de Pontuação

A cada etapa, uma quantidade de pontos equivalente à eficiência do jogador é somada ao total. A tela final exibe a pontuação em estrelas, proporcional à porcentagem de acertos, com frases personalizadas da Lara: "Você foi incrível!", "Quase lá!" ou "Da próxima consegue!". Combos de acertos consecutivos concedem bônus.

---

## Elementos do Jogo

**Visuais:** interface gráfica por etapa, fundo que muda conforme a etapa atual, sombras para distinguir itens clicáveis dos decorativos e card visual da receita com destaque no passo atual.

**Interativos:** barra de progresso, área de mistura dos ingredientes e timer visual do forno.

**Sonoros:** trilha de fundo por etapa, feedback sonoro de acerto/erro e efeitos de cozinha como som da batedeira.

**Narrativa:** personagem Lara guia o jogador durante toda a experiência, com tela de introdução e falas com instruções e reações à pontuação.

**Acessibilidade:** botão de pause sem perder o estado atual, tela de "Como Jogar" e dicas visuais.

**Técnicos:** gerenciador de cena, gerenciador de áudio, sistema de carregamento de assets e controle de FPS.

---

## Estrutura de Dados

Lista, dicionário, tupla e classe.

---

## Assets

- Imagens: `.png`
- Áudio: `.mp3` / `.wav`
- Dados / Receita: `.json`
- Fontes: `.ttf`

---

## Estrutura do Projeto

```
Trabalho/
├── main.py
├── testes/
│   └── test_jogo.py
├── docs/
│   └── proposta.md
└── README.md
```

---

## Como Executar

```bash
git clone https://github.com/gabrielagmattoso/Trabalho.git
cd Trabalho
pip install pygame
python main.py
```

Requisitos: Python 3.10+ e Pygame 2.x

---

## Como Executar os Testes

```bash
python testesdeverificacao
```

---

## Testes Planejados

- Clique nos ingredientes: verificar se o clique do mouse está sendo detectado corretamente na área do ingrediente certo e do errado, confirmando o desconto de pontos no caso de erro.
- Ordem das etapas: verificar se o jogo impede o jogador de avançar sem ter concluído a anterior.
- Bloqueio de elementos: confirmar que elementos não desbloqueados não respondem à interação do jogador.
- Sistema de pontuação: validar se os pontos são somados corretamente a cada acerto e descontados a cada erro, e se as estrelas finais refletem a porcentagem correta.
- Limite de tentativas: verificar se, após atingir o número máximo de erros em uma etapa, o jogador recebe a pontuação mínima daquela fase.
- Troca de cena: validar se o gerenciador de cena transita corretamente entre as 4 etapas e se o fundo muda conforme esperado.
- Encerramento: verificar se, ao concluir a última etapa, a tela final exibe corretamente a pontuação, as estrelas e a frase da Lara.
- Pausa: confirmar se o botão de pause interrompe o jogo sem perder o estado atual.

---

## Escopo Mínimo — Entrega Final

- Tela inicial com botão de início e tela de "Como Jogar"
- Pelo menos 2 das 4 etapas funcionais (selecionar ingredientes e misturar)
- Sistema de clique com validação de certo/errado
- Sistema de pontuação com desconto por erro e exibição de estrelas
- Bloqueio de elementos não desbloqueados
- Tela final com pontuação, estrelas e frase da Lara
- Carregamento de assets via `.png` e `.mp3` / `.wav`
- Controle exclusivo pelo mouse em todas as interações

---

## Principais Dificuldades Esperadas

- Design e organização da interface gráfica
- Inexperiência com desenvolvimento de jogos em Pygame
- Implementação de gerenciadores de cena e áudio
- Coordenação da lógica de estados entre etapas

---

Projeto desenvolvido como trabalho acadêmico — Python com Pygame.
