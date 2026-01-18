import os
import cherrypy
import sqlite3
from cherrypy.lib.sessions import RamSession


class Glob(object):
    # données a caracteres globals pour l'application
    patronhtml = "spectacle.html"                                    # fichier contenant les "patrons" HTML
    html = {}                                                # les patrons seront charges dans ce dictionnaire
    # structure de la base de données. dictionnaire des tables et champs :
    dbname = "spectacle.sq3"    # nom de la base de données
    table = {"spectacles": (("ref_spt", "k"), ("titre", "s"), ("date", "t"), ("prix_pl", "r"), ("vendues", "i")),
             "resevations": (("ref_res", "k"), ("ref_spt", "i"), ("ref_cli", "i"), ("place", "i")),
             "clients": (("ref_cli", "k"), ("nom", "s"), ("e_mail", "s"), ("tel", "i"))}


def chargerpatronshtml():
    # chargement des touts les "patrons" de page html dans un dictionnaire
    # (l'encodage est précisé au cas ou il differerait de celui par defaut) :
    label, text = " ", ""
    fi = open(Glob.patronhtml, "r", encoding="utf-8")
    try:
        for ligne in fi:
            if ligne[:2] == "[*":                       # etiquette trouvé
                label = ligne[:2]                       # suppression[*
                label = label[:-1].strip()              # suppression lf et esp event
                label = label[:-2]                      # suppression *]
                text = ""
            else:
                if ligne[:5] == "#####":
                    Glob.html[label] = text

                else:
                    text += ligne
    finally:
        fi.close()                                      # le fichier sera refermé dans tout les cas


def mep(page):
    # fonction de "mise en page" du code html generé : renvoie(la page)
    # transmise, agrementé d'un en-tete et d'un bas de page adequats.
    return Glob.html["MiseEnPage"].format(page)


def listespectacles():
    # construire la liste des spectacles proposés, dans un tableau html :
    req = "SELECT ref_spt, titre, date, prix_pl, vendues FROM spectacles"
    res = BD.executerreq(req)                                    # ==> res sera une liste de tuples
    tabl = "<tqble border='1' cellpadding='s'>`\n"
    tabs = ""
    for n in range(5):
        # remarque : pour qu'elles apparaissent comme telles dans une chaine
        # formatée, les accolades doivent etres doubles :
        tabs += "<td>{{{0}}}</td>".format(n)
    lignetableau = "<tr>" + tabs + "</tr>\n"
    # la premiere ligne du tableau contiendra le en-tete de colones :
    tabl += lignetableau.format("ref.", "titre", "date", "prix des places", "vendues")
    # ligne suivante : leurs contenu est extrait de la bd :
    for ref, tit, dat, pri, ven, in res:
        tabl += lignetableau.format(ref, tit, dat, ven)
    return tabl + "</tables>"


class GestionBD(object):
    # mise en place et interfacage d'une base de données sqlite.
    def __init__(self, dbname):                                # cf. remarque du livres
        self.dbname = dbname                                   # concernant le threads

    def executerreq(self, req, param=()):
        # execution de la requete (req), avec envoie eventuel de resultat
        connex = sqlite3.connect(self.dbname)                           # etablir la connexion avec la base de donnes
        cursor = connex.cursor()                                        # creer le curseur
        cursor.execute(req, param)                                      # executer la requete SQL
        res = None
        if "SELECT" in req.upper():
            res = cursor.fetchall()                                      # res = liste de tuples
        connex.commit()                                                # enregistre systematiquement
        cursor.close()
        connex.close()
        return res                                                    # on renvoi none ou une liste de tuples

    def createtable(self, dictable):
        # creation de la base de données ci elle n'exisiste pas deja
        for table in dictable:                                       # parcours des clefs du dictionnaire
            req = "CREATE TABLE {0} (".format(table)
            pk = ""
            for descr in dictable[table]:
                nomchamp = descr[0]                                  # libellé du champ a créer
                tch = descr[1]                                       # type de champ a créer
                if tch == "i":
                    typechamp = "INTEGER"
                elif tch == "k":
                    # champ 'cle primaire' (entier incrementer automatiquement)
                    typechamp = "INTEGER PRIMARY KEY AUTOINCREMENT"
                    pk = nomchamp
                elif tch == "r":
                    typechamp = "REAL"
                else:                                                 # pour simplifier, nous considerons
                    typechamp = "text"                                # comme textes tous les autres type
                req += "{0} {1}, ".format(pk, typechamp)
            req = req[:-2] + ")"
            try:
                self.executerreq(req)
            except:
                pass                                                 # la table exsiste probablement deja


