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


def getY(item):
    """
    fonction utilisé pour récupérer le Y du point pour la fonction sorted()
    """
    return(item.coordinates[1])

def getX(item):
    """
    fonction utilisé pour récupérer le X du point pour la fonction sorted()
    """
    return(item.coordinates[0])

def create_event(liste_des_segments):
    """
    ENTRÉE : Une liste de segment de la forme [Segment(Point1, Point2), ...., Segment(Point1, Point2)]
    SORTIE : Une liste des points triés par "ordre croissant de balayage",
    représentant l'ensemble E des évenements à parcourir.
    """
    liste_event_non_triee = []
    for s in liste_des_segments:
        for p in s.endpoints:
            liste_event_non_triee.append(p)
    ## Pour l'instant la liste des évenements n'est pas triée.
    liste_event_triee = sorted(liste_event_non_triee, key=getY)
    # on vient de trier la liste en fonction des Y croissants
    # mais il reste encore a trier la liste pour un meme Y
    # avoir comment on le fait.
    liste_vraiment_triee = []
    ##on va mettre dans cette liste la liste triée par Y croissant, puis pour des mêmes
    ##Y par x croissant
    a = []
    a.append(liste_event_triee[0])
    for p in liste_event_triee:
        if getY(p) == getY(a[0]):
            a.append(p)
            ## on rassemble au sein d'une meme liste les points avec le meme Y
        elif getY(p) != getY(a[0]):
            ## si les points n'ont plus le même Y
            b = sorted(a, key=getX)
            ## on classe la sous_liste de même Y en fonction de leur X croissant
            for point in b:
                liste_vraiment_triee.append(point)
            ## on ajoute cette sous-liste a la liste vraiment triée
            a = [p]
            ## on recomence une nouvelle sous-liste de point de meme Y


    return(liste_vraiment_triee)

def search_voisin():
    """
    Pour chaque point
    """

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

main()
