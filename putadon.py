for j in candidates:
    suma = 0
    #FUNCION PARA ELEGIR INICIAL
    inicial = getInicial()
    for i in candidatas:
        #FUNCION PARA ELEGIR EL FINAL
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



getInicial():
    #mejor de N(x) (el mejor de los vecinos)

#ValueS = PriorityQueue2.get()*PriorityQueue.get()
#aleatorio poner tantos 1 como estaciones elegidas como solucion.
#una lista separada para estos 1 o 0s en la que cada posicion de la lista sea la misma posicion de la
#lista de candidatos

#Modificar en la func evaluacion el inicio y final, ir asignandolos
#diccionario de listas en segmentos en vez de diccionario de pq con sortfrontera

#tiempo en ir de A a B hay que guardarlo en algun lado por si volvemos a calcularlo evitar calcularlo.

#AÑADIR RESULTADO DE NODO INICIO A NODO FINAL EN LA LISTA DE RESULTADOS
#CAMBIAR NODOS INICIAL Y FINAL POR EL METODO ELEGIDO (ALEATORIO) VAMOS LLAMAR A UNA FUNCION