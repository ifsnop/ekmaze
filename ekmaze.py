#/usr/bin/env python
# -*- coding: utf-8 -*-

"Script para ejecutar el juego."

from pyjuego.g_escenas import Director
from escenas import EscenaInicio, EscenaTeclado

def main():
    "Ejecutar el juego."
    director = Director("EKMAZE", (544, 544))
    director.ejecutar(EscenaInicio())

if __name__ == "__main__":
    main()
