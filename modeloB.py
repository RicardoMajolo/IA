# #Agora crie outro agente modeloB.py baseado em memória com o comportamento abaixo:
# se o agente estiver em cima de uma bomba ou adjacente a ela, deve iniciar uma fuga da posição da bomba.
# a fuga deve durar 10 iterações.
# se não estiver fugindo então deve andar aleatoriamente.

import random

class Agent:

    def __init__(self):
        self.contador = 0 
        self.posicao = (-1,-1) 

    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    def next_move(self, game_state, player_state):
        ax, ay = player_state.location 
        
        # 1. identifica bomba adjacente
        # Verificamos se há uma bomba por perto para começar a fuga
        bomba_proxima = None
        for p in [(ax, ay), (ax, ay+1), (ax, ay-1), (ax+1, ay), (ax-1, ay)]:
            if game_state.entity_at(p) == 'b':
                bomba_proxima = p
                break

        if bomba_proxima:
            self.contador = 10
            self.posicao = bomba_proxima

        if self.contador > 0:
            self.contador -= 1
            px, py = self.posicao
            dp = abs(ax - px) + abs(ay - py) # Distância atual da bomba

            actions = []
            # Tenta se mover para direções que aumentem a distância 'dp'
            for vizinho, letra in [((ax, ay+1), 'u'), ((ax, ay-1), 'd'), ((ax+1, ay), 'r'), ((ax-1, ay), 'l')]:
                if not self.tem_bloqueio(game_state, vizinho):
                    d_nova = abs(vizinho[0] - px) + abs(vizinho[1] - py)
                    if d_nova > dp:
                        actions.append(letra)
            
            if actions:
                return random.choice(actions)

        # movimento aleatorio
        possiveis = []
        for vizinho, letra in [((ax, ay+1), 'u'), ((ax, ay-1), 'd'), ((ax+1, ay), 'r'), ((ax-1, ay), 'l')]:
            if not self.tem_bloqueio(game_state, vizinho):
                possiveis.append(letra)
        
        return random.choice(possiveis) if possiveis else ''