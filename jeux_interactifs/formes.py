from tkinter import *


class Menubar(Frame):
    """"barres de menus deroulants"""
    def __init__(self, boss=None):
        Frame.__init__(self, borderwidth=10)
        # variable tkinter
        self.relief = IntVar()
        self.actpeint = IntVar()
        self.actmusi = IntVar()
        # menu (fichier)
        filemenu = Menubutton(self, text="fichier", bg="yellow", relief=RAISED, bd=5, activebackground="light blue")
        filemenu.pack(side=LEFT)
        # partie "deroulant"
        me1 = Menu(filemenu)
        me1.add_command(label="Effacer", underline=8, command=boss.effacer)
        me1.add_separator()
        me1.add_command(label="Terminer", underline=8, command=boss.quit)
        me1.add_separator()
        me1.add_command(label='issa', foreground="blue")
        # integration du menu :
        filemenu.config(menu=me1)
        # ajout d'un menu musiciens
        self.musi = Menubutton(self, text="musiciens")
        self.musi.pack(side=LEFT, padx=3)
        # partie deroulante du menu (musiciens)
        me1 = Menu(self.musi)
        me1.add_command(label="17e siecle", underline=1, foreground="red",
                        background="white", font=("comic Sans ms", 14), command=boss.Showmusi17e)
        me1.add_command(label="18e siecle", underline=1, foreground="royal blue",
                        background="white", font=("Comic Sans ms", 14, "bold"), command=boss.Showmusi18e)
        # integration du menu
        self.musi.config(menu=me1)
        # ajout d'un menu peintre
        self.peint = Menubutton(self, text="peintres", relief=RAISED, bd=5)
        self.peint.pack(side=LEFT, padx=3)
        # partie deroulante
        me1 = Menu(self.peint)
        me1.add_command(label="classique", state=DISABLED)
        me1.add_command(label="romantique", underline=0, command=boss.Showromanti)
        # sous menu pour les peintres impressionistes :
        me2 = Menu(me1)
        me2.add_command(label="claud monet", underline=7, command=boss.tabmonet)
        me2.add_command(label="August renoir", underline=8, command=boss.tabrenoir)
        # integration du sous menu
        me1.add_cascade(label="impressionistes", underline=0, menu=me2)
        me3 = me1
        me2.add_cascade(label="claud monet", underline=1, menu=me3)
        # integration du menu
        self.peint.config(menu=me1)
        # menu (option)
        optmenu = Menubutton(self, text="option")
        optmenu.pack(side=LEFT, padx=3)
        # partie deroulante :
        self.mo = Menu(optmenu)
        self.mo.add_command(label="Activer :", foreground="blue")
        self.mo.add_checkbutton(label="musiciens", command=self.choixactif, variable=self.actmusi)
        self.mo.add_checkbutton(label="peintres", command=self.choixactif, variable=self.actpeint)
        self.mo.add_separator()
        self.mo.add_command(label="Relief", foreground="blue")
        for (v, forme) in [(0, "aucun"), (1, "sorti"), (2, "rentré"), (3, "sillon"), (4, "crete"), (5, "bordure")]:
            self.mo.add_radiobutton(label=forme, variable=self.relief, value=v, command=self.reliefbarre)
        # integration du menu
        optmenu.configure(menu=self.mo)

    def reliefbarre(self):
        choix = self.relief.get()
        self.config(relief=[FLAT, RAISED, SUNKEN, GROOVE, RIDGE, SOLID][choix])

    def choixactif(self):
        p = self.actpeint.get()
        m = self.actmusi.get()
        self.peint.config(state=[DISABLED, NORMAL][p])
        self.musi.config(state=[DISABLED, NORMAL][m])


class Application(Frame):
    """"Application principale"""
    def __init__(self, boss=None):
        Frame.__init__(self)
        self.master.title("FENETRE AVEC MENU")
        mbar = Menubar(self)
        mbar.pack()
        self.can = Canvas(self, bg="light blue", height=300, width=500, borderwidth=2)
        self.can.pack()
        mbar.mo.invoke(2)
        self.pack()

    def effacer(self):
        self.can.delete(ALL)

    def Showmusi17e(self):
        self.can.create_text(160, 10, anchor=NE, text="M Purcell", font=("Times", 20, "bold"), fill="yellow")

    def Showmusi18e(self):
        self.can.create_text(190, 125, anchor=SE, text="W. A. Mozart", font=("Times", 20, "italic"), fill="dark green")

    def Showromanti(self):
        self.can.create_text(245, 70, anchor=NW, text="E de lacorix", font=("Times", 20, "bold italic"), fill="blue")

    def tabmonet(self):
        self.can.create_text(10, 100, anchor=NW, text="Nymphee a giverny", font=("Technical", 20), fill="red")

    def tabrenoir(self):
        self.can.create_text(10, 130, anchor=NW, text="le moulin de la galette",
                             font=("Dom Casual BT", 20), fill="maroon")

    def tabdegas(self):
        self.can.create_text(10, 160, anchor=NW, text=" Danseuses au repos",
                             font=("President", 20), fill="purple")


if __name__ == "__main__":
    app = Application()
    app.mainloop()





