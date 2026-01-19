# encoding "utf-8"

from tkinter import *
from random import randrange


class Bouton(Button):
    def __init__(self, boss, **arguments):
        Button.__init__(self, boss, bg="yellow", fg="blue", activebackground="forest green",
                        activeforeground='black', font=("Helvetica", 14, "bold"),
                        relief=RAISED, bd=5, width=5, **arguments)


class Jeux(Frame):
    """app pour jeux de clique constructeur de la class principal derivé de la class frame"""
    def __init__(self, boss=None, haut=500, large=500):
        self.haut, self.large = haut, large
        self.run, self.x, self.y, self.r = 0, 0, 0, 30
        self.score = 0
        Frame.__init__(self)
        self.can = Canvas(self, width=large, height=haut, relief=RAISED, bd=5, bg="black")
        self.can.bind("<Button-1>", self.score1)
        self.can.pack()
        Bouton(self, text="demarer", command=self.moov).pack(side=LEFT)
        Bouton(self, text="stop", command=self.stop).pack(side=LEFT)
        Bouton(self, text="quitter", command=self.quit).pack(side=RIGHT)
        self.bal0 = self.can.create_oval(50, 50, 80, 80, fill='white')
        self.bal1 = self.can.create_oval(350, 350, 320, 320, fill='red')
        self.lab = Label(self, text=self.score, font=("Helvetica", 16))
        self.lab.pack(side=BOTTOM, pady=10)

    def anim(self):
        """fonction permettant de declanché l'animation de la 1er balle"""
        self.x, self.y = randrange(self.haut), randrange(self.large)      # melange au hasard du canvas
        self.can.coords(self.bal0, self.x, self.y, self.x+30, self.y+30)  # positionnement de la bal dans le canvas
        if self.run > 0:                                                  # animation
            self.after(1500, self.anim)

    def anim1(self):
        """fonction declanchant la 2eme balle"""
        self.x, self.y = randrange(self.haut-20), randrange(self.large-20)
        self.can.coords(self.bal1, self.x, self.y, self.x+30, self.y+30)
        if self.run > 0:
            self.after(1500, self.anim1)

    def moov(self):
        """fonction de demarage de l'animation"""
        if self.run == 0:
            self.run = 1
            self.anim()
            self.anim1()

    def stop(self):
        """fonction d'arret de l'animation"""
        self.run = 0

    def score1(self, event):
        # le comptage des points ne fait seulement quend l'app marche :
        if self.run == 1:
            # detection du point de clique :
            item = self.can.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
            # verifier sur le clique est sur la balle:
            if self.bal0 in item:
                self.score += 1
                self.lab.config(text=f"votre score = {self.score}")
                # effet visuel quand on clique sur la balle:
                self.can.itemconfig(self.bal0, fill="green")
                self.after(200, lambda: self.can.itemconfig(self.bal0, fill="white"))


# programme principal

fen = Tk()
fen.title("animation fond d'ecran")
princi = Jeux(fen)
princi.can.config(bg="green")
princi.pack(side=TOP)
fen.mainloop()


