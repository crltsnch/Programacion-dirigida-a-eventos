#Llegan coches en un intervalo aleatorio de hasta T minutos.
#La gasolinera tiene N surtidores
#Cuando un coche se pone en el surtidor, el conductor se baja, elije el combustible de su elección y llena el depósito. Tiempo 5-10 minutos
#Tras llenarlo va a la oficia y se pone en la cola. La caja es única. 3 minutos
#Tras pagar retira el coche dejando libre el surtidor.

'''Modelar el problema con los objetos apropiados indicando los estados en que puede estar cada elemento.
Modelar los coches como Threads que genere el programa principal. A efectos del ejercicio se generan 50 coches.
Para un T de 15 minutos y N un surtidor.
Calcular el tiempo medio que tarda un coche desde que llega a la gasolinera hasta que se va.'''

import threading
import time
import random

N = 1  # número de surtidores
T = 15 * 60  # intervalo de tiempo en segundos
NUM_CARS = 50  # número total de coches

class Gasolinera:
    def __init__(self):
        self.surtidores = [threading.Lock() for _ in range(N)]
        self.cola_caja = threading.Condition()
        self.tiempo_total = 0
        self.num_coches = 0
    
    def acceder_surtidor(self):
        surtidor_libre = None
        while surtidor_libre is None:
            for surtidor in self.surtidores:
                if surtidor.acquire(blocking=False):
                    surtidor_libre = surtidor
                    break
            else:
                time.sleep(0.1)
        return surtidor_libre
    
    def salir_surtidor(self, surtidor):
        surtidor.release()
    
    def esperar_caja(self):
        with self.cola_caja:
            self.cola_caja.wait()
    
    def salir_caja(self):
        with self.cola_caja:
            self.cola_caja.notify()
    
    def sumar_tiempo(self, tiempo):
        self.tiempo_total += tiempo
        self.num_coches += 1
    
    def tiempo_medio(self):
        return self.tiempo_total / self.num_coches * 100

def coche_gasolinera(gasolinera):
    llegada = time.time()
    print(f"Coche llega a la gasolinera a las {llegada:.2f}")
    gasolinera.sumar_tiempo(0)
    
    surtidor = gasolinera.acceder_surtidor()
    inicio_surtidor = time.time()
    print(f"Coche accede al surtidor a las {inicio_surtidor:.2f}")
    gasolinera.sumar_tiempo(inicio_surtidor - llegada)
    
    tiempo_combustible = random.uniform(5, 10)
    time.sleep(tiempo_combustible)
    fin_surtidor = time.time()
    print(f"Coche llena el depósito a las {fin_surtidor:.2f}")
    gasolinera.salir_surtidor(surtidor)
    
    gasolinera.esperar_caja()
    inicio_caja = time.time()
    print(f"Coche accede a la caja a las {inicio_caja:.2f}")
    gasolinera.sumar_tiempo(inicio_caja - llegada)
    
    time.sleep(3)
    fin_caja = time.time()
    print(f"Coche paga a las {fin_caja:.2f}")
    gasolinera.salir_caja()
    
    salida = time.time()
    print(f"Coche sale de la gasolinera a las {salida:.2f}")
    gasolinera.sumar_tiempo(salida - llegada)
    

if __name__ == "__main__":
    gasolinera = Gasolinera()
    
    threads = []
    for i in range(NUM_CARS):
        llegada = random.uniform(0, T)
        t = threading.Timer(llegada, coche_gasolinera, args=[gasolinera])
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    tiempo_medio = gasolinera.tiempo_medio()
    print(f"El tiempo medio que tarda un coche en la gasolinera {tiempo_medio:.2f} segundos")

