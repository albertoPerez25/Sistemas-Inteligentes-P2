import math
import time
from functools import lru_cache
import matplotlib.pyplot as plt
from abc import ABC,abstractmethod

VMAX = math.inf #Valor Maximo

class evolutivo(ABC):
    def __init__(self, nGeneracionesMaximas, tamPoblacion , tasaMutacion,aestrella, problema):
        self.candidatos = problema.candidatos
        self.nSoluciones = problema.number_stations
        if tamPoblacion != None:
            self.tamPoblacion = tamPoblacion
            if tamPoblacion%2!=0:
                self.tamPoblacion = tamPoblacion + 1
        else:
            self.tamPoblacion = (len(self.candidatos)//self.nSoluciones)
        self.poblacion = [0] * self.tamPoblacion
        self.fitnessSols = [VMAX] * len(self.candidatos)
        self.fitness = [VMAX] * self.tamPoblacion
        self.mejorFitness = VMAX
        self.mejorIndividuo = [0] * self.nSoluciones
        self.aestrella = aestrella
        self.problema = problema
        self.tasaMutacion = tasaMutacion
        self.padres = []
        self.nGeneracionesMaximas = nGeneracionesMaximas
        self.tInicio = 0
        self.tFinal = 0
        self.poblacionDeCandidatos = 0
        self.calculadoPoblacionTotalCandidatos = False

    @lru_cache(maxsize=1280000)
    def functoolsCache(self, inicial, final):
        return self.aestrella.busqueda(inicial,final)

    def nuestraCache(self, inicial, final):
        # Creamos la key de la cache con el inicial y final
        cache_key = (inicial, final)
        
        # Comprobamos si está en cache
        if cache_key in self.aestrella.cache:
            return self.aestrella.cache[cache_key]
        
        # Si no esta en cache calculamos y almacenamos en cache
        result = self.aestrella.busqueda(inicial, final)
        self.aestrella.cache[cache_key] = result
        return result

    @abstractmethod
    def inicializarN(self,nSoluciones):
        pass
    @abstractmethod
    def calcularFitnessSolucion(self,solucionParcial):
        pass
    @abstractmethod
    def calcularFitness(self,individuo):
        pass
    @abstractmethod
    def seleccionGeneracion(self):#Seleccion por torneo
        pass
    @abstractmethod
    def cruce(self, padres, indiceCruce):
        pass
    @abstractmethod
    def mutacion(self, hijos):
        pass
    @abstractmethod
    def reemplazar(self, hijos, i):
        pass

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
            pGeneracion = self.seleccionGeneracion()
            #Cruzamos y mutamos toda la poblacion de dos en dos. (pGeneracion deberia de tener misma lon que poblacion)
            for i in range(0,len(pGeneracion),2):
                #Seleccionamos dos padres
                padres[0] = self.poblacion[pGeneracion[i]]
                padres[1] = self.poblacion[pGeneracion[i+1]]
                #Cruce
                hijos = self.cruce(padres,(self.nSoluciones)//2)
                #Mutacion
                hijos = self.mutacion(hijos)
                #Reemplazo. Mantenemos el mejor individuo de la generacion pasada, a no ser que haya uno mejor
                self.reemplazar(hijos, i)
        #Finalización
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

