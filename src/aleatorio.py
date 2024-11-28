from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3

import random
Small1 = 'problems/small/calle_del_virrey_morcillo_albacete_250_3.json'

RUTAJSON = Small1

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan

class aleatorio:
    def elegirN(self, nSoluciones, heuristica, problema):
        #candidatos = ["candidato1", "candidato2", "candidato3", "candidato4"]
        candidatos = problema.list_candidatos
        #random 1
        #elegido = random.choice(candidatos)
        soluciones = [0] * len(candidatos)
        mejorSol = 99999999
        mejorPos = 0
        #
        for i in range(nSoluciones): 
            #random 2 parece mas eficiente
            index = random.randrange(len(candidatos))
            elegido = candidatos[index]
            final = elegido
            suma = 0
            for inicial in candidatos:
                suma = (i.pop * AEstrella(problema,heuristica,inicial,final)) + suma

            #devolver el mejor de esas
            if (suma < mejorSol):
                mejorSol = suma
                mejorPos = index
            #
        #Indicamos que es solucion:
        soluciones[mejorPos] = 1 #misma longitud que candidatos
        return soluciones
    #devuelve uno 
problema = Problema(RUTAJSON)
aleatorio(4, h2, problema)

