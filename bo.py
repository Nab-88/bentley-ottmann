#!/usr/bin/env python3
"""
this tests bentley ottmann on given .bo files.
for each file:
    - we display segments
    - run bentley ottmann
    - display results
    - print some statistics
"""
import sys
from geo.segment import *
from geo.tycat import *
from sortedcontainers.sortedlist import *

def test(filename):
    """
    run bentley ottmann
    """
    adjuster, segments = load_segments(filename)
    tycat(segments)
    #TODO: merci de completer et de decommenter les lignes suivantes
    #results = lancer bentley ottmann sur les segments et l'ajusteur
    #...
    #tycat(segments, intersections)
    #print("le nombre d'intersections (= le nombre de points differents) est", ...)
    #print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
    # plusieurs segments, il compte plusieurs fois) est", ...)


def getYandX(item):
    """
    fonction utilisé pour récupérer le Y du point pour la fonction sorted()
    """
    return(item.coordinates[1], item.coordinates[0])

def getX(item):
    """
    fonction utilisé pour récupérer le X du point pour la fonction sorted()
    """
    return(item.endpoints.coordinates[0])

# def create_event(liste_des_segments):
#     """
#     ENTRÉE : Une liste de segment de la forme [Segment(Point1, Point2), ...., Segment(Point1, Point2)]
#     SORTIE : Une liste des points triés par "ordre croissant de balayage",
#     représentant l'ensemble E des évenements à parcourir.
#     """
#     liste_event_non_triee = []
#     for s in liste_des_segments:
#         for p in s.endpoints:
#             liste_event_non_triee.append(p)
#     ## Pour l'instant la liste des évenements n'est pas triée.
#     liste_event_triee = sorted(liste_event_non_triee, key=getY)
#     # on vient de trier la liste en fonction des Y croissants
#     # mais il reste encore a trier la liste pour un meme Y
#     # avoir comment on le fait.
#     liste_vraiment_triee = []
#     ##on va mettre dans cette liste la liste triée par Y croissant, puis pour des mêmes
#     ##Y par x croissant
#     a = []
#     a.append(liste_event_triee[0])
#     for p in liste_event_triee:
#         if getY(p) == getY(a[0]):
#             a.append(p)
#             ## on rassemble au sein d'une meme liste les points avec le meme Y
#         elif getY(p) != getY(a[0]):
#             ## si les points n'ont plus le même Y
#             b = sorted(a, key=getX)
#             ## on classe la sous_liste de même Y en fonction de leur X croissant
#             for point in b:
#                 liste_vraiment_triee.append(point)
#             ## on ajoute cette sous-liste a la liste vraiment triée
#             a = [p]
#             ## on recomence une nouvelle sous-liste de point de meme Y
#
#
#     return(liste_vraiment_triee)

def creation_evenement(liste_segment):
    """
    Grâce aux SortedContainers
    ENTRÉE : Une liste de segment de la forme [Segment(Point1, Point2), ...., Segment(Point1, Point2)]
    SORTIE : Une liste des points triés par "ordre croissant de balayage",
    représentant l'ensemble E des évenements à parcourir.
    En plus on rajoute le type du point, si c'est un début ou un fin.
    """
    liste_des_points = []
    for s in liste_segment:
        s.endpoints[0].type = "debut"
        liste_des_points.append(s.endpoints[0])
        s.endpoints[1].type = "fin"
        liste_des_points.append(s.endpoints[1])
    liste_event_tries = SortedListWithKey(liste_des_points, key=getYandX)
    return(liste_event_tries)

def detecter_voisin():
    """
    ENTREE: un segment
    SORTIE: la liste des segments voisins
    """
    #TODO


