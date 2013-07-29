#/usr/bin/env python
# -*- coding: utf-8 -*-

"Adaptación de Pykitten para su uso con PGU."

from pgu.tilevid import Sprite


class Interval:
    """
    Temporizador generado con un contador, utilizado para generar un pequeno
    intervalo de actualizacion.
    """
    def __init__(self, interval):
        """Define el periodo de actualizacion."""
        self.counter = 0
        self.interval = interval

    def update(self, num = 1):
        """
        Actualizar se encarga de incrementar el contador y regresar True
        en caso de que el tiempo establecido se haya cumplido; False en caso
        contrario. 
        """
        self.counter += num
        if self.counter >= self.interval:  #pling!
            self.counter = 0
            return True
        return False
        
class PykittenSprite(Sprite):
    """Clase base del sprite, con funciones agregadas."""
    def __init__(self, ishape, pos):
        """Contructor de Pykitten + PGU."""
        Sprite.__init__(self, ishape, pos)
        #Determina si el sprite se esta moviendo.
        self.moving = False
        #Determina la velocidad a la que se mueve el sprite.
        self.vel = (0, 0)
        #Similar a vel, pero utilizado para generar movimiento en una sola dir.
        self.speed = 1

    def set_vel(self, vel):
        """Velocidad en (x, y)."""
        self.vel = vel
        if self.vel[0] or self.vel[1]:
            self.moving = True
        else:
            self.moving = False

    def add_vel(self, vel):
        """Agrega velocidad a la velocidad actual."""
        v_x, v_y = vel
        self.vel = (self.vel[0] + v_x, self.vel[1] + v_y)

    def update(self):
        """Actualiza la posicion del sprite en base a su velocidad."""
        if self.moving:
            self.rect.x += self.vel[0]
            self.rect.y += self.vel[1]
        #print self.vel

class AnimatedSprite(PykittenSprite):
    """Clase para crear un sprite animado."""
    def __init__(self, images, pos, engine, delay = 5):
        """Constructor de AnimatedSprite
        @param images: Lista de imagenes que conforman la animacion.
        @param pos:    Posicion del Sprite.
        @param engine: Motor de PGU.
        @param delay:  Tiempo entre el cambio de imagen.
        """
        self.images = images
        self.engine = engine
        self.cur_image = 0
        self.anim_timer = Interval(delay)
        self.animate = False
        PykittenSprite.__init__(self, engine.images[self.images[0]], pos)

    def set_images(self, images):
        """Cambia las imagenes del sprite animado.
        @param images: Lista de imagenes.
        """
        self.images = images
        self.cur_image = 0
        self.setimage(self.engine.images[self.images[0]])

    def update(self):
        """Actualiza el sprite animado.
        Se encarga de mover el sprite (PykittenSprite), ademas de animarlo.
        """
        PykittenSprite.update(self)
        if self.animate and self.anim_timer.update():
            self.cur_image += 1
            if self.cur_image >= len(self.images):
                self.cur_image = 0
            self.setimage(self.engine.images[self.images[self.cur_image]])

    def play(self):
        """Muestra la animacion."""
        self.animate = True

    def stop(self):
        """Detiene la animacion. Muestra la primer imagen."""
        self.animate = False
        self.cur_image = 0
        self.anim_timer.counter = 0
        self.setimage(self.engine.images[self.images[self.cur_image]])

    def pause(self):
        """Pausa la animacion. Se mantiene la ultima imagen."""
        self.animate = False
        
        
