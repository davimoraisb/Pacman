# multiAgents.py ou seuPacManAgents.py
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
        Algoritmo Minimax para controle do agente Pac-Man.
        """
        def minimax(agentIndex=0, depth=0, state=gameState):
            # 5.2. Condição de Parada (Base Case)
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            actions = state.getLegalActions(agentIndex)

            # Opcional: Evita hesitação removendo 'Stop' se houver outras escolhas
            if agentIndex == 0 and 'Stop' in actions and len(actions) > 1:
                actions.remove('Stop')

            # Caso não existam ações legais disponíveis
            if not actions:
                if depth == 0:
                    return Directions.STOP
                return self.evaluationFunction(state)

            # 5.3. Gerenciamento de Agentes e Profundidade
            numAgents = state.getNumAgents()
            isLastGhost = (agentIndex == numAgents - 1)

            if isLastGhost:
                nextAgent = 0
                nextDepth = depth + 1
            else:
                nextAgent = agentIndex + 1
                nextDepth = depth

            # 5.4. Lógica de Maximização (Turno do Pac-Man)
            if agentIndex == 0:
                max_score = -float('inf')
                best_action = actions[0]  # Garante uma ação padrão caso todas levem a -inf

                for action in actions:
                    next_state = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, nextDepth, next_state)

                    if score > max_score:
                        max_score = score
                        best_action = action

                if depth == 0:
                    return best_action
                return max_score

            # 5.5. Lógica de Minimização (Turno dos Fantasmas)
            else:
                min_score = float('inf')

                for action in actions:
                    next_state = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, nextDepth, next_state)

                    if score < min_score:
                        min_score = score

                return min_score

        return minimax()


def avaliarSegurancaEComida(pos, foodList, ghostStates):
    if not foodList:
        return 0

    foodDistances = [manhattanDistance(pos, f) for f in foodList]
    minFoodDist = min(foodDistances)

    activeGhosts = [g for g in ghostStates if g.scaredTimer == 0]

    if activeGhosts:
        ghostDistances = [manhattanDistance(pos, g.getPosition()) for g in activeGhosts]
        minGhostDist = min(ghostDistances)
    else:
        minGhostDist = float('inf')

    if minFoodDist < minGhostDist - 1 or minGhostDist > 3:
        return 30.0 / (minFoodDist + 1)

    return 10.0 / (minFoodDist + 1)


def avaliarFantasmas(pos, ghostStates):
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

    score -= 20.0 * len(foodList)
    score += avaliarSegurancaEComida(pos, foodList, ghostStates)
    score += avaliarFantasmas(pos, ghostStates)

    return score

better = betterEvaluationFunction