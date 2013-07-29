#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Funciones y variables comunes para los videojuegos."""

import os
import pygame as p
 
def cargar_imagen(nombre, alpha= False, dirs= "imagenes"):
    "Cargar imágenes del juego."
    ruta = os.path.join(dirs, nombre)
    try:
        imagen = p.image.load(ruta)
    except:
        print("No se puede cargar la imagen: ", ruta)
        raise
        
    if alpha == True:
        imagen = imagen.convert_alpha()
    else:
        imagen = imagen.convert()
    return imagen
