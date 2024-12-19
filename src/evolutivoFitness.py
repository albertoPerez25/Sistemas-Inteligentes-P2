from clasesBasicas import Problema 
from BusquedasInformadas import AEstrella
from clasesHeuristica import Heuristica1,Heuristica2,Heuristica3
import matplotlib.pyplot as plt
from evolutivoGeneral import Evolutivo, VMAX
import random
from heapq import heappush,heappop

toy1 = 'problems/toy/calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'
medium1 = 'problems/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'
medium2 = 'problems/medium/calle_palmas_de_gran_canaria_albacete_500_2_candidates_167_ns_23.json'
RUTAJSON = medium2

h1 = Heuristica1(Problema(RUTAJSON)) # Euclidea
h2 = Heuristica2(Problema(RUTAJSON)) # Geodesica
h3 = Heuristica3(Problema(RUTAJSON)) # Manhattan

class evolutivoFitness(Evolutivo):
    def __init__(self, nGeneracionesMaximas, tamPoblacion, tasaMutacion, tasaCruce, aestrella, problema):
        super().__init__(nGeneracionesMaximas, tamPoblacion, tasaMutacion, tasaCruce, aestrella, problema)
        self.lfitness=[]
        self.ps=set()
        self.fitTotal=0
    
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
            self.fitTotal=self.fitTotal+fitnessIndividuo
            if (fitnessIndividuo < mejorFitness):
                mejorFitness = fitnessIndividuo
                mejorIndividuo = individuo
            self.poblacion[i] = individuo
            self.fitness[i] = fitnessIndividuo
            #heappush(self.lfitness, (fitnessIndividuo,i))  #Añadimos el fitnes del individuo
            self.lfitness.append((fitnessIndividuo,i))     #Añadimos el fitnes del individuo
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
    
    def seleccionGeneracion(self):   # Seleccion por fitness
        self.lfitness.sort() #Ordenamos los fitnesses para la formula del fitness
        padresGeneracion = [0] * len(self.poblacion)
        longPoblacion = len(self.poblacion)
        pAcumulada = 0
        fitTotal=0
        #for j in range(longPoblacion):             Antes calculabamos aqui fitTotal pero lo pasamos a calcular fuera para ahorrar tiempo y coste
        #    fitTotal=fitTotal+self.lfitness[j][0]
        for i in range(longPoblacion):
            pAcumulada += 1/(self.lfitness[i][0]/self.fitTotal)    #Formula para calcular la probabilidad basada en el fitness
            #pAcumulada=1/pAcumulada
            self.ps.add(pAcumulada)
        for i in range(longPoblacion):
            aux = random.random()
            for prob in self.ps:
                if aux <= prob:
                    #padresGeneracion[i] = heappop(self.lfitness)[1]
                    padresGeneracion[i] = self.lfitness.pop()[1]
                    break
        if len(self.lfitness) != 0:
            raise Exception("lfitness vacio exception")
        self.lfitness = []
        return padresGeneracion
    
    def cruce(self, padres, indiceCruce):
        hijos = [0] * 2
        hijos[0] = [0] * self.nSoluciones
        hijos[1] = [0] * self.nSoluciones
        nRandom = random.random()
        if (len(str(padres[0]))<indiceCruce and len(str(padres[1]))<indiceCruce or nRandom>self.tasaCruce):
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

    def cruceMascara(self, padres, indiceCruce):
        hijos=[0]*2
        hijos[0] = [0] * self.nSoluciones
        hijos[1] = [0] * self.nSoluciones
        mascara=[]
        nRandom = random.random()
        for _ in range(self.nSoluciones):
            mascara.append(random.randint(0,1))
        if (len(str(padres[0]))<indiceCruce and len(str(padres[1]))<indiceCruce or nRandom>self.tasaCruce):
            hijos[0] = padres[0]
            hijos[1] = padres[1]
        else: 
            cont=0
            for bit in mascara:
                if bit == 0:
                    hijos[0][cont]=padres[0][cont]
                    hijos[1][cont]=padres[1][cont]
                else:
                    hijos[0][cont]=padres[1][cont]
                    hijos[1][cont]=padres[0][cont]
                cont=cont+1
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
        self.fitTotal=0
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
            #heappush(self.lfitness, (self.fitness[i+j], i+j))
            self.lfitness.append((self.fitness[i+j], i+j))
            self.fitTotal=self.fitTotal+self.fitness[i+j]


problema = Problema(RUTAJSON)
aestrella = AEstrella(problema, h2)
#nGeneracionesMaximas, tamPoblacion , tasaMutacion, tasaCruce
print(evolutivoFitness(80, 100, .1, 1, aestrella, problema).genetico())
plt.show()