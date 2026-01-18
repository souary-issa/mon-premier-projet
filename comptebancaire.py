from tkinter import *


def cercle(can, x, y, r, couleur):
    """dessin d'un cercle de rayon <r> en <x, y> dans le canvas <can>"""
    can.create_oval(x-r, y-r, x+r, y+r, fill=couleur)


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)                                    # constructeur de la classe parente
        self.can = Canvas(self, width=475, height=175, bg='white')
        self.can.pack(side=TOP, padx=5, pady=5)
        Button(self, text='train', command=self.dessine).pack(side=LEFT)
        Button(self, text='hello', command=self.coucou).pack(side=LEFT)
        Button(self, text='allumer', command=self.allumage).pack(side=RIGHT)

    def dessine(self):
        """instaciation des wagons dans le canvas"""
        self.w1 = Wagon(self.can, 10, 30, 'yellow')
        self.w2 = Wagon(self.can, 130, 30, 'red')
        self.w3 = Wagon(self.can, 250, 30)
        self.w4 = Wagon(self.can, 370, 30, 'maroon')

    def coucou(self):
        """apparition de personnage dans certaines fenetres"""
        self.w1.perso(1)
        self.w1.perso(2)
        self.w1.perso(3)
        self.w4.perso(1)

    def allumage(self):
        self.w1.allumer()
        self.w4.allumer()


class Wagon(object):
    def __init__(self, can, x, y, coul='yellow'):
        self.can, self.x, self.y = can, x, y
        # rectangle de base : 95 x 60 pixels
        can.create_rectangle(x, y, x+95, y+60, fill=coul)
        # 3 fenetres de 25 x 40 pixels, ecartees de 5 pixels :
        self.fen = []
        for xf in range(x+5, x+90, 30):
            self.fen.append(can.create_rectangle(xf, y+5, xf+25, y+40, fill='black'))
        # 2 roue de rayon  egal a 12 pixels :
        cercle(can, x+18, y+73, 12, couleur='grey')
        cercle(can, x+77, y+73, 12, couleur='grey')

    def perso(self, can):
        """apperition d'un petit personnage a la fentre <fen>"""
        # calcul de coordonnees de centre de chaque fenetres :
        xf = self.x + can * 30 - 12
        yf = self.y + 25
        cercle(self.can, xf, yf, 10, couleur='pink')       # visage
        cercle(self.can, xf-5, yf-3, 2, couleur='black')    # oeil gauche
        cercle(self.can, xf+5, yf-3, 2, couleur='black')    # oeil droite
        cercle(self.can, xf, yf+5, 3, couleur='black')      # bouche

    def allumer(self):
        for f in self.fen:
            self.can.itemconfigure(f, fill='white')


app = Application()
app.mainloop()



