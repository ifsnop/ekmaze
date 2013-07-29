#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para gestión de escenas en Pygame. Está conformado por las clases Escena 
y Director.
"""

import pygame as p

class Director():
    """Es el objeto principal del videojuego y se encarga de gestionar escenas y
    ejecutar el juego."""
    def __init__(self, titulo="", res=(640, 480)):
        "Inicializar Pygame, la pantalla, y el reloj."
        p.init()
        self.pantalla = p.display.set_mode(res)
        p.display.set_caption(titulo)
        self.escena = None
        self.reloj = p.time.Clock()
        self.res = res
        
    def ejecutar(self, escena_inicial, fps = 60):
        "Ejecuta el ciclo principal del videojuego."
        self.escena = escena_inicial
        jugando = True      #Bandera para indicar la salida.
        while jugando:
            self.reloj.tick(fps)
            #Leyendo los eventos para marcar la salida.
            eventos = p.event.get()
            for evento in eventos:
                if evento.type == p.QUIT:
                    jugando = False
                elif evento.type == p.KEYDOWN:
                    if evento.key == p.K_ESCAPE:
                        jugando = False
            #Interacción con la escena.
            self.escena.leer_eventos(eventos)
            self.escena.actualizar()
            self.escena.dibujar(self.pantalla)
            #Cambio de escena, en caso de que haya alguno.
            self.escena = self.escena.escena
            #Comando necesario para reflejar cambios en la pantalla.
            p.display.flip()


class Escena:
    "Esqueleto para cada una de las escenas del videojuego."
    def __init__(self):
        self.escena = self
    
    def leer_eventos(self, eventos):
        "Lee los eventos para interactuar con los objetos."
        pass
    
    def actualizar(self):
        "Actualiza los objetos en la pantalla."
        pass
    
    def dibujar(self, pantalla):
        "Dibuja los objetos en la pantalla."
        pass
        
    def cambiar_escena(self, escena):
        "Cambia la escena del juego."
        self.escena = escena
