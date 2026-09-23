# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
from multiAgents import MultiAgentSearchAgent


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        """
        Algoritmo Minimax para controle do Pac-Man.
        """
        def minimax(agentIndex=0, depth=0, state=gameState):
            # Caso base: vitória, derrota ou profundidade máxima atingida
            if state.isWin() or state.isLose() or depth == self.depth:
                return betterEvaluationFunction(state)

            actions = state.getLegalActions(agentIndex)

            # Remove a ação de ficar parado no turno do Pac-Man (evita hesitação)
            if agentIndex == 0 and 'Stop' in actions and len(actions) > 1:
                actions.remove('Stop')

            # Se não houver ações disponíveis para o agente
            if not actions:
                if depth == 0:
                    return Directions.STOP
                return betterEvaluationFunction(state)

            # Calcula o próximo agente
            nextAgent = agentIndex + 1
            if nextAgent == state.getNumAgents():
                nextAgent = 0

            # Incrementa a profundidade apenas quando o turno volta ao Pac-Man (agente 0)
            nextDepth = depth
            if nextAgent == 0:
                nextDepth += 1

            if agentIndex == 0:
                # Maximização (Turno do Pac-Man)
                max_score = -float('inf')
                # Define a primeira ação como padrão para evitar que best_action fique como None
                best_action = actions[0]

                for action in actions:
                    next_state = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, nextDepth, next_state)

                    if score > max_score:
                        max_score = score
                        best_action = action

                if depth == 0:
                    return best_action
                return max_score

            else:
                # Minimização (Turno dos Fantasmas)
                min_score = float('inf')

                for action in actions:
                    next_state = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, nextDepth, next_state)

                    if score < min_score:
                        min_score = score

                return min_score

        return minimax()


def avaliarSegurancaEComida(pos, foodList, ghostStates):
    """
    1. Se a comida estiver mais próxima que os fantasmas (de forma segura), atrai o Pac-Man.
    2. Se a comida estiver longe, gera atração progressiva para ele se aproximar.
    """
    if not foodList:
        return 0

    foodDistances = [manhattanDistance(pos, f) for f in foodList]
    minFoodDist = min(foodDistances)

    # Considera apenas fantasmas ativos (não assustados)
    activeGhosts = [g for g in ghostStates if g.scaredTimer == 0]

    if activeGhosts:
        ghostDistances = [manhattanDistance(pos, g.getPosition()) for g in activeGhosts]
        minGhostDist = min(ghostDistances)
    else:
        minGhostDist = float('inf')

    # Regra 1: Comida mais próxima que o fantasma com margem de segurança
    if minFoodDist < minGhostDist - 1 or minGhostDist > 3:
        return 30.0 / (minFoodDist + 1)

    # Regra 2: Comida distante / aproximação contínua
    return 10.0 / (minFoodDist + 1)


def avaliarFantasmas(pos, ghostStates):
    """
    Penaliza fortemente aproximações a fantasmas perigosos.
    Incentiva a caça caso o fantasma esteja assustado.
    """
    score = 0
    for ghost in ghostStates:
        dist = manhattanDistance(pos, ghost.getPosition())

        if ghost.scaredTimer > 0:
            if dist > 0:
                score += 100.0 / dist
        else:
            if dist <= 1:
                score -= 1000.0
            elif dist <= 2:
                score -= 300.0
    return score


def betterEvaluationFunction(currentGameState: GameState):
    if currentGameState.isWin():
        return float('inf')
    if currentGameState.isLose():
        return -float('inf')

    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    score = currentGameState.getScore()

    # Penaliza a quantidade de comida restante no mapa
    score -= 20.0 * len(foodList)

    # Soma os cálculos de segurança/comida e fantasmas
    score += avaliarSegurancaEComida(pos, foodList, ghostStates)
    score += avaliarFantasmas(pos, ghostStates)

    return score

# Abreviação
better = betterEvaluationFunction