from heapq import heappush,heappop
from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3

import random
Small1 = 'problems/small/calle_del_virrey_morcillo_albacete_250_3.json'

RUTAJSON = Small1
VMAX = 999999 #Valor Maximo

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan



class evolutivoMALHECHO:
    def __init__(self, poblacion, nGeneracionesMaximas, nSoluciones, tamTorneo, heuristica, problema):
        self.candidatos = problema.list_candidatos
        self.poblacion = []#[0] * len(self.candidatos)
        self.fitnessSols = [VMAX] * len(self.candidatos)
        self.tamTorneo = tamTorneo
        self.padres = []
        self.nGeneracionesMaximas = nGeneracionesMaximas
        self.nGeneracion = 0

    def inicializarN(self,nSoluciones):
        for _ in range(len(self.candidatos)): #Un individuo esta compuesto por nSoluciones
            individuo = set()
            fitnessIndividuo = 0
            for _ in range(nSoluciones): 
                #Cogemos uno random:
                index = random.randrange(len(self.candidatos))
                #Calculamos su fitness / funcion evaluacion:
                fitnessIndividuo = self.calcularFitnessSolucion(index)
                self.fitnessSols[index] = fitnessIndividuo
                #self.poblacion[index] = 1 #antes era soluciones
                individuo.add(index)
            self.poblacion.append(individuo,fitnessIndividuo)

    def calcularFitnessSolucion(self,solucionParcial):
        final = self.candidatos[solucionParcial]
        suma = 0
        if (self.fitnessSols[solucionParcial] != VMAX):
            return self.fitnessSols[solucionParcial]
        for inicial in self.candidatos:
            #inicial[1] = poblacion, inicial[0] = identificador, final[0] = id final
            suma = (inicial[1] * AEstrella(problema,self.heuristica,inicial[0],final[0])) + suma
        #self.fitness[individuo] = suma
        #heappush(self.fitness, (suma, individuo))
        #poblacion
        #self.soluciones[individuo] = 1
        return suma

#    def seleccionPadres(self):#MAL HECHO NO HACER CASO
        #Cogemos los dos mejores entre n random:    Podria hacerse con una PriorityQueue, seria mejor?
        padres = [0] * 2
        indiceAux = random.randrange(len(self.candidatos))

        for _ in range(self.tamTorneo):
            indiceAux = random.randrange(len(self.candidatos))
            for i in range(len(padres)-1): #Hace Npadres vueltas. No deberia añadir nada de complejidad con 2 padres
                if self.fitnessSols[indiceAux] < padres[i]:
                    padres[i] = indiceAux
        return padres
    
    def seleccionGeneracion(self):#Seleccion por torneo
        #Cogemos los mejores entre n random:    Podria hacerse con una PriorityQueue, seria mejor?      
        padresGeneracion = []
        for _ in range(self.poblacion):
            mejorFitness = (VMAX,0) #fitness,indice candidatos
            for _ in range (self.tamTorneo):
                indiceAux = random.randrange(len(self.poblacion))
                if self.fitnessSols[self.poblacion[indiceAux]] < mejorFitness[0]:
                    mejorFitness[0] = self.fitnessSols[self.poblacion[indiceAux]] #Como estara almacenado en el diccionario no añadira complejidad
                    mejorFitness[1] = self.poblacion[indiceAux]
            padresGeneracion.append(mejorFitness[1]) #Metemos el indice del mejor candidato de cada torneo
        return padresGeneracion

    def cruce(self, padres, indiceCruce):
        hijos = [0] * 2
        #Cruce por un punto
        if random.randrange(3) == 1:
            hijos[0] = padres[0]
            hijos[1] = padres[1]
        else:
            #hijos[0] = padres[1][:indiceCruce] + padres[0][indiceCruce:]
            #hijos[1] = padres[0][:indiceCruce] + padres[1][indiceCruce:]
            hijos[0] = padres[1]//10**indiceCruce + padres[0]%10**indiceCruce
            hijos[1] = padres[0]//10**indiceCruce + padres[1]%10**indiceCruce
            if hijos[0] >= len(self.candidatos):
                hijos[0] = padres[0]
            if hijos[1] >= len(self.candidatos):
                hijos[1] = padres[1]
        return hijos

    def mutacion(self, hijos):
        for i in range(len(hijos)):
            if random.randint(0,1) == 0:
                hijos[i] = 10 ** random.randint(0, len(str(len(self.poblacion)-1)))
        return hijos

    def genetico(self):
        padres = [0] * 2
        hijos = [0] * 2
        self.inicializarN(self.nSoluciones)
        #for nGeneracion in range(self.nGeneracionesMaximas):
        while (self.nGeneracion < self.nGeneracionesMaximas):
            #Seleccionamos siguiente generacion de padres
            pGeneracion = self.seleccionGeneracion()
            #Cruzamos y mutamos toda la poblacion de dos en dos. (pGeneracion deberia de tener misma lon que poblacion)
            for i in range(len(pGeneracion),2):
                #Seleccionamos dos padres
                padres[0] = pGeneracion[i]
                padres[1] = pGeneracion[i+1]
                #Cruce
                hijos = self.cruce(padres,len(str(len(self.poblacion)-1))//2)
                #Mutacion
                hijos = self.mutacion(hijos)
            #Reemplazo

            #Calculamos fitness 


            self.nGeneracion += 1
               

    #devuelve uno 
problema = Problema(RUTAJSON)
evolutivoMALHECHO(4, h2, problema)