class CharacterSprite(AnimatedSprite):
    """Sprite de Personaje.
    Se encarga de mostrar animaciones del personaje en cuatro direcciones.
    """
    def __init__(self, imglists, pos, engine, delay = 5):
        """Contructor del personaje.
        @param imglists: Lista de listas de imagenes.
        """
        AnimatedSprite.__init__(self, imglists[0], pos, engine, delay)
        self.imglists = imglists
        self.cur_list = 0
        self.movedir = None
        self.cur_dir = 0
        self.crashed = False
        #Tiles en los que se encuentra el personaje.
        self.motor = engine
        self.tile = None    #Tile actual.
        self._tile = None   #Tile anterior.

    def set_movedir(self, direction):
        """Establece la direccion en la que se mueve el personaje.
        @param dir:
            - 0 = abajo
            - 1 = arriba
            - 2 = izquierda
            - 3 = derecha
        """
        self.movedir = direction
        self.play()

    def turn(self, direction):
        """Voltea el personaje a la direccion especificada.
        @param dir:
            - 0 = abajo
            - 1 = arriba
            - 2 = izquierda
            - 3 = derecha
        """
        self.set_images(self.imglists[direction])
        self.cur_dir = direction

    def update(self):
        """Actualiza el personaje.
        Mueve, anima, y gira al personaje.
        En caso de proveer un motor de tiles, calcula la posición actual.
        """
        if self.movedir is not None:
            #Calcular la posición del nuevo tile.
            self._tile = self.tile
            self.tile = self.motor.screen_to_tile(self.compensate())
            #Movimiento.
            direction = self.movedir
            if not self.moving or direction != self.cur_dir:
                self.cur_dir = direction
                self.set_images(self.imglists[direction]) #turn chara
                #set new vel
                if direction == 0:  #down
                    self.set_vel((0, self.speed))
                elif direction == 1:  #up
                    self.set_vel((0, -self.speed))
                elif direction == 2:  #left
                    self.set_vel((-self.speed, 0))
                else:  #right
                    self.set_vel((self.speed, 0))
        elif not self.movedir and self.vel != (0, 0):
            self.stop_moving()
        AnimatedSprite.update(self)

    def stop_moving(self):
        """Detiene al personaje y a la animacion."""
        self.set_vel((0, 0))
        self.movedir = None
        self.stop()
        
    def compensate(self, offset = 2):
        """Se encarga de compensar las medidas del sprite en base a la dirección
        actual, con el fin de realizar los cambios de tile justo al centro.
        """
        if self.movedir == 0:   #sur
            return (self.rect.left, self.rect.top - offset)
        elif self.movedir == 1: #norte
            return (self.rect.right, self.rect.bottom + offset)
        elif self.movedir == 2: #oeste
            return (self.rect.right + offset, self.rect.bottom)
        elif self.movedir == 3: #este
            return (self.rect.left - offset, self.rect.top)
            
    def tile_changed(self):
        "Determina si el sprite se movió a un nuevo tile."
        return not self.tile == self._tile
            
    def reverse(self):
        "Invierte la dirección actual del sprite."
        self.movedir += [+1, -1][self.movedir % 2]

    def left(self):
        "Mueve en sprite hacia la izquierda en relación a la dirección actual."
        self.movedir += [3, 1, -2, -2][self.movedir]

    def right(self):
        "Mueve en sprite hacia la derecha en relación a la dirección actual."
        self.movedir += [+2, +2, -1, -3][self.movedir]
        
    def is_free(self, tile_pos, libre=None):
        "Determina si un tile está disponible para transitar por él."
        if libre is None:
            libre = [0]
        if self.motor.get(tile_pos) in libre:
            return True
        else:
            return False
        
    def left_is_free(self, libre=None):
        "Determina si el tile a la izquierda de la posición actual está libre."
        if libre is None:
            libre = [0]
        offset = ([1, -1, 0, 0][self.movedir], [0, 0, 1, -1][self.movedir])
        tile_pos = (self.tile[0] + offset[0], self.tile[1] + offset[1])
        return self.is_free(tile_pos, libre)
            
    def right_is_free(self, libre=None):
        "Determina si el tile a la derecha de la posición actual está libre."
        if libre is None:
            libre = [0]
        offset = ([-1, 1, 0, 0][self.movedir], [0, 0, -1, 1][self.movedir])
        tile_pos = (self.tile[0] + offset[0], self.tile[1] + offset[1])
        return self.is_free(tile_pos, libre)
        
    def front_is_free(self, libre=None):
        "Determina si el tile a la derecha de la posición actual está libre."
        if libre is None:
            libre = [0]
        offset = ([0, 0, -1, 1][self.movedir], [1, -1, 0, 0][self.movedir])
        tile_pos = (self.tile[0] + offset[0], self.tile[1] + offset[1])
        return self.is_free(tile_pos, libre)
        
    def next_are_free(self, libre=None):
        "Determina cuáles de las tres direcciones están disponibles."
        if libre is None:
            libre = [0]
        free = []
        if self.right_is_free(libre):
            free.append(self.movedir + [+2, +2, -1, -3][self.movedir])
        if self.left_is_free(libre):
            free.append(self.movedir + [3, 1, -2, -2][self.movedir])
        if self.front_is_free(libre):
            free.append(self.movedir)
        return free
