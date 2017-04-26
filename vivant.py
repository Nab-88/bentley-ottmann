#!/usr/bin/env python3
"""
module regroupant les fonctions permettant de manipuler
les segments vivants
"""
import sys
from geo.segment import Segment
from geo.point import Point
from geo.tycat import Displayer
from sortedcontainers.sortedlist import SortedListWithKey
from math import atan, pi

class Vivant:
    """
    """
    def __init__(self, segment, key):
        self.segment = segment
        self.key = key
        self.endpoints = segment.endpoints
    def __str__(self):
        return "Vivant([" + str(self.segment) + ', key :' + str(self.key)+ "])"

def creation_vivant(segment, key):
    """
    """
    return Vivant(segment, key)

def mise_a_jour_key(liste_vivant, point_actuel):
    """
    Recalcule toutes les clefs des segments vivants par rapport au
    nouveau point actuel et met à jour l'attribut .key du segment vivant
    """
    for vivant in liste_vivant:
        key_vivant(vivant.segment, point_actuel)



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
        if x_proj == x_i and segment.endpoints[1].coordinates[1] > 0:
            angle = pi/2
        elif x_proj == x_i and segment.endpoints[1].coordinates[1] <= 0:
            angle = - pi/2
        else:
            angle = atan((segment.endpoints[1].coordinates[1]-y_proj)/(x_proj-x_i))
    x_key = x_i
    key_actuelle = (x_key, angle)
    #On met à jour la clé du segment
    segment.key = key_actuelle
    return(key_actuelle)

def ajouter_aux_vivants(segment_actuel, liste_vivant):
    """
    liste_vivants est de type SortedListWithKey
    """
    liste_vivant.add(segment_actuel)
    print('le segment actuel ajouté aux vivants est', segment_actuel)


def supprimer_des_vivant(segment_actuel, liste_vivant):
    """
    liste_vivants est de type SortedListWithKey
    """
    liste_vivant.remove(segment_actuel)

def attribut_key(vivant):
    """
    renvoie la key d'un vivant
    """
    return vivant.key


def initialiser_vivants():
    """
    crée une SortedListWithKey, qui contiendra la liste de tous les segments vivants
    Il faut encore trouver la clé qui permet de les classer entre eux
    La clé est un tuple (x, angle), et on classe par x croissant et ensuite pour un
    meme x par angle
    """
    liste_vivant = SortedListWithKey(key=attribut_key)
    return liste_vivant

#Louis me dit que ma key vivant marche pas car elle ne peut pas prendre 2 arguments
#il faut donc dans ma classe segment ajouter un attribut key à ma classe semgent en fonction
# d'un point et de recalculer a chaque nouvel iteration toutes les clefs des segments vivants
#et ducoup la fonction key vivant prendrai en entrée un segment et retournerai la key (x; alpha)
