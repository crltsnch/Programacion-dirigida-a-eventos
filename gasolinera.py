#Llegan coches en un intervalo aleatorio de hasta T minutos.
#La gasolinera tiene N surtidores
#Cuando un coche se pone en el surtidor, el conductor se baja, elije el combustible de su elección y llena el depósito. Tiempo 5-10 minutos
#Tras llenarlo va a la oficia y se pone en la cola. La caja es única. 3 minutos
#Tras pagar retira el coche dejando libre el surtidor.

'''Modelar el problema con los objetos apropiados indicando los estados en que puede estar cada elemento.
Modelar los coches como Threads que genere el programa principal. A efectos del ejercicio se generan 50 coches.
Para un T de 15 minutos y N un surtidor.
Calcular el tiempo medio que tarda un coche desde que llega a la gasolinera hasta que se va.'''

import random
import simpy


#Variables globales
T = 15 #Tiempo de llegada de los coches
N = 1 #Número de surtidores


class Cola:
    def __init__(self, env, surtidores, caja):
        self.env = env
        self.surtidores = simpy.resource(env, surtidores)
        self.caja = caja
        self.tiempo = simpy.Resource(env, 1)

        
    def coche(self, coche):
        print("El coche %s ha llegado a la gasolinera" % coche)
        with self.surtidores.request() as surtidor:
            yield surtidor
            print("El coche %s ha llegado al surtidor" % coche)
            yield self.env.process(self.llenar(coche))
            yield self.env.process(self.pagar(coche))
            yield self.env.process(self.retirar(coche))

    def llenar(self, coche):
        yield self.env.timeout(random.randint(5,10))
        print("El coche %s ha terminado de llenar el depósito" % coche)

    def pagar(self, coche):
        yield self.env.timeout(3)
        print("El coche %s ha terminado de pagar" % coche)

    def retirar(self, coche):
        yield self.env.timeout(2)
        print("El coche %s ha retirado el coche" % coche)
    
    def coche_llega(self, coche):
        yield self.env.timeout(random.randint(1,T))
        self.tiempo.process(self.coche(coche))
    
    def run(self):
        for i in range(50):
            self.env.process(self.coche_llega(i))
    

def main():
    env = simpy.Environment()
    cola = Cola(env, 1, 1)
    env.process(cola.run())
