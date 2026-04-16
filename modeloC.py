importar aleatório
aula Agente:
    definição __inicial__(auto):
        auto.contador = 0 #inicializa
        auto.rota =[]#rota usada para fuga
        auto.alvo =(-1,-1)#posicao do alvo
    #Função booleana auxiliar para verificar se uma posição p está bloqueada.
    #Retorna True se p está fora do mapa ou se estiver ocupado por parede/bomba/agente
    definição tem_bloqueio(auto,estado_do_jogo,p):
        retornar não estado_do_jogo.está_dentro_dos_limites(p)ou estado_do_jogo.entidade_em(p)em['sb','ib','ob','b',0,1]
    #Função que calcula a distância de Manhattan entre p1 e p2
    #Recebe p1 como uma tupla (x,y)
    #Recebe p2 como uma tupla (x,y)
    #Retorna um número
    definição distância(auto,p1,p2):
        retornar abdômen(p1[0]- p2[0])+ abdômen(p1[1]- p2[1])
    #Retorna a ação que um agente não precisa realizar para se aproximar/afastar do ponto b
    #Recebe estado_do_jogo
    #Recebe a: ponto (x,y) considerado como o agente que irá se mover
    #Recebe b: ponto (x,y) que é o ponto de referência
    #Recebe aproximar: se Verdadeiro o objetivo é se aproximar, caso contrário vai tentar afastar.
    #Retorna uma ação que mais aproxima ou afasta a de b.
    definição motor(auto,estado_do_jogo,um,b,aproximar=Verdadeiro):
        dist_ab = auto.distância(um,b)
        ações =[]
        cascas ={'você': (um[0],um[1]+1),'r': (um[0]+1,um[1]),'d': (um[0],um[1]-1),'l':(um[0]-1,um[1])}
        para Ação,p em cascas.Unid():
           se não auto.tem_bloqueio(estado_do_jogo,p):
               dist_pb = auto.distância(p,b)
               se(dist_pb > dist_ab e não aproximar)ou(dist_pb < dist_ab e aproximar):
                   ações.acrescentar(Ação)
        #Se tem alguma ação escolhe uma aleatoriamente
        se len(ações)> 0:
            retornar aleatório.escolha(ações)
        #Ser retorna vazio
        retornar ''
        
    definição próximo_movimento(auto,estado_do_jogo,estado_do_jogador):
        #Pega Coordenação do Agente e Comunicação
        machado,sim = estado_do_jogador.localização
        comunicação = estado_do_jogador.munição
        
        se auto.contador == 0 e comunicação > 0:
            #Crie uma lista com posições possíveis onde pode haver uma bomba
            posicos =[(machado,sim),(machado,sim+1), (machado+1,sim), (machado,sim-1), (machado-1,sim)]
           
            #Verifica se uma das posições da lista é bloco de minério (ob)
            para p em posicos:
                se estado_do_jogo.entidade_em(p)== 'ob':
                    auto.contador = 40 #atualiza
                    retornar 'p' #joga bomba
        #Se o contador memorizado estiver positivo até a metade
        se auto.contador > 20:
            imprimir("Afastando",auto.contador)
            auto.contador = auto.contador - 1 #atualiza
            Ação = auto.motor(estado_do_jogo, (machado,sim),auto.alvo,aproximar=Falso)
            auto.rota.acrescentar((machado,sim))#atualiza memória da rota de volta
            retornar Ação
        #Se o contador memorizado estiver positivo
        se auto.contador > 0:
            imprimir("Voltando",auto.contador)
            auto.contador = auto.contador - 1 #atualiza
            p = auto.rota.pop()#retira da lista última posição da rota
            Ação = auto.motor(estado_do_jogo, (machado,sim),p,aproximar=Verdadeiro)
            retornar Ação
        retornar aleatório.escolha(['você','d','l','r'])#Aleatório por padrão
