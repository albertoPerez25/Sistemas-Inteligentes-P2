from abc import ABC, abstractmethod
from math import sqrt
from geopy.distance import geodesic # Libreria que calcula de manera exacta la distancia geodesica

class Heuristica(ABC):
    def __init__(self,problema):
        self.problema = problema
    
    @abstractmethod
    def distancia(self,estado,final):
        pass

    # Devuelve el tiempo estimado (coste) desde un estado hasta el estado final
    def tiempo(self, distancia):
        return distancia/self.problema.maxSpeed # D->m V->m/s T->s
    
    # Metodo al que llamamos para calcular la heurística.
    def heuristica(self, nodo):
        return self.tiempo(self.distancia(nodo.estado,self.problema.Final))
    
# Dos maneras de hacer heuristicas calculando distancias
class Heuristica1(Heuristica):
    # Euclidea. Pitagoras. (Línea recta)
    def distancia(self, estado, final):
        return sqrt((estado.latitude - final.latitude)**2 + (estado.longitude - final.longitude)**2)*100000
    
class Heuristica2(Heuristica):
    # Geodesica. (Línea recta + curvatura de la Tierra)
    def distancia(self, estado, final):
        return geodesic((estado.latitude,estado.longitude), (final.latitude,final.longitude)).meters # La usan en las soluciones. Mas exacta al ser la tierra una elipse
    # https://pypi.org/project/geopy/
    # https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://geopy.readthedocs.io/&ved=2ahUKEwiWq97Su7OJAxUt_7sIHanJI7kQFnoECBYQAQ&usg=AOvVaw01VCwbF-UadfgLzmTCV4Mo

class Heuristica3(Heuristica):
    # Distancia de Manhattan. Diferencia en latitudes y longitudes.
    def distancia(self,estado,final):
        return abs(estado.latitude - final.latitude) + abs(estado.longitude - final.longitude)