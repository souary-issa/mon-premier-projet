from tkinter import *
from math import sin, cos, pi
from random import randrange


class Canon(object):
    """petit canon graphique"""
    def __init__(self, boss, id, x, y, sens, coul):
        self.boss = boss                                  # ref du canvas
        self.appli = boss.master                          # ref. de la fenetre d.application
        self.id = id                                      # identifiant de canon(chaine)
        self.coul = coul                                  # couleur associé aux canons
        self.x1, self.y1 = x, y                           # axe de rotation de canon
        self.sens = sens                                  # sens de tir(+1: gauche, -1: droite)
        self.ibu = 30                                     # longuer de la buse
        self.angle, self.guns = 0, 0                                    # hausse par defaut(angle de tir)
        # retrouver la hauteur et la largeur du canvas
        self.xmax = int(boss.cget("width"))
        self.ymax = int(boss.cget("height"))
        # dessiner la buse du canon (horizontal)
        self.x2, self.y2 = x + self.ibu * sens, y
        self.buse = boss.create_line(self.x1, self.y1, self.x2, self.y2, width=10)
        # dessiner le corp du canon cercle de couleur
        self.rc = 15                                      # rayon du cercle
        self.corp = boss.create_oval(x - self.rc, y - self.rc, x + self.rc, y + self.rc, fill=coul)
        # pré-dessiner un obus caché (point en dehors du canvas) :
        self.obus = boss.create_oval(-10, -10, -10, -10, fill='red')
        self.anim = False                                 # indicateur d'animation
        self.explo = False                                # et d'explosion

    def orienter(self, angle):
        "régler la hausse du canon"""
        # rem : le parametre (angle) est recu en tant que chaine.
        # il faut donc le traduire  en reel puis le convertir en radian :
        self.angle = float(angle) * pi/360
        # rem : utliser la methode coords de preference avec des entiers :
        self.x2 = int(self.x1 + self.ibu * cos(self.angle) * self.sens)
        self.y2 = int(self.y1 - self.ibu * sin(self.angle))
        self.boss.coords(self.buse, self.x1, self.y1, self.x2, self.y2)

    def deplacer(self, x, y):
        "amener le canon dans une nouvelle position x, y"""
        dx, dy = x - self.x1, y - self.y1                  # valeur du deplacement
        self.boss.move(self.buse, dx, dy)
        self.boss.move(self.corp, dx, dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def feu(self):
        "tir d'un obus - seulement ci le precedent a fini son vol"""
        if not(self.anim or self.explo):
            self.anim = True
            # recuperer la description des tous les canons presents :
            self.guns = self.appli.dicoCanon()
            # position de depart de l'obus (ce la bouche du canon)
            self.boss.coords(self.obus, self.x2 - 3, self.y2 - 3, self.x2 + 3, self.y2 + 3)
            v = 17                                         # vitesse initiale
            # composante horizontale et verticale de cette vitesse
            self.vx = -v * sin(self.angle)
            self.vy = v * cos(self.angle) * self.sens
            self.anim_obus()
            return True                                  # => signaler le coup est partie
        else:
            return False                                 # => le coup n'a pas pu etre tiré

    def anim_obus(self):
        """animer l'obus(trajectoire balistique)"""
        if self.anim:
            self.boss.move(self.obus, int(self.vx), int(self.vy))
            c = tuple(self.boss.coords(self.obus))                      # coord. resultantes
            x0, y0 = c[0] + 3, c[1] + 3                                 # coord de centre de l'obus
            self.test_obstacle(x0, y0)                                  # a-t-on atteint un obstacle
            self.vy += .4                                               # acceleration verticale
            self.boss.after(20, self.anim_obus())
        else:
            # animation terminer - cacher l'obus et deplacer le canon :
            self.fin_animation()

    def test_obstacle(self, x0, y0):
        " evaluer ci l'obus a atteint une cible ou les limite du jeu"
        if y0 > self.ymax or x0 > self.xmax:
            self.anim = False
            return
        # analyser le dictionnaire des canons pour voir si les coords.
        # de l'un d'entre eux sont proche de celle de l'obus :
        for id in self.guns:                                            # id = cle dans le dictionnaire.
            gun = self.guns[id]                                         # valeur corsspondante
            if x0 < gun.x1 + self.rc and x0 > gun.x1 - self.rc and y0 < gun.y1 + self.rc and y0 > gun.y1 -self.rc:
                self.anim = False
                # dessiner l'explosion de l'obus (cercle jaune)
                self.explo = self.boss.create_oval(x0 - 10, y0 - 12, x0 + 12, y0 + 12, fill="yellow", width=0)
                self.hit = id                                          # reference de la cible touché
                self.boss.after(150, self.fin_explosion)
                break

    def fin_explosion(self):
        "effacer l'explosion : reinitialiser l'obus: gerer le score"
        self.boss.delete(self.explo)                                       # effacer l'explosion
        self.explo = False                                                 # autoriser un nouveau tir
        # signale le succes a la fenetre maitresse :
        self.appli.goal(self.id, self.hit)

    def fin_animation(self):
        " action a accomplir lorseque l'obus a terminer sa trajectoire "
        self.appli.disperser()                                              # deplacer le canon
        # cacher l'obus en l'expediant heors du canvas :
        self.boss.coords(self.obus, -10, -10, -10, -10)


class Pupitre(Frame):
    """pupitre de pointage associé a un canon"""
    def __init__(self, boss, canon, coul="", id="", sens=0):
        Frame. __init__(self, bd=3, relief=GROOVE)
        self.score = 0
        self.appli = boss                                                 # ref. de l'application
        self.canon = canon                                                 # ref. de canon associé
        self.coul, self.id, self.sens = coul, id, sens
        # systeme de reglage de l'angle de tir :
        self.regl = Scale(self, from_=85, to=-15, troughcolor=canon.coul, command=self.orienter)
        self.regl.set(45)                                                  # angle initial de tir
        self.regl.pack(side=LEFT)
        # etiquette d'identification du canon :
        Label(self, text=canon.id).pack(side=TOP, anchor=W, pady=5)
        # bouton de tir :
        self.btir = Button(self, text='FEU', command=self.tirer)
        self.btir.pack(side=BOTTOM, padx=5, pady=5)
        Label(self, text="points").pack()
        self.points = Label(self, text="0", bg="white")
        self.points.pack()
        # positioner a gauche ou adroite selon le sens du canon :
        if canon.sens == -1:
            self.pack(padx=5, pady=5, side=RIGHT)
        else:
            self.pack(padx=5, pady=5, side=LEFT)

    def tirer(self):
        "declancher le tir du canon associé"
        self.canon = Canon.feu()

    def orienter(self, angle):
        "ajuster la hausse du canon associé"
        self.canon.orienter(angle)

    def attribuerpoints(self, p):
        "incrementer ou decrementer le score de(p) points"
        self.score += p
        self.points.config(text=' %s ' % self.score)


class Application(Frame):
    """fenetre principale de l'application"""
    def __init__(self):
        Frame.__init__(self)
        self.master.title(">>>>>>> boom ! boom ! <<<<<<<<<")
        self.pack()
        self.can = Canvas(self.master, width=400, height=250, bg='ivory', bd=3, relief=SUNKEN)
        self.can.pack(padx=8, pady=8, side=TOP)

        self.guns = {}                           # dictionnaire des canons présents
        self.pupi = {}                            # dictionnaire des pupitres presents
        # instanciation de 2 objets canons (+1, -1, = sens opposes) :
        self.guns["issa"] = Canon(self.can, 'issa', 30, 200, 1, 'red')
        self.guns["linus"] = Canon(self.can, 'linus', 370, 20, -1, 'blue')
        # instanciation de 2 pupitre de pointages associés a ces canons :
        self.pupi['issa'] = Pupitre(self, self.guns["issa"])
        self.pupi['linus'] = Pupitre(self, self.guns["linus"])

    def disperser(self):
        "deplacer aleatoirment les canons"""
        for id in self.guns:
            gun = self.guns[id]
            # positionner a gauche ou a droite selon sens du canon :
            if gun.sens == -1:
                x = randrange(320, 380)
            else:
                x = randrange(20, 80)
                # deplacement prprement dit :
                gun.deplacer(x, randrange(150, 240))

    def goal(self, i, j):
        "le canon <i> signale qu'il a atteint l'adversaire <j>"
        if i != j:
            self.pupi[i].attribuerpoints(1)
        else:
            self.pupi[i].attribuerpoints(-1)

    def dicoCanon(self):
        "renvoyer le dictionnaire decrivant les canons presents"
        return self.guns


if __name__ == '__main__':
    Application().mainloop()


























