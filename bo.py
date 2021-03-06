#!/usr/bin/env python3
"""
this tests bentley ottmann on given .bo files.
for each file:
    - we display segments
    - run bentley ottmann
    - display results
    - print some statistics
"""
import time
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
    Events = creation_evenement(segments, adjuster)  # sorted list with key des evenements tries
    Vivants = []  # contients les segments vivants
    current = None  # le point/evenement courant
    intersections = [] # contient les intersections
    while len(Events) != 0:
        current = adjuster.hash_point(Events.pop(0))
        a_enlever = [] # va servir a considerer TOUS les voisins(intersection)
        # Si l'evenement est un debut de segment
        if current.type == "debut":
            # on demarre le segment
            Vivants.append(current.segment)
            # on cherche les voisins
            gauche, droite, nb_g, nb_d = voisins(current, Vivants, a_enlever)
            # on traite tous les voisins: il y en a plusieurs lorsque
            # le voisin appartient a plusieurs segments
            for _ in range(nb_g):
                if gauche is not None:
                    if current.segment.intersection_with(gauche) is not None:
                        inters = adjuster.hash_point(current.segment.intersection_with(gauche))
                        if (not (inters in Events)) and pas_une_extremite(inters, segments):
                            if inters.coordinates[1] >= current.coordinates[1]:
                                inters.segment = current.segment
                                inters.inter.append(current.segment)
                                inters.inter.append(gauche)
                                Events.add(inters)
                                # ajout de l'intersection pour l'autre segment
                                inters.segment = gauche
                                inters.inter[0], inters.inter[1] = inters.inter[1], inters.inter[0]
                                Events.add(inters)
                    a_enlever.append(gauche)
                    gauche, droite, tmp1, tmp2 = voisins(current, Vivants, a_enlever)
            for _ in range(nb_d):
                if droite is not None:
                    if current.segment.intersection_with(droite) is not None:
                        inters = adjuster.hash_point(current.segment.intersection_with(droite))
                        if (not (inters in Events)) and pas_une_extremite(inters, segments):
                            if inters.coordinates[1] >= current.coordinates[1]:
                                inters.segment = current.segment
                                inters.inter.append(current.segment)
                                inters.inter.append(droite)
                                Events.add(inters)
                                # ajout de l'intersection pour l'autre segment
                                inters.segment = droite
                                inters.inter[0], inters.inter[1] = inters.inter[1], inters.inter[0]
                                Events.add(inters)
                    a_enlever.append(droite)
                    gauche, droite, tmp1, tmp2 = voisins(current, Vivants, a_enlever)
        # Si l'evenement est une fin de segment
        elif current.type == "fin":
            # on cherche les voisins avant de terminer le segment
            gauche, droite, nb_g, nb_d = voisins(current, Vivants, a_enlever)
            Vivants.remove(current.segment)
            # on considere tous les voisins
            for _ in range(min(nb_g, nb_d)):
                if gauche is not None and droite is not None:
                    if gauche.intersection_with(droite) is not None:
                        inter = adjuster.hash_point(gauche.intersection_with(droite))
                        if (not (inter in Events)) and pas_une_extremite(inter, segments):
                            if inter.coordinates[1] >= current.coordinates[1]:
                                inter.segment = gauche
                                inter.inter.append(gauche)
                                inter.inter.append(droite)
                                Events.add(inter)
                                # ajout pour l'autre segment
                                inter.segment = droite
                                inter.inter[0], inter.inter[1] = inter.inter[1], inter.inter[0]
                                Events.add(inter)
                    a_enlever.append(droite)
                    a_enlever.append(gauche)
                    gauche, droite, tmp1, tmp2 = voisins(current, Vivants, a_enlever)
        # Si l'evenement est une intersection
        else:
            intersections.append(current)
            # on considere les "bons" segments pour les intersections avec
            # les voisins
            current.inter[0], current.inter[1] = current.inter[1], current.inter[0]
            current.segment = current.inter[0]
            gauche, droite, nb_g, nb_d = voisins(current, Vivants, a_enlever)
            # on considere tous les voisins
            for _ in range(nb_g):
                if gauche is not None:
                    if gauche.intersection_with(current.inter[0]) is not None:
                        inter = adjuster.hash_point(gauche.intersection_with(current.inter[0]))
                        if not (inter in Events):
                            if pas_une_extremite(inter, segments):
                                if inter.coordinates[1] >= current.coordinates[1]:
                                    inter.segment = gauche
                                    inter.inter.append(gauche)
                                    inter.inter.append(current.inter[0])
                                    Events.add(inter)
                                    # ajout pour l'autre segment
                                    inter.segment = current.inter[0]
                                    inter.inter[0], inter.inter[1] = inter.inter[1], inter.inter[0]
                                    Events.add(inter)
                    a_enlever.append(gauche)
                    gauche, droite, tmp1, tmp2 = voisins(current, Vivants, a_enlever)
            for _ in range(nb_d):
                if droite is not None:
                    if droite.intersection_with(current.inter[1]) is not None:
                        inter = adjuster.hash_point(droite.intersection_with(current.inter[1]))
                        if not (inter in Events):
                            if pas_une_extremite(inter, segments):
                                if inter.coordinates[1] >= current.coordinates[1]:
                                    inter.segment = current.inter[1]
                                    inter.inter.append(current.inter[1])
                                    inter.inter.append(droite)
                                    Events.add(inter)
                                    # ajout pour l'autre segment
                                    inter.segment = droite
                                    inter.inter[0], inter.inter[1] = inter.inter[1], inter.inter[0]
                                    Events.add(inter)
                    a_enlever.append(droite)
                    gauche, droite, tmp1, tmp2 = voisins(current, Vivants, a_enlever)
    intersections = list(set(intersections))
    tycat(segments, intersections)
    print("le nombre d'intersections (= le nombre de points differents) est : ", len(intersections))
    return intersections
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


