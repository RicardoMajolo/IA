import random

class Agent:

    def __init__(self):
        self.contador_fuga = 0   
        self.posicao_alvo = None 
        self.bombas_colocadas = 0 

    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    def next_move(self, game_state, player_state):
        ax, ay = player_state.location
        tem_municao = player_state.ammo > 0

        # Se não temos um alvo e não estamos no meio de um plano, procuramos 'ob' adjacente
        if self.posicao_alvo is None:
            for p in [(ax, ay+1), (ax, ay-1), (ax+1, ay), (ax-1, ay)]:
                if game_state.entity_at(p) == 'ob' and tem_municao:
                    self.posicao_alvo = p
                    self.bombas_colocadas = 0
                    break

        #se tiver um alvo
        if self.posicao_alvo is not None:
            px, py = self.posicao_alvo
            dist = abs(ax - px) + abs(ay - py)

            # Se acabou de colocar a bomba (ou precisa fugir)
            if self.contador_fuga > 0:
                self.contador_fuga -= 1
                # Lógica de fuga (igual ao exercício anterior)
                actions = []
                for v, letra in [((ax,ay+1),'u'), ((ax,ay-1),'d'), ((ax+1,ay),'r'), ((ax-1,ay),'l')]:
                    if not self.tem_bloqueio(game_state, v):
                        if (abs(v[0]-px) + abs(v[1]-py)) > dist:
                            actions.append(letra)
                return random.choice(actions) if actions else ''

            # B) Se já fugiu e precisa voltar ao bloco
            if dist > 1:
                # Lógica para se aproximar do bloco (posicao_alvo)
                actions = []
                for v, letra in [((ax,ay+1),'u'), ((ax,ay-1),'d'), ((ax+1,ay),'r'), ((ax-1,ay),'l')]:
                    if not self.tem_bloqueio(game_state, v):
                        if (abs(v[0]-px) + abs(v[1]-py)) < dist:
                            actions.append(letra)
                return random.choice(actions) if actions else ''

            # Se chegou ao lado do bloco e tem munição, solta a bomba
            if dist == 1 and tem_municao and self.bombas_colocadas < 3:
                self.bombas_colocadas += 1
                self.contador_fuga = 5 # Foge por 5 turnos após dropar
                
                # Se completou 3 bombas, reseta o alvo para procurar outro depois
                if self.bombas_colocadas == 3:
                    proximo_alvo = None # Variável auxiliar para resetar no fim do turno
                
                return 'b'

            # Se as 3 bombas acabaram ou a munição acabou, esquece esse bloco
            if self.bombas_colocadas >= 3 or not tem_municao:
                self.posicao_alvo = None

            #se move aleatorio
        possiveis = []
        for v, letra in [((ax,ay+1),'u'), ((ax,ay-1),'d'), ((ax+1,ay),'r'), ((ax-1,ay),'l')]:
            if not self.tem_bloqueio(game_state, v):
                possiveis.append(letra)
        
        return random.choice(possiveis) if possiveis else ''