def chercher_intersections(segment, liste_evenements, liste_vivants):
    """
    ENTREE: un segment, liste_evenements,
    SORTIE: les intersections entre le segment en entrée et ses deux plus proches voisins
    et si il y en a, on les ajoute à la liste des evenements, et à segment.intersection
    """
    index_du_segment = liste_vivants.index(segment)
    #Rajouter des tests pour pas avoir un index list out of range
    voisin_gauche = liste_vivants[index-1]
    voisin_droite = liste_vivants[index+1]
    ##
    intersection_gauche = segment.intersection_with(voisin_gauche)
    liste_evenements.add(intersection_gauche)
    segment.intersections.append(intersection_gauche)
    voisin_gauche.intersections.append(intersection_gauche)
    ##
    intersection_droite = segment.intersection_with(voisin_droite)
    liste_evenements.add(intersection_droite)
    segment.intersections.append(intersection_droite)
    voisin_droite.intersections.append(intersection_droite)
    ##



def chercher_intersection_entre_voisin(segment, liste_evenements):
    """
    ENTREE: un segment
    SORTIE: les intersections entre les deux plus proches voisins du segment
    MAIS SANS LUI, car on fait comme si on l'avait enlevé.
    et si il y en a, on les ajoute à la liste des evenements, et à segment.intersection
    """
    index_du_segment = liste_vivants.index(segment)
    #Rajouter des tests pour pas avoir un index list out of range
    voisin_gauche = liste_vivants[index-1]
    voisin_droite = liste_vivants[index+1]
    ##
    intersection = voisin_gauche.intersection_with(voisin_droite)
    liste_evenements.add(intersection)
    voisin_gauche.intersections.append(intersection)
    voisin_droite.intersections.append(intersection)


def est_un_debut(point_actuel):
    """"
    renvoie true si le point_actuel est un début de segment
    """"
    if point_actuel.type == 'debut':
        return(True)
    else:
        return(False)

def est_une_fin(point_actuel):
    """"
    renvoie true si le point_actuel est une fin de segment
    """"
    if point_actuel.type == 'fin':
        return(True)
    else:
        return(False)

def supprimer_evenement_actuel(liste_evenements):
    """"

    """"
    #TODO

def passer_evenement_suivant(liste_evenements, liste_finale):
    """
    supprime l'évenement actuel (le premier) de la liste des evenements, l'ajoute
    à la liste finale des points traités
    et renvoie le nouveau_premier point de la liste des evenements
    """"
    #TODO


def segment_actuels(point_actuel):
    """"
    renvoie la liste des segments dont le point_actuel fait partie
    """"
    #TODO


def bentley_ottman(liste_evenements, liste_segments):
    """"
    Cette fonction implémente l'algorithme de Bentley_ottman
    En entrée la liste des segments et des evenements sont triées
    """"
    #-----ATTENTION----
    #Dans la version ci dessous de l'algorithme
    #J'ai décidé d'ajouter et d'enlever à chaque fois tous les segments qui contenaient le point_courant
    #Il faudrait peut etre ajouter/enlever seulement le (ou les) segment(s) dont cest le debut/ou la fin
    #A REFLECHIR ...
    liste_finale = []
    #cette liste va contenir tous les points traités
    #et cest cette liste qu'on va retourner et afficher
    point_courant=liste_evenements[0]
    segments_vivants = initialiser_vivants()
    while len(liste_evenements) !=0:
        segments_courants = segment_actuels(point_courant)
        #liste de tous les segments dont le point_courant fait partie
        if est_un_debut(point_courant):
            #si point est un début de segment
            for segment in segments_courants:
                ajouter_aux_vivants(segment)
                #on ajoute tous les segments du point_courant aux vivants
            for segment in segments_courants:
                #on reparcourt la liste des segments courant et on compare avec leur voisin
                #de gauche et droite
                #on est obligé de de le faire une fois apres les avoir tous ajoutés aux vivants
                #sinon on risque d'en louper
                chercher_intersection(segment, liste_evenements)
                #on regarde si le segment actuel intersecte avec ses deux plus proches voisins et si
                #oui on ajoute l'intersection a la liste des evenements
        elif est_une_fin(point_courant):
            #si point est une fin de segment
            for segment in segments_courants:
                chercher_intersection_entre_voisin(segment)
                #on regarde si il existe des intersections entre les voisins de gauche et droite
                #du segment qu'on va enlever
                supprimer_des_vivants(segment)
                #on enleve tous les segments du point_courant des vivants
        point_courant = passer_evenement_suivant(liste_des_evenements, liste_finale)
    return(liste_finale)







def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)


main()
