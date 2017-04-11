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
    return(liste_event_triee)







def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

main()
