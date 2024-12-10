#clase abstracta que tendrá busqueda(), expandir(), estadisticas() e imprimirResultado()
import math
from clasesBasicas import Nodo
from abc import ABC,abstractmethod

class Busqueda(ABC):
    def __init__(self, problema):
        self.frontera = None # Se inicializará al tipo que le corresponda a cada algoritmo
        self.problema = problema
        self.cerrados = None        # Para no volver a expandir nodos ya visitados
        self.inicial = None
        self.nodo = None
        self.final = None
        self.cache = {}

    def nuestraCache(self, inicial, destino, coste):
        # Crear la key de la cache con inicial y destino
        key_cache = (inicial, destino)
        
        # Comprobamos si esta en la cache
        if key_cache in self.cache:
            return self.cache[key_cache]
        
        # Si no esta en la cache, guardamos el coste
        self.cache[key_cache] = coste


    def expandir(self,nodo,problema):
        acciones = problema.getAccionesDe(nodo.estado.identifier)
        #while not len(acciones) == 0:          
        for accion in acciones: 
            # Cambiado a for porque ahora es una lista segmentos
            sucesor = Nodo(problema.getEstado(accion.destination))
            sucesor.padre = nodo
            sucesor.accion = accion
            sucesor.coste = nodo.coste + accion.time
            if (sucesor.estado.identifier in self.problema.candidatos[0]):
                self.nuestraCache(nodo.estado.identifier,sucesor.estado.identifier,sucesor.coste)
            sucesor.profundidad = nodo.profundidad + 1
            self.añadirNodoAFrontera(sucesor, self.frontera)    # Añadimos los sucesores a frontera.
                                                                # Nos ahorramos un bucle For al añadirlos 
                                                                # desde expandir
    def busqueda(self,inicial,final):
        self.inicial = self.problema.getEstado(inicial)
        self.nodo = Nodo(self.inicial)
        self.final = self.problema.getEstado(final)
        self.cerrados = set()        # Para no volver a expandir nodos ya visitados
        self.vaciar_frontera()
        self.añadirNodoAFrontera(self.nodo,self.frontera)
        while(not self.esVacia(self.frontera)): 
            self.nodo = self.extraerNodoDeFrontera(self.frontera)
            if (self.nodo.estado == (self.final)):     # Cambio de .eq a ==
                return self.nodo.coste 
            if (not self.nodo.estado.identifier in self.cerrados):
                self.expandir(self.nodo, self.problema)     # Obtenemos los sucesores con Expandir()
                self.cerrados.add(self.nodo.estado.identifier)
        return 9999

    @abstractmethod
    def añadirNodoAFrontera(self, nodo, frontera):
        pass
    @abstractmethod
    def extraerNodoDeFrontera(self, frontera):
        pass
    @abstractmethod
    def esVacia(self, frontera):
        pass
    @abstractmethod
    def vaciar_frontera(self):
        pass