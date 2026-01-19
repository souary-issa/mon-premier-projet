# _*_ coding: utf-8 _*_
from math import *
from curseurs import *


class Graphique(Canvas):
    """fentre dessin graphique"""
    def __init__(self, largeur=500, hauteur=500):
        Canvas.__init__(self, width=largeur, height=hauteur, bg="white")
        self.largeur, self.haut = largeur, hauteur
        self.create_line(10, self.haut/2, self.largeur-10, self.haut/2, fill="black", arrow=LAST)
        self.create_line(self.largeur/2, 10, self.largeur/2, 500, fill="black", arrow=LAST)
        # creation des panneaux de control :
        self.graduation_x()
        self.graduation_y()
        self.pack()

    def graduation_x(self):
        """tracer des graduation en X"""
        espacex = (self.largeur-30)/(2*10)
        # graduation en zone negative :
        for i in range(10, 0, -1):
            stx = self.largeur/2 - i * espacex
            valeur = -i
            self.create_line(stx, self.haut/2+5, stx, self.haut/2-5,  fill='black', width=2)
            self.create_text(stx, self.haut/2+15, text=str(valeur), fill="black")
        # graduation en zone positive :
        for i in range(1, 11, 1):
            stx = self.largeur/2 + i * espacex
            valeur = i
            self.create_line(stx, self.haut/2+5, stx, self.haut/2-5, fill="black", width=2)
            self.create_text(stx, self.haut/2+15, text=str(valeur))
        # graduation  centrale  en 0 :
        self.create_line(self.largeur/2 - 5, self.haut/2, self.largeur/2 + 5, self.haut/2)
        self.create_text(self.largeur/2 - 10, self.haut/2, text="0", fill="red")

    def graduation_y(self):
        """tracer des graduation Y """
        espacey = (self.haut - 30) / (2*10)
        # graduation e zone negative :
        for i in range(10, 0, -1):
            sty = self.haut/2 + i * espacey
            valeur = -i
            self.create_line(self.largeur/2-5, sty, self.largeur/2+5, sty, fill="black", width=2)
            self.create_text(self.largeur/2 - 15, sty, text=str(valeur))
        # graduation en zone positive :
        for i in range(1, 10+1):
            sty = self.haut/2 - i * espacey
            valeur = i
            self.create_line(self.largeur/2+5, sty, self.largeur/2-5, sty, fill="black", width=2)
            self.create_text(self.largeur/2-15, sty, text=(valeur))

    def tracecourbe(self, ampl=2, freq=2, phase=0, coul="", bien=0):
        """tracer de la courbe d'elogation/temp sur 1 seconde"""
        curve = []
        pas = (self.largeur - 25)/1000
        for t in range(0, 1001, 5):
            e = ampl * sin(2*pi * freq * t / 1000 - phase)
            x = 10 + t * pas
            y = self.haut / 2 - e * self.haut/25
            curve.append(x)
            curve.append(y)
        return self.create_line(curve, fill=coul, smooth=True)


if __name__ == "__main__":
    root = Tk()
    root.title("Vibration harmonique")
    gra = Graphique(500, 400)
    gra.graduation_x()
    gra.graduation_y()
    gra.tracecourbe(phase=0, freq=5, ampl=5, coul="green")
    root.mainloop()
