from tkinter import *
from math import pi, sin, cos


class Canon(object):
    """petit canon graphique"""
    def __init__(self, boss, x, y):
        self.boss = boss                          # reference de canvas
        self.x1, self.y1 = x, y                             # axe de rotation du canon
        # dessiner la buse du canon a l'horizontal pour commencer :
        self.ibu = 50
        self.x2, self.y2 = x + self.ibu, y
        self.buse = boss.create_line(self.x1, self.y1, self.x2, self.y2, width=10)
        # dessiner le corp du canon par dessu :
        r = 20                                              # rayon du cercle
        boss.create_oval(x-r, y-r, x+r, y+r, fill='blue', width=5)
        # dessiner un obus (reduit a un simple point , avant animation) :
        self.obus = boss.create_oval(x, y, x, y, fill="red")
        self.anim = False                              # interupteur d'animation
        # retrouver la hauteur et la largeur du canvas :
        self.xmax = int(boss.cget('width'))
        self.ymax = int(boss.cget('height'))

    def feu(self):
        "declancher le tir d'un obus"
        if not self.anim:
            self.anim = True
            # position de depart de l'obus (ce la bouche du canon)
            self.boss.coords(self.obus, self.x2-5, self.y2-5, self.x2+5, self.y2+5)
            v = 8.25            # vitesse initiale
            # composante horizontale et verticale de cette vitesse :
            self.vy = -v * sin(self.angle)
            self.vx = v * cos(self.angle)
            self.animer_obus()

    def animer_obus(self):
        # animation de l'obus trajectoire balistique :
        if self.anim:
            self.boss.move(self.obus, int(self.vx), int(self.vy))
            self.vy += 0
            self.boss.after(500, self.animer_obus)
            if self.vx > 200 or self.vy > 200:
                self.anim = False


    def orienter(self, angle):
        """choisir l'angle de tir du canon"""
        # ram : le parametre (angle) est recu en tant que chaine de car
        # il faut le traduire en nombre reel, puis convertir en radian :
        self.angle = float(angle) * 2 * pi/360
        self.x2 = self.x1 + self.ibu * cos(self.angle)
        self.y2 = self.y1 - self.ibu * sin(self.angle)
        self.boss.coords(self.buse, self.x1, self.y1, self.x2, self.y2)


if __name__ == "__main__":
    # code pour tester normalment la class canon :
    f = Tk()
    can = Canvas(f, width=300, height=300, bg='ivory')
    can.pack(padx=10, pady=10)
    c1 = Canon(can, 25, 200)
    Button(f, text='FEU', command=c1.feu).pack(side=LEFT)
    s1 = Scale(f, label='hausse', from_=90, to=9, command=c1.orienter)
    s1.pack(side=LEFT, pady=5, padx=5)
    s1.set(45)

    f.mainloop()

