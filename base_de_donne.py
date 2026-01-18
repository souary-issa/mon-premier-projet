from pg8000 import dbapi


class Glob(object):
    """espaces des noms pour les variables et fonctions (psodo-global)"""                                                # utilisateur

    host = "127.0.0.1"                                       # nom ou adresse IP du serveur
    port = 5432
    # structure de la base de donnees. dictionnaire des tables et champs :
    dicoT = {
        'compositeurs': [
            ("id_champ", "K", "cle primaire"),
            ("nom", 25, "nom"),
            ("prenom", 25, "prenom"),
            ("a_nais", "i", "annee de naissance"),
            ("a_mort", "i", "annee de mort")],
        'oeuvre': [
            ("id_oeuv", "k", "cle primaire"),
            ("id_comp", "i", "cle compositeurs"),
            ("titre", 50, "titre de l'oeuvre"),
            ("duree", "i", "duree(en minute)"),
            ("interpr", 30, "interprete principal")]
    }


class Connect(Glob):
    def __init__(self, port=Glob.port, host=Glob.host):
        Glob.__init__(self)
        try:
            self.user = input("entrez votre nom : ")
            self.dbname = input("entrez le nom de la base de donnée : ")
            self.passwd = input("entrez  votre mot de pass : ")
            self.basdon = dbapi.Connection(host=host, port=port, database=self.dbname, user=self.user, password=self.passwd)
        except Exception as err:
            print("eurreur de connexion a la base de donnée :\n"
                  "Erreur detecte : ", err)
            self.echec = 1
        else:
            self.cur = self.basdon.cursor()
            self.echec = 0
            self.ssl_context = True
            print("connexion reussi a la base de donnée ! ! !")

    def ecrire(self):
        try:
            req = input("entrez votre requete SQL : ")
            self.cur.execute(req)
        except Exception as err:
            print("requete SQL erronne ", err)
        else:
            self.basdon.commit()

    def creer_tables(self, dicoT):
        """creation des tables decrites dans le dico dictable"""
        for table, champs, in dicoT.items():
            req = "CREATE TABLE {} ( ".format(table)
            pk = ""
            first_field = True
            for descr in champs:                   # libellé du champ a creér
                nomchamp = descr[0]                # premier champ
                tch = descr[1]                     # 2eme champ
                commentaire = descr[2]             # 3eme champ les commentaire
                if not first_field:
                    req += ", "
                else:
                    first_field = False
                if tch == "K":
                    # cle primaire auto incrementer:
                    req += "{} SERIAL".format(nomchamp)
                    pk = nomchamp
                elif tch == 'i':
                    req += "{} INTEGER".format(nomchamp)
                else:
                    # VACHAR avec la taille specifié :
                    req += " {} VARCHAR ({})".format(nomchamp, tch)
            # Ajout de la contrainte de cle primaire  :
            if pk:
                req += ", PRIMARY KEY ({})".format(pk)
            req += ")"
            try:
                self.cur.execute(req)
                self.basdon.commit()
                print("table ' {} ' créée avec succes".format(table))
            except Exception as err:
                print("Erreur creation table {}: {}'".format(table, err))
                self.basdon.rollback()

    def voir_table(self):
        while 1:
            req = input("entrez votre requete sql : ")
            self.cur.execute(req)
            try:
                resultat = self.cur.fetchall()
                # afficher le nom des colones :
                colones = [description[0] for description in self.cur.description]
                print(" | ".join(colones))
                print("-" * (len("|".join(colones)) + 10))
                # afficher les donnees :
                for row in resultat:
                    print(" | ".join(str(value) for value in row))
            except Exception as err:
                print("requete sql erronne : ", err)
                if req == "":
                    print("au revoir deconnexion de la base de donnée ")
                    break

    def remplir(self):
        dico = [('Vivaldi', 'Mozart', 'Brahms', 'Beethoven', 'Beethoven', 'Schubert',
                'Haydn', 'Chopin', 'Bach', 'Beethoven', 'Mozart', 'Mozart', 'Beethoven')]
        comps = [(comp,) for comp in dico[0]]
        for champs in comps:
            req = "INSERT INTO oeuvre (comps) VALUES (%s)"
            self.cur.execute(req, champs)
            self.basdon.commit()


con = Connect()
print()
choix = input("entrez un nombre pour votre choix :\n"
              "1 : pour ecrire dans la base:\n"
              "2 : pour consultez la base : \n"
              "3 : pour creer des tables : \n"
              "4 : pour remplir la base : \n"
              "ou Enter pour quitter \n")
if choix == "1":
    con.ecrire()
elif choix == "2":
    con.voir_table()
elif choix == "3":
    con.creer_tables(con.dicoT)
elif choix == "4":
    con.remplir()
elif choix == "":
    print("au revoir deconexion de la base de donneé", con.dbname)
