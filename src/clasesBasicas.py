#GRUPO 9 - 3ºB esiiab
#ALBERTO PEREZ ALVAREZ
#MARCOS LOPEZ GOMEZ
import json
from queue import PriorityQueue


#Interseccion:
class Estado:
    def __init__(self, id, latitude, longitude):
        self.identifier = id
        self.latitude = latitude
        self.longitude = longitude
    def __str__(self):
        return f"Interseccion: (id={self.identifier}, latitud={self.latitude}, longitud={self.longitude})"
    def __repr__(self):
        return f"{self.identifier}"
    def __eq__(self, otro):
        if not isinstance(otro, Estado):
            return False
        else:
            return self.identifier == otro.identifier
    def __lt__(self, otro):
        return self.identifier < otro.identifier

#Segmento:    
class Accion:
    def __init__(self, origin, destination, distance, speed):
        self.origin = origin
        self.destination = destination
    # Dan la velocidad en Km/h y la distancia en m
        self.time = (distance/(speed*(10/36))) # Usamos: D->m. T->s y V->m/s
    def __str__(self):
        return f"Calle: Origen: {self.origin}, Destino: {self.destination})"
    def __repr__(self):
        return f"{self.origin} → {self.destination} ({self.time})"
    def __eq__(self, otro):
        if not isinstance(otro, Accion):
            return False
        else:
            return self.origin == otro.origin and self.destination == otro.destination and self.time == otro.time
    def __lt__(self, otro):
        return self.destination < otro.destination
    
class Problema:   
    #Constructor de Problema
    def __init__(self,ruta):
        with open(ruta, 'r') as file:
            self.data = json.load(file)
        
        self.dic_estados = {}
        self.dic_acciones = {}
        self.maxSpeed = 0

        # Pasamos las intersecciones del JSON a un nuevo diccionario estados
        for inter in self.data['intersections']:
            self.dic_estados.update({inter['identifier']:(Estado(inter['identifier'], inter['latitude'], inter['longitude']))})         
            self.dic_acciones.update({inter['identifier']:PriorityQueue()})  # Acciones = {id:PriorityQueue de Acciones}
            
        # Cargamos los nodos iniciales y finales del JSON.
        self.Inicial = self.dic_estados[self.data["initial"]]
        self.Final = self.dic_estados[self.data["final"]]
        
        # Pasamos los segmentos del JSON a un nuevo diccionario acciones     
        for seg in self.data['segments']:
            if (seg['speed']*(10/36) > self.maxSpeed):
                self.maxSpeed = seg['speed']*(10/36) # km/h -> m/s
            accion=Accion(seg['origin'], seg['destination'], seg['distance'], seg['speed'])
            self.dic_acciones[seg['origin']].put(accion)  # Metemos las acciones de cada Estado en una PriorityQueue

    # Obtener un objeto Estado a partir de su ID
    def getEstado(self, id):
        return self.dic_estados[id]

    # Obtener todas las acciones de un estado a partir de su ID
    def getAccionesDe(self,id):
        return self.dic_acciones[id]

class Nodo:
    def __init__(self, interseccion, padre = None, accionTomada = None, coste = 0, profundidad = 0, nGenerado = 0):
        self.estado = interseccion
        self.padre = padre
        self.accion = accionTomada
        self.coste = coste
        self.profundidad = profundidad
        self.nGenerado = nGenerado  # El 1º generado deberia empezar en 1 no en 0, pues dijo en clase que   
                                    # se deberia contar pero ellos no lo cuentan en sus soluciones, asi que 
                                    # nosotros tampoco
    def __str__(self):
        return f"Nodo(estado={self.estado}, padre={self.padre}, accion={self.accion}, coste={self.coste}, profundidad={self.profundidad})"
    def __repr__(self):
        return f"{self.estado.identifier}"
    def __eq__(self,otro):
        if not isinstance(otro, Nodo):
            return False
        return self.estado.__eq__(otro.estado) and self.nGenerado.__eq__(otro.nGenerado)
    def __lt__(self,otro):
        return self.estado.__lt__(otro.estado)