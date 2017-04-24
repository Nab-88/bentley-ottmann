#!/usr/bin/env python3
"""
module regroupant les fonctions permettant de manipuler
les segments vivants
"""
import sys
from geo.segment import *
from geo.tycat import *
from sortedcontainers.sortedlist import *
from math import atan

def key_vivant(segment, point):
    """
    définition de la clé qui permet de déterminer les segments vivants
    ENTREE : (segment, point)
    SORTIE : (x, angle)
    """
    y = point.coordinates[1]
    point_gauche = Point([-99999999999999, y])
    point_droit = Point([99999999999999, y])
    long_line = Segment([point_gauche, point_droit])
    #creation de la ligne permettant de déterminer les x de la clef
    point_intersection = long_line.intersection_with(segment)

    if point_intersection is None:
        x_i, y_i = None, None
        angle = None
    else:
        x_i, y_i = point_intersection.coordinates[0], point_intersection.coordinates[1]
        x_proj, y_proj = x_i, y
        angle = atan((abs(segment.endpoints[1]-y_proj))/(abs(x_proj-x_i)))

def ajouter_aux_vivants(segment_actuel, liste_vivant):
    """
    liste_vivants est de type SortedListWithKey
    """
    liste_vivant.add(segment_actuel)


def supprimer_des_vivant(segment_actuel, liste_vivant):
    """
    liste_vivants est de type SortedListWithKey
    """
    liste_vivant.remove(segment_actuel)


def initialiser_vivants():
    """
    crée une SortedListWithKey, qui contiendra la liste de tous les segments vivants
    Il faut encore trouver la clé qui permet de les classer entre eux
    La clé est un tuple (x, angle), et on classe par x croissant et ensuite pour un
    meme x par angle
    """
    liste_vivant = SortedListWithKey(key=key_vivant())

    return liste_vivant

#Louis me dit que ma key vivant marche pas car elle ne peut pas prendre 2 arguments
#il faut donc dans ma classe segment ajouter un attribut key à ma classe semgent en fonction
# d'un point et de recalculer a chaque nouvel iteration toutes les clefs des segments vivants
#et ducoup la fonction key vivant prendrai en entrée un segment et retournerai la key (x; alpha)
