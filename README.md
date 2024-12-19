# Sistemas-Inteligentes-P2
Parte 2 de la practidca de Sistemas Inteligentes

NUEVA FORMULA EVALUACION:
value(s) = (1/sum(c[i].pop)) * sum(c[i].pop * min(time(c[i],s[j]))

    Cosas para la memoria

En inicializar cambiar la parte de coger los individuos al azar por una linea con random.sample (0,len,nSoluciones)

En genético cambiar el for de debajo de seleccion generacion, para añadirlo a el

Cambiar el orden de la lista en lugar de por destination a ordenarlo por coste

Paquete intertools para hacer la cache interna

Ordenar la lista de accione por coste mas bajo para que la cahe funcione