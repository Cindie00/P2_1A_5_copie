#########################################################################################
#
#  ce fichier extrait toutes les données nécessaires pour les graphes de la base de données remplie
#
################################################################

## les imports
#
from flask import Blueprint
from flask import render_template
from flaskr.db import get_db

bp = Blueprint("index", __name__)


## Recherche des données dans les tables insert_...sql
#
## Max
## extracteur de données pour la Question 1 sur le site ou l'exercice 1 de la liste (sur le site de Renaud Detry)
#
def Pourcentages():
    '''
    pre:/
    post: pourcentage naissances par jour du cycle lunaire
    '''

    db = get_db()

    def makeDates(Jfrom, Mfrom, Yfrom, Jto, Mto, Yto):
        '''
        pre: Jfrom, Mfrom, Yfrom, Jto, Mto, Yto des integer
        post: calendrier lunaire
        '''
        jours = Jfrom
        mois = Mfrom
        annee = Yfrom

        dates = {}

        dates[f"{jours:02}/{mois:02}/{annee}"] = 0
        while not (jours == Jto and mois == Mto and annee == Yto):
            jours += 1
            if mois == 2:
                if annee % 4 != 0 and jours == 29:
                    jours = 1
                    mois += 1
                elif annee % 4 == 0 and jours == 30:
                    jours = 1
                    mois += 1
            elif mois % 2 == 1:
                if mois <= 7 and jours == 32:
                    jours = 1
                    mois += 1
                if mois > 7 and jours == 31:
                    jours = 1
                    mois += 1
            elif mois % 2 == 0:
                if mois <= 7 and jours == 31:
                    jours = 1
                    mois += 1
                if mois > 7 and jours == 32:
                    jours = 1
                    mois += 1

            if mois == 13:
                mois = 1
                annee += 1

            dates[f"{jours:02}/{mois:02}/{annee}"] = 0
        return dates

    Dates = makeDates(int(tuple(db.execute("select date from velages"))[0][0][0:2]),
                      int(tuple(db.execute("select date from velages"))[0][0][3:5]),
                      int(tuple(db.execute("select date from velages"))[0][0][6:]),
                      int(tuple(db.execute("select date from velages"))[-1][0][0:2]),
                      int(tuple(db.execute("select date from velages"))[-1][0][3:5]),
                      int(tuple(db.execute("select date from velages"))[-1][0][6:]))

    for born in db.execute("select date from velages"):
        Dates[born[0]] += 1

    cycle = []
    for a in range(28):
        cycle.append(0)

    n = 0
    for c in range(0, len(Dates) - 28, 29):
        tnc = 0
        for t in range(28):
            tnc += list(Dates.items())[c + t][1]  # tnc: Total de naissance du cycle
        if tnc != 0:
            for i in range(28):
                cycle[i] += list(Dates.items())[c + i][1] * (100 / tnc)
        n += 1

    for m in range(len(cycle)):
        cycle[m] = round(cycle[m] / n, 2)

    Somme = 0
    for i in cycle:
        Somme += i

    return cycle


##Cindie
#
## Extracteur de données pour la Question 2 sur le site ou l'exercice 4.2. de la liste (sur le site de Renaud Detry)
#
def FamillesStatistiques():
    '''
    pre:/
    post: renvoie une liste triée en ordre croissant du nombre de veaux morts prématurément par famille
          (plus il y a de veaux morts prématurément plus la famille est au bout)
    '''
    db = get_db()

    # on crée une liste avec tous les identifiants de chaque famille
    familles = []
    allFamillesIDs = db.execute("SELECT id FROM familles").fetchall()
    allFamillesIDs = [row[0] for row in allFamillesIDs]
    # on crée une l
    for id_famille in allFamillesIDs:
        familleMembres = db.execute(
            "SELECT id, famille_id, decede FROM animaux WHERE famille_id = {}".format(id_famille)).fetchall()

        nbr_membres = len(list(familleMembres))
        total_vivants = 0
        total_morts = 0
        #on compte la proporton de vaches vivantes et de veaux morts prématurément dans chaque famille
        for membre in familleMembres:
            if membre[2] == 1:
                total_morts += 1
            else:
                total_vivants += 1

        familles.append([nbr_membres, total_vivants, total_morts, id_famille])

    familles = sorted(familles, key=lambda famille: famille[2] / famille[0])
    return familles


## Kyllian
# Extracteur de la Question 3 ou l'exercice 3.1. dans la liste (sur le site de Renaud Detry)
#
def totalveauxmortnes():
    '''
    pre:/
    post: renvoie un dictionnaire avec le nombre de veaux morts-nés par mois
    '''

    db = get_db()

    nombre_mort_nes = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 0, '08': 0, '09': 0, '10': 0,
                       '11': 0, '12': 0, }
    for ligne in db.execute(
            "SELECT animaux.id, animaux.mort_ne, velages.date from animaux INNER JOIN velages ON animaux.id = velages.id WHERE animaux.mort_ne <>'8';"):
        nombre_mort_nes[ligne[2][3:5]] += 1

    return nombre_mort_nes


# Chong
def Velage():
    '''
    pre:/
    post: renvoie un dictionnaire avec le nombre de velages par année
    '''
    db = get_db()
    data = list(db.execute("SELECT mere_id, date FROM velages"))
    dico = {}
    annee = {}
    for x in data:  # on crée 2 dictionnaires avec le nombre de velages par années
        if dico.get(x[0], None) == None:
            dico[x[0]] = 1
        else:
            dico[x[0]] += 1
        if annee.get(x[1][-4:], None) == None:
            annee[x[1][-4:]] = {dico[x[0]]: 1}

        else:
            if annee[x[1][-4:]].get(dico[x[0]], None) == None:
                annee[x[1][-4:]][dico[x[0]]] = 1
            else:
                annee[x[1][-4:]][dico[x[0]]] += 1

    for a in annee:  # on récupère les donnés pour chaque année
        for i in range(1, 8):
            if annee[a].get(i, None) == None:
                annee[a][i] = 0

    # on renvoie le dictionnaire avec les données du nombre de velages par an
    return annee

# cette fonction connecte les données récupérées à l'aide des extracteurs aux graphiques
#
@bp.route("/")
def index():
    '''
    pre:/
    post: relie les valeurs extraites des fonctions précédentes (juste au dessus) à une valeur
          qui sera associée aux graphes dans le fichier index.html
    '''

    # MAX (Graphe de la Question 1)
    PourcentageParCycle = Pourcentages()

    # CINDIE (Graphe de la Question 2)
    stats = FamillesStatistiques()
    vivantes = [famille[1] for famille in stats]
    mortes = [famille[2] for famille in stats]
    familles = [famille[3] for famille in stats]

    # KYLLIAN (Graphe de la Question 3)
    deces = list(totalveauxmortnes().values())

    # CHONG (Graphe de la Question 4)
    VelageX = []
    VelageS = []
    Annee = Velage()

    for a in Annee:
        for i in range(1, 8):
            if i == 1:
                VelageX.append("{}: {}er velage(s)".format(a, i))
            else:
                VelageX.append("{}: {}eme velage(s)".format(a, i))

    for a in Annee:
        for i in range(1, 8):
            VelageS.append(Annee[a][i])

    return render_template('index.html', PourcentageVelagePleineLune=PourcentageParCycle, mortes=mortes, vivantes=vivantes,
                           familles=familles, deces=deces, VelageX=VelageX, VelageS=VelageS)
