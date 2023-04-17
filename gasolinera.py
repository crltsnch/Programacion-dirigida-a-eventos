#Llegan coches en un intervalo aleatorio de hasta T minutos.
#La gasolinera tiene N surtidores
#Cuando un coche se pone en el surtidor, el conductor se baja, elije el combustible de su elección y llena el depósito. Tiempo 5-10 minutos
#Tras llenarlo va a la oficia y se pone en la cola. La caja es única. 3 minutos
#Tras pagar retira el coche dejando libre el surtidor.

import random
import simpy
import time

#Variables globales
T = 15 #Tiempo de llegada de los coches
N = 1 #Número de surtidores
tiempo = 0 #Tiempo de simulación

class Cola:
    coche = 0
    def __init__(self, env, surtidores, caja):
        self.env = env
        self.surtidores = simpy.resource(env, surtidores)
        self.caja = caja

    def llenar(self, coche):
        yield self.env.timeout(random.randint(5,10))
        print("El coche %s ha terminado de llenar el depósito" % coche)

    def pagar(self, coche):
        yield self.env.timeout(3)
        print("El coche %s ha terminado de pagar" % coche)

    def retirar(self, coche):
        yield self.env.timeout(2)
        print("El coche %s ha retirado el coche" % coche)