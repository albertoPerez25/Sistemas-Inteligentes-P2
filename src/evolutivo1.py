from heapq import heappush,heappop
import math
from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3

import random
toy1 = 'problems/toy/calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'
medium1 = 'problems/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'

RUTAJSON = toy1
VMAX = math.inf #Valor Maximo

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan



class evolutivoMALHECHO:
    def __init__(self, nGeneracionesMaximas, tamTorneo, heuristica, problema):
        self.candidatos = problema.candidatos
        self.nSoluciones = problema.number_stations
        self.poblacion = [0] * ((len(self.candidatos))//self.nSoluciones)
        self.fitnessSols = [VMAX] * len(self.candidatos)
        self.fitness = [VMAX] * (len(self.candidatos)//self.nSoluciones)
        self.tamTorneo = tamTorneo
        self.padres = []
        self.nGeneracionesMaximas = nGeneracionesMaximas
        self.heuristica = heuristica

    def inicializarN(self,nSoluciones):
        mejorFitness = VMAX
        mejorIndividuo = 0
        for i in range(len(self.poblacion)): 
            individuo = [0] * nSoluciones   #Un individuo esta compuesto por nSoluciones
            fitnessIndividuo = 0
            for j in range(nSoluciones): 
                #Cogemos uno random:
                index = random.randrange(len(self.candidatos))
                #Calculamos su fitness / funcion evaluacion:
                
                individuo[j] = index
                # Si el individuo es mejor que el mejor de todos, lo guardamos
            fitnessIndividuo = self.calcularFitness(individuo)
            if (fitnessIndividuo < mejorFitness):
                mejorFitness = fitnessIndividuo
                mejorIndividuo = i
            self.poblacion[i] = individuo
            self.fitness[i] = fitnessIndividuo
        return mejorIndividuo
    
    def calcularFitnessSolucion(self,solucionParcial):
        final = self.candidatos[solucionParcial]
        suma = 0
        if (self.fitnessSols[solucionParcial] != VMAX):
            return self.fitnessSols[solucionParcial]
        for inicial in self.candidatos:
            #inicial[1] -> poblacion, inicial[0] -> identificador, final[0] = id final
            aes=AEstrella(problema,inicial[0],final[0],self.heuristica).busqueda()
            suma = (inicial[1] * aes) + suma
        self.fitnessSols[solucionParcial] = suma
        return suma

    def calcularFitness(self,individuo):
        suma = 0
        for i in individuo:
            suma = suma + self.calcularFitnessSolucion(i)
        return suma
    
    def seleccionGeneracion(self):#Seleccion por torneo
        #Cogemos los mejores entre n random:    Podria hacerse con una PriorityQueue, seria mejor?      
        padresGeneracion = [0] * len(self.poblacion)
        for i in range(len(self.poblacion)):
            mejorFitness = VMAX #fitness
            mejorIndividuo = 0 #indice en poblacion
            for _ in range (self.tamTorneo):
                indiceAux = random.randrange(len(self.poblacion))
                if self.fitness[indiceAux] < mejorFitness:
                    mejorFitness = self.fitness[indiceAux] #Como estara almacenado en el diccionario no añadira complejidad
                    mejorIndividuo = indiceAux
            padresGeneracion[i] = mejorIndividuo #Metemos el indice del mejor candidato de cada torneo
        return padresGeneracion

    def cruce(self, padres, indiceCruce):
        hijos = [0] * 2
        #Cruce por un punto. Nos quedamos la mitad de soluciones parciales de cada padre
        if (random.randrange(3) == 1) or (len(str(padres[0]))>indiceCruce and len(str(padres[1]))>indiceCruce):
            hijos[0] = padres[0]
            hijos[1] = padres[1]
        else:   
            hijos[0] = padres[1][:indiceCruce] + padres[0][indiceCruce:]
            hijos[1] = padres[0][:indiceCruce] + padres[1][indiceCruce:]
            if hijos[0] > padres[0]:
                hijos[0] = padres[0]
            if hijos[1] > padres[0]:
                hijos[1] = padres[1]
        return hijos

    def mutacion(self, hijos):
        for i in range(len(hijos)): # Dos hijos, 0 y 1
            nCambios = random.randint(0,self.nSoluciones-1)-self.nSoluciones//2 
            if nCambios > 0:
                for j in range(nCambios):
                    hijos[i][j] =  random.randrange(len(self.candidatos))
        return hijos

    def genetico(self):
        padres = [0] * 2
        hijos = [0] * 2
        mejorIndividuo = self.inicializarN(self.nSoluciones)
        for _ in range(self.nGeneracionesMaximas):
            #Seleccionamos siguiente generacion de padres
            pGeneracion = self.seleccionGeneracion()
            #Cruzamos y mutamos toda la poblacion de dos en dos. (pGeneracion deberia de tener misma lon que poblacion)
            for i in range(0,len(pGeneracion)-1,2):
                #Seleccionamos dos padres
                padres[0] = self.poblacion[pGeneracion[i]]
                padres[1] = self.poblacion[pGeneracion[i+1]]
                #Cruce
                hijos = self.cruce(padres,len(str(len(self.poblacion)-1))//2)
                #Mutacion
                hijos = self.mutacion(hijos)
                #Reemplazo. Mantenemos el mejor individuo de la generacion pasada, a no ser que haya uno mejor
                for j in range(2): # 2 Hijos
                    fitnessHijo = self.calcularFitness(hijos[j])
                    esMejorFitness = fitnessHijo < self.fitness[i]
                    if (self.poblacion[i] != mejorIndividuo) or esMejorFitness:
                        self.poblacion[i] = hijos[j]
                        self.fitness[i] = fitnessHijo
                        if esMejorFitness:
                            mejorIndividuo = hijos[j]
        for ind in mejorIndividuo:
            print(self.candidatos[ind][0])
        return mejorIndividuo
    #devuelve uno 

problema = Problema(RUTAJSON)
print(evolutivoMALHECHO(2, 4, h2, problema).genetico())

