from oscillographe import Graphique
from curseurs import *


class Voir(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.control = [0] * 3
        self.trace = [0] * 3
        self.couleur = ["green", "red", "purple"]

        self.gra = Graphique()
        self.gra.config(width=500, height=500)
        self.gra.pack(side=TOP, pady=5)
        # instanciation de 3 panneaux de controle (curseurs) :
        for i in range(3):
            self.control[i] = Choixvibra(self, self.couleur[i])
            self.control[i].pack()
        # instanciation de canvas avec x et y :
        # designation des evenement qui declanche le trace des courbes :
        self.master.bind("<Return>", self.montrecourbe)
        self.master.title("Mouvement vibratoire harmonique")
        self.pack()

    def montrecourbe(self, event):
        """(Re)affichage des trois graphiques elongation/temps"""
        for i in range(3):

            # D'abord effacer le tracé précedent (eventuel) :
            if self.trace[i] is not None:
                self.gra.delete(self.trace[i])

            # ensuite dessiner le nouveau trace :
            if self.control[i].chk.get() == 1:
                freq, phase, ampl = self.control[i].valeurs()
                self.trace[i] = self.gra.tracecourbe(freq, phase, ampl, self.couleur[i])


app = Voir()
app.mainloop()


