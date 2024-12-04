from heapq import heappush,heappop
import math
import time
from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3
from functools import lru_cache
import matplotlib.pyplot as plt

import random
toy1 = 'problems/toy/calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'
medium1 = 'problems/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'

RUTAJSON = medium1
VMAX = math.inf #Valor Maximo

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan

class evolutivoMALHECHO:
    def __init__(self, nGeneracionesMaximas, tamTorneo, tamPoblacion , tasaMutacion,aestrella, problema):
        self.candidatos = problema.candidatos
        self.nSoluciones = problema.number_stations
        if tamPoblacion != None:
            self.tamPoblacion = tamPoblacion
        else:
            self.tamPoblacion = (len(self.candidatos)//self.nSoluciones)
        self.poblacion = [0] * self.tamPoblacion
        self.fitnessSols = [VMAX] * len(self.candidatos)
        self.fitness = [VMAX] * self.tamPoblacion
        self.mejorFitness = VMAX
        self.mejorIndividuo = [0] * self.nSoluciones
        self.aestrella = aestrella
        self.problema = problema
        self.tamTorneo = tamTorneo
        self.tasaMutacion = tasaMutacion
        self.padres = []
        self.nGeneracionesMaximas = nGeneracionesMaximas
        self.tInicio = 0
        self.tFinal = 0
        self.poblacionDeCandidatos = 0
        self.calculadoPoblacionTotalCandidatos = False

    @lru_cache(maxsize=1280000)
    def functoolsCache(self, inicial, final):
        #print("2.DENTRO a AESTRELLA")
        return self.aestrella.busqueda(inicial,final)

    def nuestraCache(self, inicial, final):
        # Creamos la key de la cache con el inicial y final
        cache_key = (inicial, final)
        
        # Comprobamos si está en cache
        if cache_key in self.aestrella.cache:
            return self.aestrella.cache[cache_key]
        
        # Si no esta en cache calculamos y almacenamos en cache
        #print("2.DENTRO a AESTRELLA")
        result = self.aestrella.busqueda(inicial, final)
        self.aestrella.cache[cache_key] = result
        return result

    def inicializarN(self,nSoluciones):
        mejorFitness = VMAX
        mejorIndividuo = [0] * nSoluciones
        for i in range(len(self.poblacion)): 
            individuo = [0] * nSoluciones   #Un individuo esta compuesto por nSoluciones
            fitnessIndividuo = 0
            for j in range(nSoluciones): 
                #Cogemos uno random:
                index = random.randrange(len(self.candidatos))

                while index in individuo:
                    index = random.randrange(len(self.candidatos))

                #Calculamos su fitness / funcion evaluacion:
                individuo[j] = index
                # Si el individuo es mejor que el mejor de todos, lo guardamos
            fitnessIndividuo = self.calcularFitness(individuo)
            if (fitnessIndividuo < mejorFitness):
                mejorFitness = fitnessIndividuo
                mejorIndividuo = individuo
            self.poblacion[i] = individuo
            self.fitness[i] = fitnessIndividuo
        self.mejorFitness = mejorFitness
        #print("mejor fitness inicial: ",mejorFitness)
        return mejorIndividuo

    def calcularFitnessSolucion(self,solucionParcial):
        final = self.candidatos[solucionParcial]
        busqueda = 0
        if (self.fitnessSols[solucionParcial] != VMAX):
            return self.fitnessSols[solucionParcial]

        for inicial in self.candidatos:
            busqueda += self.nuestraCache(inicial[0], final[0])         # inicial[1] es poblacion 
                      # inicial[0] es identificador y final[0] es id final
            if not self.calculadoPoblacionTotalCandidatos:
                self.poblacionDeCandidatos += inicial[1]
        self.calculadoPoblacionTotalCandidatos = True
        sol = busqueda * self.poblacionDeCandidatos
        self.fitnessSols[solucionParcial] = sol
        return sol

    def calcularFitness(self,individuo):
        suma = 0
        sumaMinima = VMAX
        for candidato in individuo:
            suma = self.calcularFitnessSolucion(candidato)
            if suma < sumaMinima:
                sumaMinima = suma
        re = sumaMinima/self.poblacionDeCandidatos
        return re

    def seleccionGeneracionRango(self):#Seleccion por torneo
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
        hijos[0] = [0] * self.nSoluciones
        hijos[1] = [0] * self.nSoluciones
        #Cruce por un punto. Nos quedamos la mitad de soluciones parciales de cada padre

        if (len(str(padres[0]))<indiceCruce and len(str(padres[1]))<indiceCruce):
            hijos[0] = padres[0]
            hijos[1] = padres[1]
        else:   
#            hijos[0] = padres[1][:indiceCruce] + padres[0][indiceCruce:]
 #           hijos[1] = padres[0][:indiceCruce] + padres[1][indiceCruce:]
  #          if len(hijos[0]) > len(padres[0]):
   #             hijos[0] = padres[0]
    #        if len(hijos[1]) > len(padres[1]):
     #           hijos[1] = padres[1]
            for i in range(len(padres[0])):
                if i < indiceCruce or padres[1][i] in hijos[0] :
                    hijos[0][i]=padres[0][i]
                else:
                    hijos[0][i]=padres[1][i]

                if i < indiceCruce or padres[0][i] in hijos[1] :
                    hijos[1][i]=padres[1][i]
                else:
                    hijos[1][i]=padres[0][i]
        return hijos

    def mutacion(self, hijos):
        for i in range(len(hijos)): # Dos hijos, 0 y 1
#            nCambios = random.randint(0,self.nSoluciones-1)-self.nSoluciones//3 
 #           if nCambios > 0:
  #              #for j in range(nCambios):
   #             for j in range(len(hijos[i])):
    #                hijos[i][j] = random.randrange(len(self.candidatos))
            nRandom = random.random()
            if nRandom < self.tasaMutacion:
                indiceRandom = random.randrange(len(self.candidatos))
                while indiceRandom in hijos[i]:
                    indiceRandom = random.randrange(len(self.candidatos))
                hijos[i][random.randrange(len(hijos[i]))] = indiceRandom
        return hijos

    def genetico(self):
        self.tInicio = time.time()
        padres = [0] * 2
        hijos = [0] * 2
        self.mejorIndividuo = self.inicializarN(self.nSoluciones)
        y = []
        #print("Mejor individuo inicial: ", self.mejorIndividuo)
        for _ in range(self.nGeneracionesMaximas):
            y.append(self.mejorFitness)
            #Seleccionamos siguiente generacion de padres
            pGeneracion = self.seleccionGeneracionRango()
            #Cruzamos y mutamos toda la poblacion de dos en dos. (pGeneracion deberia de tener misma lon que poblacion)
            for i in range(0,len(pGeneracion)-1,2):
                #Seleccionamos dos padres
                padres[0] = self.poblacion[pGeneracion[i]]
                padres[1] = self.poblacion[pGeneracion[i+1]]
                #Cruce
                hijos = self.cruce(padres,(self.nSoluciones)//2)
                #Mutacion
                hijos = self.mutacion(hijos)
                #Reemplazo. Mantenemos el mejor individuo de la generacion pasada, a no ser que haya uno mejor
                for j in range(2): # 2 Hijos
                    fitnessHijo = self.calcularFitness(hijos[j])
                    #print("fitness hijo ",j,": ",fitnessHijo)
                    if (self.poblacion[i+j] != self.mejorIndividuo) or fitnessHijo < self.fitness[i+j]:
                        self.poblacion[i+j] = hijos[j]
                        self.fitness[i+j] = fitnessHijo
                        if fitnessHijo < self.mejorFitness:
                            #print("Ha encontrado un mejor individuo")
                            self.mejorIndividuo = hijos[j]
                            self.mejorFitness = fitnessHijo
        print("Fitness del mejor individuo final: ",self.mejorFitness)
        for ind in self.mejorIndividuo:
            print(self.candidatos[ind][0])
        self.tFinal = time.time()
        x = list(range(0,self.nGeneracionesMaximas))
        plt.plot(x,y)
        print("Tiempo de ejecución:",self.formatearTiempo(self.tFinal - self.tInicio))
        return self.mejorIndividuo
    #devuelve uno 
    def formatearTiempo(self, tiempo):  # Para imprimir los tiempos como en las soluciones
        horas = int(tiempo // 3600)
        minutos = int((tiempo % 3600) // 60)
        segundos = int(tiempo % 60)
        milisegundos = int((tiempo - int(tiempo)) * 1000000)
        return f"{horas:01d}:{minutos:02d}:{segundos:02d}.{milisegundos:06d}"

problema = Problema(RUTAJSON)
aestrella = AEstrella(problema, h2)
#nGeneracionesMaximas, tamTorneo, tamPoblacion , tasaMutacion
print(evolutivoMALHECHO(50, 5, 50, 1, aestrella, problema).genetico())
plt.show()
