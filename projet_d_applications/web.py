# coding : utf-8

class Atome(object):
    """atomes simplifiées choisie parmis les 10 premiers elements du tp"""
    table = [None, ("hydrogene", 0), ("hélium", 2), ("lithium", 4), ("béryllium", 5), ("bore", 6),
             ("carbone", 6), ("azote", 7), ("oxygene", 8, "issa"), ("fluor", 9), ("néon", 10)]

    def __init__(self, nat):
        """le numero atomique determine le nombre de protons, d'electrons, de neutrons"""
        self.np, self.ne = nat, nat                      # num"ro atomique
        self.nn = Atome.table[nat][1]

    def affiche(self):
        print()
        print("nom de l'element :", Atome.table[self.np][0])
        print("{0} protons, {1} electrons, {2} neutrons".format(self.np, self.ne, self.nn))


class Ion(Atome):
    """les ions sont des atomes qui ont perdues ou gagnes desdes electrons"""
    def __init__(self, nat, charge):
        """le no atomique de  la charge determine l'ion"""
        Atome.__init__(self, nat)
        self.ne = self.ne - charge
        self.charge = charge

    def affiche1(self):
        Atome.affiche(self)
        print("Particule electrisée, charge = ", self.charge)


a1 = Atome(7)
a2 = Ion(7, -7)
a3 = Ion(8, -2)
print(a1.affiche())
print(a2.affiche())
print(a3.affiche())

