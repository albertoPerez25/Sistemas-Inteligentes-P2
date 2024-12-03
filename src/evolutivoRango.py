from heapq import heappush,heappop
import math
import time
from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3
from functools import lru_cache
import matplotlib.pyplot as plt
#from evolutivo1 import evolutivoMALHECHO

import random
toy1 = 'problems/toy/calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'
medium1 = 'problems/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'

RUTAJSON = medium1
VMAX = math.inf #Valor Maximo
NGENS = 100000

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan

class evolutivoRango():
    def __init__(self, nGeneracionesMaximas, aestrella, problema):
        self.candidatos = problema.candidatos
        self.nSoluciones = problema.number_stations
        self.poblacion = [0] * ((len(self.candidatos))//self.nSoluciones)
        self.fitnessSols = [VMAX] * len(self.candidatos)
        self.fitness = [VMAX] * (len(self.candidatos)//self.nSoluciones)
        self.mejorFitness = VMAX
        self.mejorIndividuo = [0] * self.nSoluciones
        self.aestrella = aestrella
        self.problema = problema
        self.padres = []
        self.nGeneracionesMaximas = nGeneracionesMaximas
        self.tInicio = 0
        self.tFinal = 0
        self.rango = []
        self.ps = set()

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
                #Calculamos su fitness / funcion evaluacion:
                individuo[j] = index
                # Si el individuo es mejor que el mejor de todos, lo guardamos
            fitnessIndividuo = self.calcularFitness(individuo)
            if (fitnessIndividuo < mejorFitness):
                mejorFitness = fitnessIndividuo
                mejorIndividuo = individuo
            self.poblacion[i] = individuo
            self.fitness[i] = fitnessIndividuo
            heappush(self.rango, (fitnessIndividuo, i))
        self.mejorFitness = mejorFitness
        return mejorIndividuo

    def calcularFitnessSolucion(self,solucionParcial):
        final = self.candidatos[solucionParcial]
        suma = 0
        if (self.fitnessSols[solucionParcial] != VMAX):
            return self.fitnessSols[solucionParcial]
        for inicial in self.candidatos:
            #inicial[1] -> poblacion, inicial[0] -> identificador, final[0] = id final
            busqueda = self.nuestraCache(inicial[0], final[0])
            suma = (inicial[1] * busqueda) + suma
        self.fitnessSols[solucionParcial] = suma
        return suma

    def calcularFitness(self,individuo):
        suma = 0
        for i in individuo:
            suma = suma + self.calcularFitnessSolucion(i)
        return suma

    def seleccionGeneracionRango(self):#Seleccion por rango
        padresGeneracion = [0] * len(self.poblacion)
        tam = len(self.poblacion)
        pAcumulada = 0
        for i in range(1,tam+1):
            pAcumulada += (2*(tam - i + 1)/(tam**2 + tam))
            self.ps.add(pAcumulada)
        for i in range(tam):
            aux = random.random()
            for prob in self.ps:
                if aux <= prob:
                    padresGeneracion[i] = heappop(self.rango)[1]
                    break
        if len(self.rango) != 0:
            raise Exception("No se vacia rango!")
        return padresGeneracion

    def cruce(self, padres, indiceCruce):
        hijos = [0] * 2
        #Cruce por un punto. Nos quedamos la mitad de soluciones parciales de cada padre
        if (random.randrange(2) == 1) or (len(str(padres[0]))>indiceCruce and len(str(padres[1]))>indiceCruce):
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
            nCambios = random.randint(0,self.nSoluciones-1)-self.nSoluciones//3 
            if nCambios > 0:
                for j in range(nCambios):
                    hijos[i][j] =  random.randrange(len(self.candidatos))
        return hijos

    def genetico2(self):
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
                hijos = self.cruce(padres,len(str(len(self.poblacion)-1))//2)
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
                    heappush(self.rango, (self.fitness[i+j], i+j))
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
print(evolutivoRango(NGENS, aestrella, problema).genetico2())
plt.show()