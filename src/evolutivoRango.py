from heapq import heappush,heappop
from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3
import matplotlib.pyplot as plt
from evolutivoGeneral import Evolutivo, VMAX

import random
toy1 = 'problems/toy/calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'
medium1 = 'problems/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json' 
medium2 = 'problems/medium/calle_palmas_de_gran_canaria_albacete_500_2_candidates_167_ns_23.json' #tarda mas
medium3 = 'problems/medium/calle_f_albacete_2000_0_candidates_25_ns_4.json'

large1 = 'problems/large/calle_cardenal_tabera_y_araoz_albacete_1000_2_candidates_104_ns_22.json'
large2 = 'problems/huge/calle_de_josé_carbajal_albacete_5000_2_candidates_537_ns_12.json'
large3 = 'problems/large/calle_herreros_albacete_1000_4_candidates_496_ns_14.json'
large4 = 'problems/large/calle_industria_albacete_1000_0_candidates_122_ns_8.json'
large5 = 'problems/large/calle_industria_albacete_1000_2_candidates_549_ns_71.json'

huge1 = 'problems/huge/calle_de_josé_carbajal_albacete_2000_2_candidates_1254_ns_110.json'

RUTAJSON = large1

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan

class evolutivoRango(Evolutivo):
    def __init__(self, nGeneracionesMaximas, tamPoblacion, tasaMutacion, aestrella, problema):
        super().__init__(nGeneracionesMaximas, tamPoblacion, tasaMutacion, aestrella, problema)
        self.rango = []
        self.ps = set()

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
            #heappush(self.rango, (fitnessIndividuo, i))
            self.rango.append((fitnessIndividuo,i))
        self.rango.sort()
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

    def calcularFitnessAntiguo(self,individuo):
        suma = 0
        sumaMinima = VMAX
        for candidato in individuo:
            suma = self.calcularFitnessSolucion(candidato)
            if suma < sumaMinima:
                sumaMinima = suma
        re = sumaMinima/self.poblacionDeCandidatos
        return re
    
    def calcularFitness(self,individuo):
        tiempos = 0
        for inicial in self.candidatos: #I
            if not self.calculadoPoblacionTotalCandidatos: 
                self.poblacionDeCandidatos += inicial[1] # inicial[1] es la poblacion de un candidato
            tiempo = VMAX                                # inicial[0] es identificador del inicial
            tiempoMin = VMAX
            for final in individuo: #J
                tiempo = self.nuestraCache(inicial[0],self.candidatos[final][0])
                tiempoMin = min(tiempo,tiempoMin)       # si inicial = final no hacemos if pq tarda mas
            tiempos += tiempoMin * inicial[1]
        self.calculadoPoblacionTotalCandidatos = True
        return tiempos/self.poblacionDeCandidatos

    def seleccionGeneracion(self):   # Seleccion por rango
        self.ps = set()
        padresGeneracion = [0] * len(self.poblacion)
        tam = len(self.poblacion)
        pAcumulada = 0
        for i in range(1,tam+1):                            # En la formula el primer elemento es 1, no 0
            pAcumulada += (2*(tam - i + 1)/(tam**2 + tam))
            self.ps.add(pAcumulada)
        for i in range(tam):
            aux = random.random()
            for prob in self.ps:
                if aux <= prob:
                    #padresGeneracion[i] = heappop(self.rango)[1]
                    padresGeneracion[i] = self.rango.pop()[1]
                    break
        if len(self.rango) != 0:
            raise Exception("No se vacia rango!")
        self.rango = []
        return padresGeneracion

    def cruce(self, padres, indiceCruce):
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
            #heappush(self.rango, (self.fitness[i+j], i+j))
            self.rango.append((self.fitness[i+j], i+j))
            self.rango.sort()


problema = Problema(RUTAJSON)
aestrella = AEstrella(problema, h2)
random.seed()
#nGeneracionesMaximas, tamPoblacion , tasaMutacion
print(evolutivoRango(80, 100, .9, aestrella, problema).genetico())
plt.show()
