from abc import ABCMeta, abstractmethod
from claseBusqueda import Busqueda
from queue import PriorityQueue # Para la PriorityQueue
# https://docs.python.org/3/library/queue.html#queue.PriorityQueue



class BusquedaInformada(Busqueda,metaclass=ABCMeta):
    def __init__(self, problema, heuristica):
        super().__init__(problema)
        self.frontera = PriorityQueue() # Frontera se usará como PriorityQueue de nodos a ser expandidos
        self.H = heuristica
        self.cacheHeuristica = {}
    @abstractmethod
    def añadirNodoAFrontera(self, nodo, frontera):
        pass

    def extraerNodoDeFrontera(self, frontera):  # Igual en PrimeroMejor y AEstrella
        return frontera.get()[1]                # Sacamos el nodo que toca
    
    def esVacia(self, frontera):                # Igual en PrimeroMejor y AEstrella
        return frontera.empty()
    
    def cache_heuristica(self, nodo):
        # Crear la key de la cache con el id del estado del nodo
        key_cache = (nodo.estado.identifier)
        
        # Comprobamos si esta en la cache
        if key_cache in self.cache:
            return self.cache[key_cache]
        
        # Si no esta en la cache, guardamos el coste
        resultado = self.H.heuristica(nodo, self.final)
        self.cache[key_cache] = resultado
        return resultado

class PrimeroMejor(BusquedaInformada):
    def añadirNodoAFrontera(self, nodo, frontera):
        frontera.put((self.H.heuristica(nodo), nodo))   # Una tupla con su heuristica y el propio nodo  
                                                        # Si la heuristica es igual se elige el de menor id                                                                            
class AEstrella(BusquedaInformada):
    def añadirNodoAFrontera(self, nodo, frontera):
        gn = nodo.coste   
        hn = self.cache_heuristica(nodo)                # Almacenamos en una cache la heuristica de un estado
        fn = hn + gn   
        frontera.put((fn, nodo))                                                     
    
    