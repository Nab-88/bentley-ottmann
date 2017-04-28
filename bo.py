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
import vivant as v


def test(filename):
    """
    run bentley ottmann
    """
    adjuster, segments = load_segments(filename)
    tycat(segments)
    Events = creation_evenement(segments) # sorted list with key des evenements tries
    Vivants = [] # contients les segments vivants
    current = None # le point/evenement courant
    intersections = []
    while len(Events) != 0:
        current = adjuster.hash_point(Events.pop(0))
        tycat(segments, current)
        print("Current: "+str(current))
        # Si l'evenement est un debut de segment
        if current.type == "debut":
            Vivants.append(current.segment)
            gauche, droite = voisins(current, Vivants)
            if gauche is not None:
                inters = adjuster.hash_point(current.segment.intersection_with(gauche))
                if inters is not None:
                    inters.inter.append(current.segment)
                    inters.inter.append(gauche)
                    Events.add(inters)
            if droite is not None:
                print("droite: "+str(droite))
                inters = adjuster.hash_point(current.segment.intersection_with(droite))
                if inters is not None:
                    inters.inter.append(current.segment)
                    inters.inter.append(droite)
                    Events.add(inters)
        # Si l'evenement est une fin de segment
        elif current.type == "fin":
            gauche, droite = voisins(current, Vivants)
            Vivants.remove(current.segment)
            if gauche is not None and droite is not None:
                inter = adjuster.hash_point(gauche.intersection_with(droite))
                if inter is not None:
                    if not (inter in Events):
                        inter.inter.append(gauche)
                        inter.inter.append(droite)
                        Events.add(inter)
        # Si l'evenement est une intersection
        else:
            intersections.append(current)
            current.inter[0], current.inter[1] = current.inter[1], current.inter[0]
            gauche, droite = voisins(current, Vivants)
            if gauche is not None:
                inter = adjuster.hash_point(gauche.intersection_with(current.inter[0]))
                if inter is not None:
                    if not (inter in Events):
                        inter.inter.append(gauche)
                        inter.inter.append(current.inter[0])
                        Events.add(inter)
            if droite is not None:
                inter = adjuster.hash_point(droite.intersection_with(current.inter[1]))
                if inter is not None:
                    if not (inter in Events):
                        inter.inter.append(current.inter[1])
                        inter.inter.append(droite)
                        Events.add(inter)
    print("---------------------")
    print(intersections)
    print("---------------------")
    #merci de completer et de decommenter les lignes suivantes
    #results = lancer bentley ottmann sur les segments et l'ajusteur
    # intersections = bentley_ottman(creation_evenement(segments), segments, adjuster)
    tycat(segments, intersections)
    #print("le nombre d'intersections (= le nombre de points differents) est", ...)
    #print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
    # plusieurs segments, il compte plusieurs fois) est", ...)


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
    for s in liste_segment:
        s.endpoints[0].type = "debut"
        s.endpoints[0].segment = s
        liste_des_points.append(s.endpoints[0])
        s.endpoints[1].type = "fin"
        s.endpoints[1].segment = s
        liste_des_points.append(s.endpoints[1])
    liste_events_tries = SortedListWithKey(liste_des_points, key=getYandX)
    return liste_events_tries


def chercher_intersection(vivant, liste_evenements, liste_vivants,liste_intersections, adjuster):
    """
    ENTREE: un segment, liste_evenements,
    SORTIE: les intersections entre le segment en entrée et ses deux plus proches voisins
    et si il y en a, on les ajoute à la liste des evenements, et à segment.intersection
    """
    index = liste_vivants.index(vivant)
    print('vivant', liste_vivants)
    if index != len(liste_vivants)-1 and index != 0:
        vivant_gauche = liste_vivants[index-1]
        vivant_droite = liste_vivants[index+1]
        segment = vivant.segment
        voisin_gauche = vivant_gauche.segment
        voisin_droite = vivant_droite.segment
        # PENSER À FAIRE PASSER LES DEUX NOUVEAUX POINTS DANS L'AJUSTEUR
        intersection_gauche = segment.intersection_with(voisin_gauche)

        if intersection_gauche is not None:
            intersection_gauche = adjuster.hash_point(intersection_gauche)
            if intersection_gauche not in liste_evenements:
                liste_evenements.add(intersection_gauche)
                liste_intersections.append(intersection_gauche)
        intersection_droite = segment.intersection_with(voisin_droite)

        if intersection_droite is not None:
            intersection_droite = adjuster.hash_point(intersection_droite)
            if intersection_droite not in liste_evenements:
                liste_evenements.add(intersection_droite)
                liste_intersections.append(intersection_droite)
    elif index == 0 and len(liste_vivants) != 1:
        vivant_droite = liste_vivants[index+1]
        segment = vivant.segment
        voisin_droite = vivant_droite.segment
        intersection_droite = segment.intersection_with(voisin_droite)

        if intersection_droite is not None:
            intersection_droite = adjuster.hash_point(intersection_droite)
            #intersection_droite.type = "intersection"
            if intersection_droite not in liste_evenements:
                liste_evenements.add(intersection_droite)
                liste_intersections.append(intersection_droite)
            segment.intersections.append(intersection_droite)
            voisin_droite.intersections.append(intersection_droite)
    elif index == len(liste_vivants)-1 and len(liste_vivants) != 1:
        vivant_gauche = liste_vivants[index-1]
        # PENSER À FAIRE PASSER LES DEUX NOUVEAUX POINTS DANS L'AJUSTEUR
        segment = vivant.segment
        voisin_gauche = vivant_gauche.segment
        intersection_gauche = segment.intersection_with(voisin_gauche)

        if intersection_gauche is not None:
            intersection_gauche = adjuster.hash_point(intersection_gauche)
            if intersection_gauche not in liste_evenements:
                liste_evenements.add(intersection_gauche)
                liste_intersections.append(intersection_gauche)
            segment.intersections.append(intersection_gauche)
            voisin_gauche.intersections.append(intersection_gauche)


