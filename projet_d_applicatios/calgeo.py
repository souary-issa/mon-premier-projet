from tkinter import*


class Carre(Canvas):
    """construction de la class rectangele par derivation de la classe canvas"""
    def __init__(self, boss=" ", haut=200, large=300):
        Canvas.__init__(self)
        self.a0, self.a1 = StringVar(), StringVar()
        self.haut, self.large, self.final, self.nom = haut, large, 0, "carre"
        self.can = Canvas(bg="yellow")
        self.can.grid(row=1, column=1)

        self.master.title("calculatrice géometique")
        Label(text="entree la largeur en metre :").grid(row=2, column=0)
        self.txt = Entry(textvariable=self.a0)
        self.txt.bind('<Return>', self.calcule)
        self.txt.grid(row=3, column=0)
        Label(text="entrez la longueur en metre : ").grid(row=2, column=2)
        self.txt1 = Entry(textvariable=self.a1)
        self.txt1.bind('<Return>', self.calcule)
        self.txt1.grid()
        self.txt1.bind('<Return>', self.calcule)
        self.txt1.grid(row=3, column=2)

    def calcule(self, p):                                       # methode d'affichage dans le canvas
        self.can.create_rectangle(150, 90, 250, 190)            # et les differents calcule geometrique
        self.can.create_text(200, 80, text=self.txt.get() + "m", font="bold")
        self.can.create_text(130, 140, text=self.txt1.get(), font="bold")
        # calcule du resultat final a affiche dans le canvas
        a0, a1 = float(self.a0.get()), float(self.a1.get())
        self.final = a0 * a1
        peri = (a0+a1) * 2
        peri1 = str(peri)
        self.can.create_text(170, 20, text="la surface du " + self.nom + " = " + str(self.final) + ' m²',
                             font="bold")
        self.can.create_text(180, 40, text="le perimetre du " + self.nom + " = " + peri1 + " ml",
                             font="bold")


class Rectangle(Canvas):
    """construction de la class carre par derivation de la class canvas"""
    def __init__(self, boss=None, haut=200, large=300):
        Canvas.__init__(self)
        self.a0, self.a1 = StringVar(), StringVar()
        self.haut, self.large, self.final, self.nom = haut, large, 0, "rectangle"
        self.can = Canvas(bg="cadet blue")
        self.can.grid(row=1, column=1)
        Label(text="entree la longuer en metre :").grid(row=2, column=0)
        self.txt = Entry(textvariable=self.a0)
        self.txt.bind('<Return>', self.calcule)
        self.txt.grid(row=3, column=0)
        Label(text="entrez la largeur en metre : ").grid(row=2, column=2)
        self.txt1 = Entry(textvariable=self.a1)
        self.txt1.bind('<Return>', self.calcule)
        self.txt1.grid()
        self.txt1.bind('<Return>', self.calcule)
        self.txt1.grid(row=3, column=2)

    def calcule(self, p):                                          # methode d'affichage dans le canvas
        self.can.create_rectangle(100, 80, 280, 180)
        self.can.create_text(180, 70, text=self.txt.get() + "m", font="helvetica")
        self.can.create_text(80, 140, text=self.txt1.get(), font="helvetica")
        # calcule du resultat final a affiche dans le canvas
        a0, a1 = float(self.a0.get()), float(self.a1.get())
        self.final = a0 * a1
        peri = (a0+a1) * 2
        peri1 = str(peri)
        self.can.create_text(170, 20, text="la surface du " + self.nom + " = " + str(self.final) + ' m²',
                             font="helvetica")
        self.can.create_text(175, 40, text="le perimetre du " + self.nom + " = " + peri1 + " ml",
                             font="helvetica")


class Cercle(Canvas):
    """constructeur de la classe cercle et ces differente methode"""
    def __init__(self):
        Canvas. __init__(self)


# programme principal
if __name__ == "__main__":
    root = Carre()
    root.mainloop()
