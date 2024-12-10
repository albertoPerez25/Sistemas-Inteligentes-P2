from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3
import matplotlib.pyplot as plt
from evolutivoGeneral import evolutivo, VMAX
import random
from heapq import heappush,heappop

toy1 = 'problems/toy/calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'
medium1 = 'problems/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'
RUTAJSON = medium1

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan

class evolutivoFitness(evolutivo):
    def __init__(self, nGeneracionesMaximas, tamPoblacion, tasaMutacion, aestrella, problema):
        super().__init__(nGeneracionesMaximas, tamPoblacion, tasaMutacion, aestrella, problema)
        self.lfitness=[]
        self.ps=set()
    
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
            heappush(self.lfitness, fitnessIndividuo)  #Añadimos el fitnes del individuo
        self.mejorFitness = mejorFitness
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
    
    def seleccionGeneracion(self):   # Seleccion por fitness
        padresGeneracion = [0] * len(self.poblacion)
        tam = len(self.poblacion)
        pAcumulada = 0
        for i in range(1,tam+1):
            pAcumulada += ()    #Formula para calcular la probabilidad basada en el fitness
            self.ps.add(pAcumulada)
        for i in range(tam):
            aux = random.random()
            for prob in self.ps:
                if aux <= prob:
                    padresGeneracion[i] = heappop(self.rango)[1]
                    break
        if len(self.rango) != 0:
            raise Exception("No se vacia rango!")
        self.rango = []
        return padresGeneracion