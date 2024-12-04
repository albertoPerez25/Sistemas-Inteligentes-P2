import math
from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3
import matplotlib.pyplot as plt
from evolutivoGeneral import evolutivo,VMAX

import random
toy1 = 'problems/toy/calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'
medium1 = 'problems/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'

RUTAJSON = medium1

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan

class evolutivoTorneo(evolutivo):
    def __init__(self, nGeneracionesMaximas, tamTorneo, tamPoblacion, tasaMutacion, aestrella, problema):
        super().__init__(nGeneracionesMaximas, tamPoblacion, tasaMutacion, aestrella, problema)
        self.tamTorneo = tamTorneo

    def inicializarN(self,nSoluciones):
        mejorFitness = VMAX
        mejorIndividuo = [0] * nSoluciones
        
        for i in range(len(self.poblacion)): 
            individuo = [0] * nSoluciones   # Un individuo esta compuesto por nSoluciones
            fitnessIndividuo = 0

            for j in range(nSoluciones): 
                index = random.randrange(len(self.candidatos))         # Cogemos uno random
                while index in individuo:
                    index = random.randrange(len(self.candidatos))
                individuo[j] = index                                   # Calculamos su fitness / funcion evaluacion:
            fitnessIndividuo = self.calcularFitness(individuo)         # Si el individuo es mejor que el mejor de todos, lo guardamos
            
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
            busqueda += self.nuestraCache(inicial[0], final[0])     # inicial[1] es poblacion 
            if not self.calculadoPoblacionTotalCandidatos:          # inicial[0] es identificador y final[0] es id final
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

    def seleccionGeneracion(self):                 # Seleccion por torneo 
        padresGeneracion = [0] * len(self.poblacion)    # Cogemos los mejores entre n random:  
        for i in range(len(self.poblacion)):
            mejorFitness = VMAX     # fitness
            mejorIndividuo = 0      # indice en poblacion
            for _ in range (self.tamTorneo):
                indiceAux = random.randrange(len(self.poblacion))
                if self.fitness[indiceAux] < mejorFitness:
                    mejorFitness = self.fitness[indiceAux]  # Como estara almacenado en el diccionario no añadira complejidad
                    mejorIndividuo = indiceAux
            padresGeneracion[i] = mejorIndividuo            # Metemos el indice del mejor candidato de cada torneo
        return padresGeneracion

    def cruce(self, padres, indiceCruce):       # Cruce por un punto. Nos quedamos la mitad de soluciones parciales de cada padre
        hijos = [0] * 2
        hijos[0] = [0] * self.nSoluciones
        hijos[1] = [0] * self.nSoluciones
        if (len(str(padres[0]))<indiceCruce and len(str(padres[1]))<indiceCruce):
            hijos[0] = padres[0]
            hijos[1] = padres[1]
        else:   
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
            nRandom = random.random()
            if nRandom < self.tasaMutacion:
                indiceRandom = random.randrange(len(self.candidatos))
                while indiceRandom in hijos[i]:
                    indiceRandom = random.randrange(len(self.candidatos))
                hijos[i][random.randrange(len(hijos[i]))] = indiceRandom
        return hijos
    
    def reemplazar(self, hijos, i):
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

problema = Problema(RUTAJSON)
aestrella = AEstrella(problema, h2)
#nGeneracionesMaximas, tamTorneo, tamPoblacion , tasaMutacion
print(evolutivoTorneo(50, 5, 3, 1, aestrella, problema).genetico())
plt.show()
