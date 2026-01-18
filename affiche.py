from calgeo import *


class Affiche(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self)
        self.boss = boss
        self.fen = Tk()
        self.fen.title("fenetre composée a l'aide de Frame")
        self.fen.geometry('400x500')
        self.c1 = Frame(self.fen, bg='#80c80c', width=300, height=300, relief=SUNKEN)
        self.c1.grid(column=1)
        self.car = Button(self.c1, text="Carre", bg='blue', fg='white',
                          command=Carre, width=30, relief=RAISED, bd=5, font="helvetica")
        self.car.grid(column=1)
        self.rec = Button(self.c1, text='Rectangle', bg='royal blue', fg="white",
                          command=Rectangle, width=25, relief=RAISED, bd=5, font="helevetica")
        self.rec.grid(column=1)
        self.tri = Button(self.c1, text='Triangle', bg='green', fg="white",
                          width=25, relief=RAISED, bd=5, font="helevetica")
        self.tri.grid(column=1)
        self.cer = Button(self.c1, text='Cercle', bg='#80c80c', fg="white",
                          width=25, relief=RAISED, bd=5, font="italic")
        self.cer.grid(column=1)
        self.fen.mainloop()


if __name__ == '__main__':
    can = Affiche()
