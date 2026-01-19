from random import *
from tkinter import *

# _*_ encoding utf-8 _*_


def tirage():
    """def qui permet de faire le tirage"""
    i, comte = 0, 0
    tir = [0] * 100
    for i in range(1, 100):                            # generation des 100 nombres et leurs melange
        tir[i] = random()
        comte = [0] * 5                                # tirage des cinq nombre choisie dans les 100 aleatoire
    for val in tir:
        index = int(val*5)
        comte[index] = comte[index]+1
    return comte


def affiche(event=None):
    """def qui permet l'affichage des textes dans la fenetre kinter"""
    chaine1 = ent.get()
    chaine.configure(text=str(chaine1))                 # affichage des nombres choisis
    chaine2.configure(text=str(tirage()))               # affichage des nombres tirés


def age():
    val1 = val.get()
    if val1 < 1:
        lab.config(text="cochez la case d'abord")
    elif val1 > 0:
        lab.config(text='vous pouvez tirez 18+')           # def pour verifié le clic sur le button a cocher


# creation de la fenetre principal


fen = Tk()
fen.title("jeux de loto")
fen.geometry("500x450", )
txt = Label(fen, text="chisissez vos 5 numeros entre 1 et 99 :", fg="black")
txt.pack()
ent = Entry(fen, bd=10, bg="white", fg="black",)
ent.pack()
txt1 = Label(fen, text="ce jeux est reservé au 18 ans \n ou plus cochez la case pour \n "
                       "accepté nos conditions ", fg="red")
txt1.pack()
val = IntVar()
case = Checkbutton(fen, text='cochez la case', variable=val, command=age)
case.pack()
txt2 = Label(fen, text="les 5 numerons choisie sont :", fg="black", bg="yellow")
txt2.pack()
chaine = Label(fen, fg="black")
chaine.pack()
bou = Button(fen, text="lancer le tirage", fg="white", bg="black",  bd=10, command=tirage)
bou.bind("<ButtonRelease>", affiche)
bou.pack()
chaine2 = Label(fen, fg="black")
chaine2.pack()
lab = Label(fen, fg="red")
lab.bind('<ButtonRelease>', age)
lab.pack()
fen.mainloop()