class Webspectacles(object):
    # classe generant les objets gestionnaire de requetes http

    def index(self):
        # page d'entree de site web. les variable des sessions servent a repérer
        # les operations deja effectuees (ou non) par le visiteur :
        nom = cherrypy.session.get("nom", "")
        # renvoie d'une page html adapté a la situation du visiteur :
        if nom:
            acces = cherrypy.session["acces"]
            if acces == "Acces administrateur":
                # renvoie d'une page html "statique":
                return mep(Glob.html["accesAdmin"])
            else:
                # renvoi d'une page html formatée avec le nom du visiteur :
                return mep(Glob.html["PageAccueil"])
    index.exposed = True

    def identification(self, acces="", nom="", mail="", tel=""):
        # les coords du visiteur dans des variables de session :
        cherrypy.session["nom"] = nom
        cherrypy.session["mail"] = mail
        cherrypy.session["tel"] = tel
        cherrypy.session["acces"] = acces
        if acces == "Acces administrateur":
            return mep(Glob.html["accesAdmin"])
        else:
            # une variable de session servira de "caddy" pour les reservations
            # de places de spectacles effectuées par le visiteur:
            cherrypy.session["caddy"] = []                        # liste vide au depart
            return mep(Glob.html["AccesClients"].format(nom))
    identification.exposed = True

    def reserver(self):
        # presenter le formulaire de reservation au visiteur "client" :
        nom = cherrypy.session["nom"]                          # retrouver son nom
        # retrouver dans la BD la liste des spectacles proposés :
        tabl = listespectacles()
        return mep(Glob.html["reserver"].format(tabl, nom))
    reserver.exposed = True

    def reservation(self, spect="", places=""):
        # memoriser les reservation demendeés, dans une variable de session :
        spect, places = int(spect), int(places)           # conversion en nombre
        caddy = cherrypy.session["caddy"]                 # recuperation de l'etat actuel
        caddy.append((spect, places))                     # ajout d'un tuple a la liste
        cherrypy.tools.session.on["caddy"] = caddy                 # mémorisation de la liste
        nsp, npl = len(caddy), 0
        for c in caddy:                                   # totaliser les reservation
            npl += c[1]
        return mep(Glob.html["reservations"].format(npl, nsp))
    reservation.exposed = True

    def finaliser(self):
        # Enregistrer le "caddy" du client dans la base de donnée :
        nom = cherrypy.session["nom"]
        mail = cherrypy.session["mail"]
        tel = cherrypy.session["tel"]
        caddy = cherrypy.session["caddy"]
        # Enregistrer les infos du client dans la table ad hoc :
        req = "INSERT INTO clients[nom, e_mail, tel] VALUES(?, ?, ?)"
        res = BD.executerreq(req, [nom, mail, tel])
        # Recuperer la reference qui lui a ete attribué automatiquement :
        req = "SELECT ref_cli From clients WHERE nom=?"
        res = BD.executerreq(req, (nom,))
        client = res[0][0]
        # parcours du caddy - enregistrement des places deja reserve pour chaque spectacles:
        for (spect, places) in caddy:
            # Rechercher le dernier no deja reserver pour ce spect. :
            req = "SELECT MAX(place) FROM reservation WHERE ref_spt = ?"
            res = BD.executerreq(req, (int(spect), ))
            nump = res[0][0]
            if nump is None:
                nump = 0
                # generer les no des places suivantes, les enregistrer :
                req = "INSERT INTO reservation(ref_spt, ref_cli, place) VALUES(?, ?, ?)"
                for i in range(places):
                    nump += 1
                    res = BD.executerreq(req, (spect, client, nump))
                # Enregistrer le nombres de places vendue pour ce spectacles :
                req = "UPDATE spectacles SET vendue=? WHERE ref_spt=?"
                res = BD.executerreq(req, (nump, spect))
            cherrypy.session["caddy"] = []                             # vider le caddy
            cherrypy.session["nom"] = ""                               # "oublier" le visiteur
            return mep("<h3>Session terminée </h3>")
    finaliser.exposed = True

    def revoir(self):
        # Retrouver les réservations faite par un client particulier.
        # (on retrouve sa reference a l'aide de son courriel) :
        mail = cherrypy.session["mail"]
        req = "SELECT ref_cli, nom, tel FROM clients WHERE e_mail=?"
        res = BD.executerreq(req, (mail,))
        client, nom, mail = res[0]
        # spectacles pour lesquels il a acheté des places :
        req = "SELECT titres, date, place, prix_pl "\
              "FROM reservation JOIN spectacles USING (ref_spt)"\
              "WHERE ref_cli=? ORDER BY titrem plqce"
        res = BD.executerreq(req, (client,))
        # construction d'un tableau html pour listée les infos trouvées :
        tabl = "<table border ='1' cellpadding='5'>\n"
        tabs = ""
        for n in range(4):
            tabs += "<td>{{{0}}}</td>".format(n)
        lignetableau = "<td>'+tabs+'</td>\n"
        # la prémiere ligne du tableau contient les en-tete de colonnes :
        tabl += lignetableau.format("titre", "date", "no place", "prix")
        # ligne suivantes :
        tot = 0
        for titre, date, place, prix in res:
            tabs += lignetableau.format(titre, date, place, prix)
            tot += prix
        # ajouter une ligne en bas du tableau avec le total en bonne place :
        tabl += lignetableau.format("", "", "total", str(tot))
        tabl += "</table>"
        return mep(Glob.html["revoir"].format(nom, mail, tabl))
    revoir.exposed = True

    def entrerspectacles(self):
        # Retrouver la listes des spectacles exisistants :
        tabl = listespectacles()
        # Renvoyer un formulaire pour l'ajout d'un nouveau spectacles :
        return mep(Glob.html["entrerspectacles"].format(tabl))
    entrerspectacles.exposed = True

    def memospectacles(self, titre="", date="", prixpl=""):
        # memoriser un nouveau spectacles :
        if not titre or not date or not prixpl:
            return "<h4>Completez les champs ![<a href='/'>Retour1</a>]</h4>" \
                   "<background-color=yellow></p>"

        req = "INSERT INTO spectacles (titre, date, prixpl, vendues)"\
              "VALUES(?, ?, ?)"
        msg = BD.executerreq(req, (titre, date, float(prixpl), 0))
        if msg: return msg                                     # message d'erreur
        return self.index()                                    # Retour a la pge d'acceuil
    memospectacles.exposed = True

    def toutereservations(self):
        # lister les reservations effectuées par chaque client :
        req = "SELECT titre, nom, e_mail, COUNT(place) FROM spectacles"\
              "LEFT JOIN reservation USING (re_spt)"\
              "LEFT JOIN clients USING(ref_cli)"\
              "GROUP BY nom, titre"\
              "ORDER BY titre, nom"
        res = BD.executerreq(req)
        # construction d'un tableau html pour lister les infos trouvées :
        tabl = "<tableborder='1' cellpadding='5'>\n"
        tabs = ""
        for n in range(4):
            tabs += "<td>{{{0}}}</td>".format(n)
            lignetableau = "<tr>+tabs+</tr>\n"
            # la premiere ligne du tableau contient le en-tete des colonne :
            tabl += lignetableau.\
                format("titre", "nom client", "courriel", "places reserves")
            # ligne suivantes :
            for tit, nom, mail, pla in res:
                tabs += lignetableau.format(tit, nom, mail, pla)
            tabl += "</table>"
            return mep(Glob.html["toutereservations"].format(tabl))
    toutereservations.exposed = True


# Programme principal
# Ouverture de la base de données :
BD = GestionBD(Glob.dbname)
BD.createtable(Glob.table)
# chargement des patrons des pages web dans un dictionnaire globale :
chargerpatronshtml()
# Reconfiguration et demmarage du serveur web :
cherrypy.config.update({"tools.staticdir.root": os.getcwd()})
cherrypy.config.update({"tools.sessions.on": True})
cherrypy.quickstart(Webspectacles(), config="tutoriel.conf")
