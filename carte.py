from random import randrange
import time


class jeux_cartes(object):
    """"jeux de cartes"""
    couleur = ('pique', 'trefle', 'carreau', 'coeur')
    valeur = (0, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'valet', 'dame', 'roi', 'as')

    def __init__(self):
        """construction de la liste de 52 cartes"""
        self.carte = []
        for coul in range(4):
            for val in range(13):
                self.carte.append((val + 2, coul))

    def nom_cartes(self, c):
        """renvoi de la carte c en clair"""
        return "{0} de {1}".format(self.valeur[c[0]], self.couleur[c[1]])

    def battre(self):
        """"melange de cartes"""
        t = len(self.carte)             # nombre de cartes restantes
        # pour melanger on procede a un nombre d'echanges équivalent
        for i in range(t):
            # tirage au hasard 2 emplacement dans la liste :
            h1, h2 = randrange(t), randrange(t)
            # echange de cartes situées a ces emplacements :
            self.carte[h1], self.carte[h2] = self.carte[h2], self.carte[h1]

    def tirer(self):
        """"tirage de la premiere carte de la pile"""
        t = len(self.carte)
        if t > 0:
            carte = self.carte[0]
            return carte
        else:
            return None


if __name__ == '__main__':
    jeux = jeux_cartes()
    jeux.battre()
    for n in range(52):
        c = jeux.tirer()
    if c == 0:
        print("teminer")
    else:
        print(jeux.nom_cartes(c))

star = time.time()
end = time.time()
print(end-star)
