from tkinter import *
from math import pi


class Choixvibra(Frame):
    """curseur por choisir fréquence phase et amplitude d'une vibration"""
    def __init__(self, boss=None, coul='green'):
        Frame.__init__(self, width=500, height=500)                              # constructeur de la class parente
        # initialisation de quelque attributs de d'instance
        self.freq, self.phase, self.ampl, self.coul = 0, 0, 0, coul
        # variable d'etat de la case a cocher :
        self.chk = IntVar()                         # objet variable tkinter
        Checkbutton(self, text='Afficher', variable=self.chk,
                    fg=self.coul, command=self.setcurve).pack(side=LEFT)
        # definition des 3widget curseurs
        Scale(self, length=150, orient=HORIZONTAL, sliderlength=25, label='frequence hz :', troughcolor='yellow',
              from_=-1, to=9., tickinterval=2, resolution=0.25,
              command=self.setfrequency, relief=SOLID).pack(side=LEFT)
        Scale(self, length=200, orient=HORIZONTAL, sliderlength=15, label='phase(degre) :', troughcolor='yellow',
              from_=-180, to=180, tickinterval=90,
              command=self.setphase, relief=SOLID).pack(side=LEFT, padx=5, pady=5)
        Scale(self, length=150, orient=HORIZONTAL, sliderlength=25, label='amplitude :',
              from_=1, to=9, tickinterval=2, troughcolor='yellow',
              command=self.setamplitude, relief=SOLID).pack(side=LEFT)

    def setcurve(self):
        self.event_generate('<Return>')

    def setfrequency(self, f):
        self.freq = float(f)
        self.event_generate('<Return>')

    def setphase(self, p):
        pp = float(p)
        self.phase = pp * 2*pi/360
        self.event_generate('<Return>')

    def setamplitude(self, a):
        self.ampl = float(a)
        self.event_generate('<Return>')

    def valeurs(self):
        acces = (self.freq, self.phase, self.ampl)
        return acces

# code pour tester la classe :


if __name__ == '__main__':

    def affichetout(event=None):
        lab.configure(text='{0} / {1} / {2:8.2f} / {3}'.format(fra.chk.get(), fra.freq, fra.phase, fra.ampl))

    root = Tk()
    fra = Choixvibra()
    fra.pack()
    fra.configure(bd=5, relief=SUNKEN)
    lab = Label(root, text="test")
    lab.pack(side=TOP)
    root.bind('<Return>', affichetout)
    root.mainloop()





