#clase abstracta que tendrá busqueda(), expandir(), estadisticas() e imprimirResultado()
from clasesBasicas import Nodo
from abc import ABC,abstractmethod
import time

class Busqueda(ABC):
    def __init__(self, problema):
        self.frontera = None # Se inicializará al tipo que le corresponda a cada algoritmo
        self.problema = problema
        self.tInicio = 0
        self.tFinal = 0
        self.cerrados = set()        # Para no volver a expandir nodos ya visitados
        self.nodo = Nodo(problema.Inicial)
        # Estadisticas:
        self.nExpandidos = 0
        self.nProfundidad = 0
        self.nCosteTotal = 0           
        self.nGenerados = 0

    def expandir(self,nodo,problema):
        acciones = problema.getAccionesDe(nodo.estado.identifier)
        while not acciones.empty():            
            accion = acciones.get()
            sucesor = Nodo(problema.getEstado(accion.destination))
            sucesor.padre = nodo
            sucesor.accion = accion
            sucesor.coste = nodo.coste + accion.time
            sucesor.profundidad = nodo.profundidad + 1
            self.nGenerados = self.nGenerados + 1
            sucesor.nGenerado = self.nGenerados
            self.añadirNodoAFrontera(sucesor, self.frontera)    # Añadimos los sucesores a frontera.
                                                                # Nos ahorramos un bucle For al añadirlos 
                                                                # desde expandir
                                                            
    def busqueda(self):
        self.tInicio = time.time()
        self.añadirNodoAFrontera(self.nodo,self.frontera)
        while(not self.esVacia(self.frontera)): 
            self.nodo = self.extraerNodoDeFrontera(self.frontera)
            if (self.nodo.estado.__eq__(self.problema.Final)):
                self.tFinal = time.time()
                return self.listaAcciones(self.nodo)
            if (not self.nodo.estado.identifier in self.cerrados):
                self.expandir(self.nodo, self.problema)     # Obtenemos los sucesores con Expandir()
                self.nExpandidos = self.nExpandidos + 1
                self.cerrados.add(self.nodo.estado.identifier)
        self.tFinal = time.time()
        return self.imprimirResultado([])

    def listaAcciones(self,nodo):
        sol = []                         # Lista de acciones que han llevado desde el final al inicial
        estados = []                     # Lista de ids de los estados desde el final al inicial
        self.nCosteTotal = nodo.coste    # nodo.coste es acumulativo
        self.nProfundidad=nodo.profundidad
        while (nodo.padre):
            sol.append(nodo.accion)
            estados.append(nodo.estado.identifier)
            nodo = nodo.padre
        #estados.append(nodo.estado.identifier) # Añadimos el inicial
        sol.reverse()                   # Ahora es una lista de acciones desde el inicial al final.
        self.imprimirResultado(sol)     # Le damos la vuelta para que salga como en la solución proporcionada.
        estados.reverse()               # Le damos la vuelta a las intersecciones tambien
        return estados

    def imprimirResultado(self,sol):
        if not sol : print("Solución no encontrada")
        print("Nodos generados:",self.nGenerados)
        print("Nodos expandidos:",self.nExpandidos)
        print("Tiempo de ejecución:",(self.formatearTiempo(self.tFinal - self.tInicio)),"segundos")
        print("Profundidad:",self.nProfundidad)
        print("Coste de la solución:",self.formatearTiempo(self.nCosteTotal))
        print("Solución:",sol)
    
    def formatearTiempo(self, tiempo):  # Para imprimir los tiempos como en las soluciones
        horas = int(tiempo // 3600)
        minutos = int((tiempo % 3600) // 60)
        segundos = int(tiempo % 60)
        milisegundos = int((tiempo - int(tiempo)) * 1000000)
        return f"{horas:01d}:{minutos:02d}:{segundos:02d}.{milisegundos:06d}"

    @abstractmethod
    def añadirNodoAFrontera(self, nodo, frontera):
        pass
    @abstractmethod
    def extraerNodoDeFrontera(self, frontera):
        pass
    @abstractmethod
    def esVacia(self, frontera):
        pass