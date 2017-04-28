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
from geo.point import Point
from geo.segment import Segment, load_segments
from geo.tycat import tycat
from sortedcontainers.sortedlist import SortedListWithKey


def test(filename):
    """
    run bentley ottmann
    """
    adjuster, segments = load_segments(filename)
    tycat(segments)
    Events = creation_evenement(segments)  # sorted list with key des evenements tries
    Vivants = []  # contients les segments vivants
    current = None  # le point/evenement courant
    intersections = []
    while len(Events) != 0:
        current = adjuster.hash_point(Events.pop(0))
        # tycat(segments, current)
        # Si l'evenement est un debut de segment
        if current.type == "debut":
            Vivants.append(current.segment)
            gauche, droite = voisins(current, Vivants)
            if gauche is not None:
                if current.segment.intersection_with(gauche) is not None:
                    inters = adjuster.hash_point(current.segment.intersection_with(gauche))
                    if (not (inters in Events)) and pas_une_extremite(inters, segments):
                        inters.segment = current.segment
                        inters.inter.append(current.segment)
                        inters.inter.append(gauche)
                        Events.add(inters)
                        # ajout de l'intersection pour l'autre segment
                        inters.segment = gauche
                        inters.inter[0], inters.inter[1] = inters.inter[1], inters.inter[0]
                        Events.add(inters)
            if droite is not None:
                if current.segment.intersection_with(droite) is not None:
                    inters = adjuster.hash_point(current.segment.intersection_with(droite))
                    if (not (inters in Events)) and pas_une_extremite(inters, segments):
                        inters.segment = current.segment
                        inters.inter.append(current.segment)
                        inters.inter.append(droite)
                        Events.add(inters)
                        # 2e
                        inters.segment = droite
                        inters.inter[0], inters.inter[1] = inters.inter[1], inters.inter[0]
                        Events.add(inters)
        # Si l'evenement est une fin de segment
        elif current.type == "fin":
            gauche, droite = voisins(current, Vivants)
            Vivants.remove(current.segment)
            if gauche is not None and droite is not None:
                if gauche.intersection_with(droite) is not None:
                    inter = adjuster.hash_point(gauche.intersection_with(droite))
                    if (not (inter in Events)) and pas_une_extremite(inter, segments):
                        inter.segment = gauche
                        inter.inter.append(gauche)
                        inter.inter.append(droite)
                        Events.add(inter)
                        # 2e
                        inter.segment = droite
                        inter.inter[0], inter.inter[1] = inter.inter[1], inter.inter[0]
                        Events.add(inter)
        # Si l'evenement est une intersection
        else:
            intersections.append(current)
            current.inter[0], current.inter[1] = current.inter[1], current.inter[0]
            current.segment = current.inter[0]
            gauche, droite = voisins(current, Vivants)
            if gauche is not None:
                if gauche.intersection_with(current.inter[0]) is not None:
                    inter = adjuster.hash_point(gauche.intersection_with(current.inter[0]))
                    if not (inter in Events):
                        if pas_une_extremite(inter, segments):
                            inter.segment = gauche
                            inter.inter.append(gauche)
                            inter.inter.append(current.inter[0])
                            Events.add(inter)
                            # 2e
                            inter.segment = current.inter[0]
                            inter.inter[0], inter.inter[1] = inter.inter[1], inter.inter[0]
                            Events.add(inter)
            if droite is not None:
                if droite.intersection_with(current.inter[1]) is not None:
                    inter = adjuster.hash_point(droite.intersection_with(current.inter[1]))
                    if not (inter in Events):
                        if pas_une_extremite(inter, segments):
                            inter.segment = current.inter[1]
                            inter.inter.append(current.inter[1])
                            inter.inter.append(droite)
                            Events.add(inter)
                            # 2e
                            inter.segment = droite
                            inter.inter[0], inter.inter[1] = inter.inter[1], inter.inter[0]
                            Events.add(inter)
    intersections = list(set(intersections))
    tycat(segments, intersections)
    print("le nombre d'intersections (= le nombre de points differents) est : ", len(intersections))
    # print("le nombre de coupes dans les segments (si un point d'intersection apparait dans plusieurs segments, il compte plusieurs fois) est : ", len(intersections)+decalage)


def pas_une_extremite(point, segments):
    """
    renvoie True si le point ne correspond a aucune extremite de segment
    renvoie False sinon
    """
    for seg in segments:
        if seg.endpoints[0] == point:
            return False
        if seg.endpoints[1] == point:
            return False
    return True


def voisins(point, segments):
    """
    renvoie le segment de gauche et celui de droite par rapport au point donné
    (si ils existent sinon renvoie None)
    """
    x = point.coordinates[0]
    y = point.coordinates[1]
    ligne_balayage = Segment([Point([-999999999, y]), Point([999999999, y])])
    segments_pris_en_compte = []
    # On veut la liste triee des segments balayés
    for seg in segments:
        if seg.contains(point):
            continue
        intersection = ligne_balayage.intersection_with(seg)
        if intersection is not None:
            seg.key = intersection.coordinates[0]
            segments_pris_en_compte.append(seg)
    if len(segments_pris_en_compte) == 0:
        return None, None
    elif len(segments_pris_en_compte) == 1:
        if segments_pris_en_compte[0].key <= x:
            return segments_pris_en_compte[0], None
        else:
            return None, segments_pris_en_compte[0]
    else:
        segments_pris_en_compte.sort(key=lambda x: x.key)
        index = 0
        # On cherche l'index des voisins de x
        if x <= segments_pris_en_compte[0].key:
            return None, segments_pris_en_compte[0]
        elif x >= segments_pris_en_compte[-1].key:
            return segments_pris_en_compte[-1], None
        else:
            for i in range(len(segments_pris_en_compte)-1):
                if (segments_pris_en_compte[i].key <= x) and (x <= segments_pris_en_compte[i+1].key):
                    index = i
                    break
            # On retourne les voisins
            return segments_pris_en_compte[index], segments_pris_en_compte[index+1]


def getYandX(item):
    """
    fonction utilisé pour récupérer le Y du point pour la fonction sorted()
    """
    return(item.coordinates[1], item.coordinates[0])


def creation_evenement(liste_segment):
    """
    Grâce aux SortedContainers
    ENTRÉE : Une liste de segment de la forme [Segment(Point1, Point2), ....,
    Segment(Point1, Point2)]
    SORTIE : Une liste des points triés par "ordre croissant de balayage",
    représentant l'ensemble E des évenements à parcourir.
    En plus on rajoute le type du point, si c'est un début ou un fin.
    """
    liste_des_points = []
    debut = None
    fin = None
    for s in liste_segment:
        # determiner le debut et la fin
        if s.endpoints[0].coordinates[1] < s.endpoints[1].coordinates[1]:
            debut, fin = s.endpoints[0], s.endpoints[1]
        elif s.endpoints[0].coordinates[1] > s.endpoints[1].coordinates[1]:
            debut, fin = s.endpoints[1], s.endpoints[0]
        else:
            if s.endpoints[0].coordinates[0] < s.endpoints[1].coordinates[0]:
                debut, fin = s.endpoints[0], s.endpoints[1]
            else:
                debut, fin = s.endpoints[1], s.endpoints[0]
        # affecter les attributs et ajouter a la liste triee
        debut.type = "debut"
        debut.segment = s
        liste_des_points.append(debut)
        fin.type = "fin"
        fin.segment = s
        liste_des_points.append(fin)
    liste_events_tries = SortedListWithKey(liste_des_points, key=getYandX)
    return liste_events_tries


def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

if __name__ == '__main__':
    main()
