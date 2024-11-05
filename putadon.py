for j in candidates:
    suma = 0
    for i in candidatas:
        aux = i.pop * aestrella(Problema(RUTAJSON),heuristica,inicio,final)
        #Inicio es i.id o C[i].id
        #Final es j o S[j]
        suma = suma + aux

        #PriorityQueue2.put(1/i.pop)
        #suma2 = suma2 + j.pop
        #para la otra parte de la formula
    PriorityQueue.put((suma,j)) # Metemos tupla organizada por minimo por la suma. 
    suma2 = suma2 + j.pop

ValueS = 1/suma2 * PriorityQueue.get()

#ValueS = PriorityQueue2.get()*PriorityQueue.get()