def voisins(point, segments, a_enlever):
    """
    renvoie le segment de gauche et celui de droite par rapport au point donné
    (si ils existent sinon renvoie None)
    """
    x = point.coordinates[0]
    y = point.coordinates[1]
    ligne_balayage = Segment([Point([-999999, y]), Point([999999, y])])
    segments_pris_en_compte = []
    nb_gauche = 0
    nb_droite = 0
    # On veut la liste triee des segments balayés sauf ceux de a_enlever
    # et celui du point considere
    for seg in segments:
        if len(a_enlever) != 0:
            if seg in a_enlever:
                continue
        if seg.contains(point):
            continue
        intersection = ligne_balayage.intersection_with(seg)
        if intersection is not None:
            seg.key = intersection.coordinates[0]
            segments_pris_en_compte.append(seg)
    # on va determiner les voisins et leur nombre
    # Si il n'y a pas de voisin
    if len(segments_pris_en_compte) == 0:
        return None, None, nb_gauche, nb_droite
    # Si il y en a un seul
    elif len(segments_pris_en_compte) == 1:
        if segments_pris_en_compte[0].key <= x:
            nb_gauche += 1
            return segments_pris_en_compte[0], None, nb_gauche, nb_droite
        else:
            nb_droite += 1
            return None, segments_pris_en_compte[0], nb_gauche, nb_droite
    # si il y en a plusieurs
    else:
        # on les trie en fonction de la cle 'abscisse'
        segments_pris_en_compte.sort(key=lambda x: x.key)
        index = 0
        # On cherche l'index des voisins de x
        # si le segment actuel est le plus a gauche
        if x <= segments_pris_en_compte[0].key:
            segm = segments_pris_en_compte[0]
            nb_droite += 1
            for i in range(1, len(segments_pris_en_compte)):
                if segm.key == segments_pris_en_compte[i].key:
                    nb_droite += 1
                if segments_pris_en_compte[i].key != segm.key:
                    break
            return None, segments_pris_en_compte[0], nb_gauche, nb_droite
        # si le segment actuel est le plus a droite
        elif x >= segments_pris_en_compte[-1].key:
            segm = segments_pris_en_compte[-1]
            nb_gauche += 1
            for i in range(len(segments_pris_en_compte) - 2, -1, -1):
                if segments_pris_en_compte[i].key == segm.key:
                    nb_gauche += 1
                if segments_pris_en_compte[i].key != segm.key:
                    break
            return segments_pris_en_compte[-1], None, nb_gauche, nb_droite
        # si le segment actuel est quelque part au milieu
        else:
            for i in range(len(segments_pris_en_compte)-1):
                if (segments_pris_en_compte[i].key <= x) and (x <= segments_pris_en_compte[i+1].key):
                    index = i
                    break
            segm_g = segments_pris_en_compte[index]
            segm_d = segments_pris_en_compte[index+1]
            nb_gauche += 1
            nb_droite += 1
            for i in range(index-1, -1, -1):
                if segments_pris_en_compte[i].key == segm_g.key:
                    nb_gauche += 1
                if segments_pris_en_compte[i].key != segm_g.key:
                    break
            for i in range(index+1, len(segments_pris_en_compte)):
                if segments_pris_en_compte[i].key == segm_d.key:
                    nb_droite += 1
                if segments_pris_en_compte[i].key != segm_d.key:
                    break
            return segments_pris_en_compte[index], segments_pris_en_compte[index+1], nb_gauche, nb_droite


def getYandX(item):
    """
    fonction utilisé pour récupérer le Y et le X du point
    """
    return(item.coordinates[1], item.coordinates[0])


def creation_evenement(liste_segment, adjuster):
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
            debut, fin = adjuster.hash_point(s.endpoints[0]), adjuster.hash_point(s.endpoints[1])
        elif s.endpoints[0].coordinates[1] > s.endpoints[1].coordinates[1]:
            debut, fin = adjuster.hash_point(s.endpoints[1]), adjuster.hash_point(s.endpoints[0])
        else:
            if s.endpoints[0].coordinates[0] < s.endpoints[1].coordinates[0]:
                debut, fin = adjuster.hash_point(s.endpoints[0]), adjuster.hash_point(s.endpoints[1])
            else:
                debut, fin = adjuster.hash_point(s.endpoints[1]), adjuster.hash_point(s.endpoints[0])
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
    temps = []
    liste_inter = []
    for filename in sys.argv[1:]:
        print("Pour le test ", filename)
        debut = time.time()
        intersections = test(filename)
        liste_inter.append(len(intersections))
        tps = time.time() - debut
        temps.append(tps)
        print("Temps d'exécution: ", tps, " s")
        print("-----------------------------")
    print("==============================================")
    print("Voici les nb d'intersections respectifs: ", liste_inter)
    print("Voici les temps respectifs: ", temps)


if __name__ == '__main__':
    main()
