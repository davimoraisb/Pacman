# Implementação do Agente Minimax no Pac-Man

Este projeto contém a implementação do algoritmo Minimax para o jogo Pac-Man, permitindo que o agente tome decisões inteligentes antecipando os movimentos dos fantasmas (que agem de forma a minimizar a pontuação do Pac-Man).

## Alterações Realizadas

O arquivo `seuPacManAgents.py` passou por diversas refatorações para otimizar o comportamento do Pac-Man:

### 1. Estrutura do Algoritmo Minimax
- O algoritmo foi devidamente estruturado em turnos. No turno `agentIndex == 0`, o Pac-Man busca **maximizar** sua pontuação. Nos turnos subsequentes (fantasmas), o algoritmo busca **minimizar** a pontuação.
- A profundidade (`depth`) da árvore de busca só é incrementada após todos os agentes completarem suas jogadas (quando o turno volta para o Pac-Man).
- Caso o jogo atinja o estado de vitória/derrota, ou atinja a profundidade máxima, a função de avaliação é chamada.

### 2. Tratamento da Ação "Ficar Parado" (Stop)
- **O Desafio:** Em muitos cenários de Minimax, quando o Pac-Man percebia que não tinha nenhuma rota vantajosa imediata (ou quando as pontuações avaliadas de se mover empatavam), ele optava por ficar parado (`Stop`). Isso causava hesitação e muitas vezes resultava nele sendo pego facilmente, em vez de tentar escapar.
- **A Solução:** Removemos a ação `'Stop'` da lista de ações legais sempre que o Pac-Man tem outras opções (`if agentIndex == 0 and 'Stop' in actions and len(actions) > 1: actions.remove('Stop')`). Isso força o Pac-Man a se manter em movimento e tentar explorar rotas de fuga.

### 3. Loop Infinito e Falta de Busca por Comida
- **O Desafio:** Outro problema comum na avaliação do estado original era que o Pac-Man muitas vezes entrava em "loop" (indo para frente e para trás constantemente) e ignorava as comidas, especialmente quando elas estavam distantes. Ele acabava focando apenas em manter distância dos fantasmas.
- **A Solução:** A `betterEvaluationFunction` foi completamente reformulada:
  - Foi adicionada uma **forte penalidade por comidas restantes** no mapa (`-20.0 * len(foodList)`), forçando-o a sempre querer limpar o labirinto.
  - Funções auxiliares (`avaliarSegurancaEComida` e `avaliarFantasmas`) foram criadas para gerar uma atração progressiva para a comida mais próxima, balanceando com o risco dos fantasmas se aproximarem (mantendo uma distância segura).
  - Além de fugir, ele também é fortemente atraído para caçar fantasmas quando eles estão assustados.

## Como Executar

Abra o terminal dentro da pasta `pacman/` e utilize os comandos abaixo.

**Para rodar o MinimaxAgent com configurações padrão:**
```bash
python pacman.py -p MinimaxAgent
```

**Para rodar ajustando a profundidade da busca (ex: depth=2):**
```bash
python pacman.py -p MinimaxAgent -a depth=2
```

> **Dica:** Profundidades maiores farão o Pac-Man prever jogadas mais adiante, mas deixarão o cálculo mais lento. Profundidades curtas como `2` ou `3` costumam oferecer um bom equilíbrio entre inteligência e velocidade de execução.
