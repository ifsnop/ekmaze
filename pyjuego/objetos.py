#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo que contiene objetos para ser desplegados en la interfaz gráfica.
"""

import pygame as p

class Texto():
    "Crea un texto para mostrar en pantalla."
    def __init__(
        self, predeterminado = "", tamano = 24, fuente = None, color = (0, 0, 0)
    ):
        "Inicializa el texto."
        self.fuente = p.font.Font(fuente, tamano)
        self.default = predeterminado
        self.texto = None
        self.rect = None
        self.color = color
        self.mostrar()
        
    def mostrar(self, cadena = ""):
        "Regresa el texto a mostrar."
        self.texto = self.fuente.render(self.default + cadena, True, self.color)
        self.rect = self.texto.get_rect()
        return self.texto

class TecladoPantalla():
    "Clase para crear un teclado completo en pantalla."
    def __init__(self, longitud=8, teclado=None):
        """
        Inicialización de las propiedades y banderas necesarias:
        -- self.teclado:    Mapa de caracteres a desplegar.
        -- self.opcs:       Comandos que pueden ser ejecutados.
        -- self.len:        Longitud permisible de la cadena.
        -- self.cadena:     Variable para almacenar el texto capturado.
        -- self.sel:        Indicador de la posición del cursor en letras.
        -- self.opc:        Indicador de la posición del cursor en opciones.
        -- self.controles:  Bandera para saber si estamos en texto o controles.
        -- self.completado: Bandera para indicar si se completa el registro.
        """
        if teclado is None:
            self.teclado = [
                'ABCDEFGHIJKLM',
                'NOPQRSTUVWXYZ',
                'abcdefghijklm',
                'nopqrstuvwxyz',
                '0123456789 -.'
            ]
        else:
            self.teclado = teclado
        self.opcs = ['CLEAR', 'DEL', 'OK']  #Opciones de control.
        self.len = longitud     #Longitud de palabra.
        self.cadena = ""        #Cadena para guardar el texto.
        self.sel = [0, 0]       #Carácter seleccionado inicialmente.
        self.opc = 0            #Opción seleccionada inicialmente.
        self.controles = False  #Bandera para saber si estamos en los controles.
        self.completado = False #Bandera para saber si terminó.
        
    def dir_derecha(self):
        "Acciones a ser tomadas al presionar la tecla flecha derecha."
        if self.controles:
            self.opc += 1
            if self.opc >= len(self.opcs):
                self.opc = 0
        else:
            self.sel[1] += 1
            if self.sel[1] >= len(self.teclado[0]):
                self.sel[1] = 0
                
    def dir_izquierda(self):
        "Acciones a ser tomadas al presionar la tecla flecha izquierda."
        if self.controles:
            self.opc -= 1
            if self.opc < 0:
                self.opc = len(self.opcs) - 1
        else:
            self.sel[1] -= 1
            if self.sel[1] < 0:
                self.sel[1] = len(self.teclado[0]) - 1
                
    def enter_presionado(self):
        "Acciones que se realizan al presionar <Enter>."
        if self.controles == False:
            fila, col = self.sel[0], self.sel[1]
            if len(self.cadena) < self.len:
                self.cadena += self.teclado[fila][col]
            else:
                self.cadena = self.cadena[:-1]
                self.cadena += self.teclado[fila][col]
        else:
            if self.opc == 0:
                self.cadena = ""
            elif self.opc == 1:
                self.cadena = self.cadena[:-1]
            elif self.opc == 2:
                self.completado = True
            
    def leer_eventos(self, eventos):
        """Lectura de los eventos para determinar el uso del teclado."""
        for evento in eventos:
            if evento.type == p.KEYDOWN:
                if evento.key == p.K_RIGHT:
                    self.dir_derecha()
                elif evento.key == p.K_LEFT:
                    self.dir_izquierda()
                elif evento.key == p.K_UP:
                    self.sel[0] -= 1
                    if self.sel[0] < 0:
                        self.sel[0] = len(self.teclado)
                        self.controles = True
                    else:
                        self.controles = False
                elif evento.key == p.K_DOWN:
                    self.sel[0] += 1
                    if self.sel[0] >= len(self.teclado):
                        self.controles = True
                        self.sel[0] = -1
                    else:
                        self.controles = False
                elif evento.key == p.K_RETURN or evento.key == p.K_KP_ENTER:
                    self.enter_presionado()


    def dibujar_teclado(self, pantalla, tamano=14, fuente=None, 
        color=(0xFF,0xFF,0x00), color2=(0xFF,0xFF,0xFF), pos_y=64, inc_y=16):
        """
        Dibuja el teclado en pantalla. Los argumentos que recibe son:
        -- pantalla: Superficie sobre la cual dibujar.
        -- tamano:   Tamaño de letra de los caracteres.
        -- fuente:   Fuente con la que se dibujaran los caracteres.
        -- color:    Color del texto seleccionado.
        -- color2:   Color del texto no seleccionado.
        -- pos_y:    Posición vertical inicial de los caracteres.
        -- inc_y:    Espaciado vertical entre caracteres.
        """
        #Dibujando los caracteres del teclado.
        for fila in range(len(self.teclado)):
            for col in range(len(self.teclado[0])):
                caracter = self.teclado[fila][col]
                if [fila, col] == self.sel:
                    texto = Texto(caracter, tamano, fuente, color)
                else:
                    texto = Texto(caracter, tamano, fuente, color2)
                pos_x = pantalla.get_size()[0] / (len(self.teclado[fila]) + 1)
                pos_x = pos_x * (col+1) - texto.rect.centerx
                pantalla.blit(texto.mostrar(), (pos_x, pos_y))
            pos_y += inc_y
            
    def dibujar_display(self, pantalla, tamano=14, fuente=None, 
        color=(0xFF,0xFF,0xFF), pos_x=None, pos_y=None):
        """
        Dibujar el display de las letras en la pantalla.
        -- pantalla: Superficie sobre la cual dibujar.
        -- tamano:   Tamaño de letra de los caracteres.
        -- fuente:   Fuente con la que se dibujaran los caracteres.
        -- color:    Color del texto seleccionado.
        -- pos_x:    Coordenada en X donde inicia el display.
        -- pos_y:    Coordenada en Y donde inicia el display.
        """
        cadena = ""
        for caracter in self.cadena:
            cadena += caracter + " "
        while len(cadena) < self.len * 2:
            cadena += "_ "
        texto = Texto(cadena, tamano, fuente, color)
        if pos_x is None:
            pos_x = pantalla.get_size()[0] / 2 - texto.rect.centerx
        if pos_y is None:
            pos_y = 0
        pantalla.blit(texto.mostrar(), (pos_x, pos_y))
        
    def dibujar_comandos(self, pantalla, tamano=14, fuente=None, 
        color=(0xFF,0xFF,0x00), color2=(0xFF,0xFF,0xFF), pos_y=None):
        """
        Dibujar el área de comandos en pantalla.
        -- pantalla: Superficie sobre la cual dibujar.
        -- tamano:   Tamaño de letra de los caracteres.
        -- fuente:   Fuente con la que se dibujaran los caracteres.
        -- color:    Color del texto seleccionado.
        -- color2:   Color del texto no seleccionado.
        -- pos_y:    Coordenada en Y donde se dibujan las opciones.
        """
        for cmd in range(len(self.opcs)):
            if self.controles and self.opc == cmd:
                texto = Texto(self.opcs[cmd], tamano, fuente, color)
            else:
                texto = Texto(self.opcs[cmd], tamano, fuente, color2)
            pos_x = pantalla.get_size()[0] / (len(self.opcs) + 1) * (cmd+1)
            if pos_y is None:
                pos_y = pantalla.get_size()[1] / 10 * 9
            pantalla.blit(texto.mostrar(), (pos_x, pos_y))
