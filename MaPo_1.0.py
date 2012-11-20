#! /usr/bin/env python

import pilas
import sys
sys.path.insert(0, "..")
from pilas.escenas import *
import random
from pilas.actores import Aceituna

#Ponemos al enemigo (aceituna)
class AceitunaVigilante(Aceituna):
    
    def __init__(self, x=0, y=15):
        Aceituna.__init__(self, x, y)
#Esto hace que la aceituna se mueva de izquierda a derecha indefinidamente
    def actualizar(self):
         
        self.x += 2
        if self.x > 120:
            self.x = [-90],1.2

#esta es la escena que en la parte del menu principal muestra los agradecimientos
class Agradecimientos(Escena):
    def __init__(self):
        Escena.__init__(self)
        self.text = self.texto()
#Fondo del menu
        pilas.fondos.Espacio()
#Definimos la unica opcion que hay en el "MENU" de agradecimientos       
        salida = [('Salir', self.salida)]    
        
        self.menu = pilas.actores.Menu(salida)
        self.menu.y = -200
     
    def salida(self):
        Menu()
#Estos son los agradecimientos propiamente dichos que leemos cuando ingresamos a los agradecimientos en el juego
    def texto(self):
        texto = pilas.actores.Texto("Nuestros mas sinceros agradecimientos a:", x = 0, y = 40)
        texto2 = pilas.actores.Texto("Luciano Castillo x 2", x = 0, y = 0)
        texto3 = pilas.actores.Texto("Agustin Venturi", x = 0, y = -40)
        texto3.escala = 0.5
   
#La clase del juego en si
class Juego(Escena):

    def __init__(self):
        Escena.__init__(self)
        self.cancer = 0
        self.mapa = self.crear_mapa()
        self.pato = self.pato()
        self.martian = self.marcianito(self.mapa)
        self.aceituna = self.aceituna()
        self.txt = self.texto()
        self.sonido_monedita = self.sonido()        
        pilas.mundo.colisiones.agregar(self.martian, self.pato, self.chorear)
        pilas.mundo.colisiones.agregar(self.martian, self.aceituna, self.muerte)
#Aca creamos el fondo, con el mapa, las plataformas, el suelo.
    def crear_mapa(self):
        grilla = pilas.imagenes.cargar_grilla('plataformas.png',10,10)
        mapa = pilas.actores.Mapa(grilla)


    #pintando la plataforma grande   
        mapa.pintar_bloque(10, 7, 13)
        mapa.pintar_bloque(10, 8, 14)
        mapa.pintar_bloque(10, 9, 14)
        mapa.pintar_bloque(10, 10, 14)
        mapa.pintar_bloque(10, 11, 14)
        mapa.pintar_bloque(10, 12, 14)
        mapa.pintar_bloque(10, 13, 29)

    #pintando las piedras abajo de la plataforma grande (para que quede mejor)
        mapa.pintar_bloque(11, 7, 23, False)
        mapa.pintar_bloque(11, 8, 24, False)
        mapa.pintar_bloque(11, 9, 24, False)
        mapa.pintar_bloque(11, 10, 24, False)
        mapa.pintar_bloque(11, 11, 24, False)
        mapa.pintar_bloque(11, 12, 24, False)
        mapa.pintar_bloque(11, 13, 31, False)      

        mapa.pintar_bloque(13, 4, 13)
        mapa.pintar_bloque(13, 5, 14)
        mapa.pintar_bloque(13, 6, 14)
        mapa.pintar_bloque(13, 7, 29)

        mapa.pintar_bloque(14, 4, 23, False)
        mapa.pintar_bloque(14, 5, 24, False)
        mapa.pintar_bloque(14, 6, 24, False)
        mapa.pintar_bloque(14, 7, 31, False)

    #pintando el suelo de el escenario (Nieve)   
        for i in range(0, 20):
            mapa.pintar_bloque(16, i, 14)
            mapa.pintar_bloque(17, i, 24)

        #ponemos la imagen de fondo
        fondo = pilas.fondos.Fondo('frio2.jpg')
        fondo.escala = [1.5] 
        return mapa

        #Ponemos a nuestro personaje principal        
    def marcianito(self, mapa):
        martian = pilas.actores.Martian(mapa)
        martian.x = 200
        martian.y = -192
        martian.radio_de_colision=20
        martian.aprender(pilas.habilidades.SeMantieneEnPantalla)
        return martian

#Estas son las tres monedas que giran en las tres posiciones indicadas en el mapa       
    def pato(self):
        pato=[pilas.actores.Moneda(), pilas.actores.Moneda(), pilas.actores.Moneda()]
        pato[0].x = -130
        pato[0].y = -90
        pato[1].x = 0
        pato[1].y = 10
        pato[2].x = -190
        pato[2].y = 100
        return pato
#Aqui llamamos a la funcion del enemigo y la ponemos en el mapa
    def aceituna (self):
        aceituna = AceitunaVigilante()
        return aceituna
#Esto es el puntaje que aumenta cada vez que agarramos una moneda
    def texto (self):
        texto = ''
        texto = pilas.actores.Puntaje(x=-240, y=200)
        return texto
#El sonido que hacen las monedas cuando las agarramos
    def sonido (self):
        sonido_monedita = pilas.sonidos.cargar('Sound_65.wav')
        return sonido_monedita
#Esta es la colicion que permite que el marciano pueda "chorear" las monedas
    def chorear(self, marcianito, pato):
        pato.eliminar()
        self.txt.aumentar()
        self.sonido_monedita.reproducir()
        self.cancer += 1
        Html = open("Ganadores.html", "w")
        Html.write("-----Nombre-----Puntaje:_-_-_-([" + str(self.cancer) + "])-_-_-_")
        Html.close()
        if self.cancer == 3:
            def comenzar():
                jueguito = Juego()
            def salir():
                Menu()
            
            opciones = [
                        ("Volver a jugar =D!!!", comenzar),
                        ("Volver al menu", salir)
                        ]
            pilas.avisar('No sos pobre')
            self.menu = pilas.actores.Menu(opciones)

#Aca ponemos la colision entre el marciano y la aceituna, hace que el marciano al tocar la aceituna desaparezca
    def muerte(self, marcianito, aceituna):
        marcianito.eliminar()
        aceituna.eliminar()
        Tecabe = pilas.actores.Texto("Te moriste =(", x = 0, y = 100)

#con esto iniciamos la clase con el mapa los enemigos y el personaje de nuevo despues de perder
        def comenzar():
            jueguito = Juego()
#con esto salimos del juego despues de perder(no se recomienda, el juego es demasiado divertido como para dejar de jugarlo)
        def salir():
            import sys
            sys.exit(0)
      
        opciones = [
                    ('Volver a jugar =D!!!', comenzar),
                    ('Salir =(', salir)
                    ]
        self.menu = pilas.actores.Menu(opciones)        
#Este es el menu principal, con las tres opciones de comenzar, salir y de ver los Agradecimientos
class Menu(Normal):
    def __init__(self):
        Normal.__init__(self)

        pilas.fondos.Espacio()

        opciones = [
                    ('Comenzar a jugar', self.comenzar),
                    ('Agradecimientos', self.agradecimientos),
                    ('Salir', self.salir)
                    ]

        self.menu = pilas.actores.Menu(opciones)

    def agradecimientos(self):
        Agradecimientos()

    def comenzar(self):
        jueguito = Juego()


    def salir(self):
        import sys
        sys.exit(0)


pilas.iniciar()
Menu()
pilas.ejecutar()