def chercher_intersection_entre_voisin(vivant, liste_evenements, liste_vivants, liste_intersections, adjuster):
    """
    ENTREE: un segment
    SORTIE: les intersections entre les deux plus proches voisins du segment
    MAIS SANS LUI, car on fait comme si on l'avait enlevé.
    et si il y en a, on les ajoute à la liste des evenements, et à segment.intersection
    """
    print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
    index = liste_vivants.index(vivant)

    #Rajouter des tests pour pas avoir un index list out of range
    if index != len(liste_vivants)-1 and index != 0:
        vivant_gauche = liste_vivants[index-1]
        vivant_droite = liste_vivants[index+1]
        ##
        voisin_gauche = vivant_gauche.segment
        voisin_droite = vivant_droite.segment
        intersection = voisin_gauche.intersection_with(voisin_droite)

        if intersection is not None:
            intersection = adjuster.hash_point(intersection)
            liste_evenements.add(intersection)
            voisin_gauche.intersections.append(intersection)
            voisin_droite.intersections.append(intersection)
            liste_intersections.append(intersection)


def est_un_debut(point_actuel):
    """
    renvoie true si le point_actuel est un début de segment
    """
    if point_actuel.debut is not None:
        return True
    else:
        return False


def est_une_fin(point_actuel):
    """
    renvoie true si le point_actuel est une fin de segment
    """
    if point_actuel.fin is not None:
        return True
    else:
        return False


def segment_actuels(point_actuel, liste_de_tous_les_segments, adjuster):
    """
    renvoie la liste des segments dont le point_actuel fait partie
    """
    segment_actuels = []
    for s in liste_de_tous_les_segments:
        if s.contains(point_actuel):
            segment_actuels.append(s)
            if point_actuel == s.endpoints[0]:
                point_actuel.debut.append(s)
            elif point_actuel == s.endpoints[1]:
                point_actuel.fin.append(s)
            else:
                point_actuel.milieu.append(s)
    return segment_actuels


def bentley_ottman(liste_evenements, liste_segments, adjuster):
    """
    Cette fonction implémente l'algorithme de Bentley_ottman
    En entrée la liste des segments et des evenements sont triées
    """
    liste_intersections = []
    segments_vivants = v.initialiser_vivants()
    point_courant = None
    segments_courants = []
    while len(liste_evenements) != 0:
        point_courant = liste_evenements.pop(0)
        tycat(liste_segments, point_courant)
        print('=======nouvelle iteration======')
        segments_courants = segment_actuels(point_courant, liste_segments, adjuster)
        v.mise_a_jour_key(segments_vivants, point_courant)
        if est_un_debut(point_courant):
            for segment in segments_courants:
                clef = v.key_vivant(segment, point_courant)
                vivant = v.Vivant(segment, clef)
                v.ajouter_aux_vivants(vivant, segments_vivants)
            for vivant in segments_vivants:
                # on reparcourt la liste des segments courant et on compare avec leur voisin
                # de gauche et droite
                # on est obligé de de le faire une fois apres les avoir tous ajoutés aux vivants
                # sinon on risque d'en louper
                print('liste_evenements', liste_evenements)
                chercher_intersection(vivant, liste_evenements, segments_vivants, liste_intersections, adjuster)
                #on regarde si le segment actuel intersecte avec ses deux plus proches voisins et si
                #oui on ajoute l'intersection a la liste des evenements
        elif est_une_fin(point_courant):
            #FAUX ! il faut faire un for segment in segments_courants
            #mais je vois pas comment le faire sans que ça bug ... avec ma classe vivant
            for segment in segments_courants:
                for vivant in segments_vivants:
                    if segment == vivant.segment:
                        chercher_intersection_entre_voisin(vivant, liste_evenements, segments_vivants, liste_intersections, adjuster)
                #on regarde si il existe des intersections entre les voisins de gauche et droite
                #du segment qu'on va enlever
                        v.supprimer_des_vivant(vivant, segments_vivants)
                #on enleve tous les segments du point_courant des vivants
        print('liste_intersection=', liste_intersections)
    return liste_intersections


def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

main()
