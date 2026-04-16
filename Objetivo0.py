        rota =[(mx,meu)]
        x,y =(mx,meu)
        enquanto visitados[(x,y)]é não Nenhum:
           x,y = visitados[(x,y)]
           se visitados[(x,y)]é não Nenhum:
               rota.acrescentar((x,y))
        retornar rota[::-1]#Inverta uma lista
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
    #Retorna verdadeira se o ponto (x,y) é uma posição livre no mapa.
    #Para ser considerado livre a posição deve estar dentro dos limites
    #do mapa e não deve conter nenhum objeto indicado na lista "ocupados"
    #Por padrão, ocupados são apenas blocos de madeira, minerais e indestrutíveis
    definição posicao_livre(auto,x,y,estado_do_jogo,Últimos =['sb','ob','ib','b']):
        b = estado_do_jogo.está_dentro_dos_limites((x,y))
        e = estado_do_jogo.entidade_em((x,y))
        retornar(b e e não em Últimos)
    #Retorna uma lista com as posições livres adjacentes a (ex,ey)     
    definição livro nca(auto,ex,ei,estado_do_jogo,Últimos =['sb','ob','ib','b']):
        vizinhas =[]
        #Coordenadas de cima, baixo, esquerda, direita
        posicos =[(ex,ei-1), (ex,ei+1), (ex-1,ei), (ex+1,ei)]
        para px,py em posicos:
            se auto.posicao_livre(px,py,estado_do_jogo,Últimos):
               vizinhas.acrescentar((px,py))
        retornar vizinhas
   
    #Calcula uma rota da origem (ox,oy) até uma meta (mx,my).
    #A rota é uma lista de coordenadas ou uma lista vazia caso não exista uma rota
    definição busca_largura(auto,boi,oy,mx,meu,estado_do_jogo,estado_do_jogador):
        visitados ={}
        visitados[(boi,oy)]= Nenhum 
        fila = deque([(boi,oy)])#criando a fila com a pos inicial
        
        enquanto fila:#enquanto tiver elementos na fila
           ex,ei = fila.popleft()#retiramos elemento da esq. da fila
           se ex == mx e ei == meu:#verifica se servir a meta
              retornar auto.reconstroi(mx,meu,visitados)
           para x,y em auto.livro nca(ex,ei,estado_do_jogo):
              se(x,y)não em visitados:
                  visitados[(x,y)]=(ex,ei)
                  fila.acrescentar((x,y))
        retornar[]#Retorna uma rota vazia caso não encontre a meta
    
    #Função principal do jogo: deve retornar uma das ações abaixo:
    # 'u' = Andar para cima     
    # 'r' = Andar para direita  
    # 'd' = Andar para baixo    
    # 'l' = Andar para esquerda
    # 'p' = Jogar bomba         
    # '' = Ficar parado           
    definição próximo_movimento(auto,estado_do_jogo,estado_do_jogador):
        # SENSORES =======================================================
        machado,sim = estado_do_jogador.localização
        hx,hy = estado_do_jogo.oponentes(estado_do_jogador.eu ia)[0]
        distância_humano = auto.distância((machado,sim), (hx,hy))
        distancia_bomba,bx,por = auto.bomba_proxima(machado,sim,estado_do_jogo)
        distância_tesouro,tx,obrigado = auto.bem-vindo(machado,sim,estado_do_jogo)
        imprimir("Estado:",auto.estado)
        imprimir("Tesouro",tx,obrigado,distância_tesouro)
        imprimir("Bomba",bx,por,distancia_bomba)
        # TRANSIÇÃO DE ESTADOS =============================================
        
        se distancia_bomba <= 3:
            auto.estado = "fugir"
        elif distância_tesouro <= 5:
            auto.estado = "coletar_tesouro"
        elif distância_humano <= 1:
            auto.estado = "atacar"    
        outro:
            auto.estado = "explorar"    
        # EXECUÇÃO DE AÇÕES ==============================================
        se auto.estado == "fugir":
            retornar auto.motor(estado_do_jogo, (machado,sim), (bx,por),aproximar = Falso)
        se auto.estado == "coletar_tesouro":
            #Rotação Calcular
            rota = auto.busca_largura(machado,sim,tx,obrigado,estado_do_jogo,estado_do_jogador)
            imprimir(rota)
            se rota:
                retornar auto.motor(estado_do_jogo, (machado,sim),rota[0])
        se auto.estado == "atacar":
           retornar 'p'
        se auto.estado == "explorar":
           retornar aleatório.escolha(['você','d','l','r'])
        se distância_tesouro <=5:
            auto.estado = "coletar_tesouro"
       
        retornar '' #Caso nenhuma ação seja possível fique parado por padrão.
