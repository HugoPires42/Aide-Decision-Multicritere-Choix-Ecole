# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SIMULATEUR AMD v2.0 — Aide Multicritère à la Décision                     ║
║  50 Écoles d'Ingénieurs Françaises                                         ║
║  M1 MIAGE — Semestre 2 — Décision Multicritère                             ║
║                                                                            ║
║  Méthodes implémentées :                                                   ║
║    1. Somme Pondérée (normalisation min-max [0;100])                       ║
║    2. Opérateur OWA (Yager)                                                ║
║    3. Intégrale de Choquet (modèle 2-additif de Grabisch)                  ║
║    4. Méthode du Min (Maximin / Wald)                                      ║
║    5. ELECTRE Is (surclassement avec vetos)                                ║
║                                                                            ║
║  Critères :                                                                ║
║    g1 = Salaire moyen à la sortie (€/an)       → à MAXIMISER               ║
║    g2 = Taux d'emploi à 6 mois (%)             → à MAXIMISER               ║
║    g3 = Coût total sur 3 ans (€)               → à MINIMISER               ║
║    g4 = Diversité sociale (%)                   → à MAXIMISER               ║
║    g5 = Engagement DD&RS (note sur 5)           → à MAXIMISER               ║
║    g6 = Vie associative (note sur 10)           → à MAXIMISER               ║
║                                                                            ║
║  Interface : Style RATP / Métro Parisien (sobre, clair, institutionnel)    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
import math

# =============================================================================
# ███████████████████████████████████████████████████████████████████████████████
# █  SECTION 1 : BASE DE DONNÉES — 50 ÉCOLES D'INGÉNIEURS FRANÇAISES         █
# ███████████████████████████████████████████████████████████████████████████████
# =============================================================================
# Format : "Nom de l'école" : [g1, g2, g3, g4, g5, g6]
#   g1 : Salaire moyen à la sortie (€/an)        [35000 – 60000]
#   g2 : Taux d'emploi à 6 mois (%)              [85 – 100]
#   g3 : Coût total sur 3 ans (€)                [0 – 15000]
#   g4 : Diversité sociale (%)                    [5 – 40]
#   g5 : Engagement DD&RS (note sur 5)            [1.0 – 5.0]
#   g6 : Vie associative (note sur 10)            [1.0 – 10.0]
# Données simulées mais réalistes, cohérentes avec les classements publics.

ECOLES = {
    # ──────── Groupe Centrale ────────
    "Centrale Paris (CentraleSupélec)": [58000, 97, 4500, 12, 4.0, 8.5],
    "Centrale Lyon":                     [52000, 95, 3800, 14, 4.2, 8.0],
    "Centrale Lille":                    [48000, 93, 3500, 16, 3.8, 7.5],
    "Centrale Nantes":                   [49000, 94, 3200, 18, 4.5, 8.0],
    "Centrale Marseille":                [46000, 91, 3000, 17, 3.5, 7.0],

    # ──────── Mines ────────
    "Mines Paris (PSL)":                 [60000, 98, 5000, 10, 3.5, 7.0],
    "Mines Saint-Étienne":               [47000, 92, 2800, 20, 4.0, 7.5],
    "Mines Nancy":                       [46000, 91, 2500, 19, 3.8, 7.0],
    "IMT Atlantique":                    [48000, 93, 2600, 22, 4.5, 7.5],
    "IMT Mines Albi":                    [43000, 89, 2200, 24, 4.2, 6.5],

    # ──────── Groupe INSA ────────
    "INSA Lyon":                         [45000, 94, 1200, 30, 4.5, 9.0],
    "INSA Toulouse":                     [44000, 92, 1100, 28, 4.3, 8.5],
    "INSA Rennes":                       [43000, 91, 1000, 27, 4.0, 8.0],
    "INSA Rouen":                        [42000, 90, 1000, 26, 3.8, 7.5],
    "INSA Strasbourg":                   [43000, 91, 1100, 25, 4.0, 7.5],

    # ──────── Réseau Polytech ────────
    "Polytech Nice Sophia":              [38000, 88, 800,  25, 3.0, 7.5],
    "Polytech Montpellier":              [37000, 87, 700,  28, 3.2, 7.0],
    "Polytech Grenoble":                 [39000, 89, 900,  24, 3.5, 7.5],
    "Polytech Nantes":                   [38000, 88, 750,  26, 3.3, 7.0],
    "Polytech Lille":                    [37000, 87, 700,  27, 3.0, 6.5],

    # ──────── Universités de Technologie ────────
    "UTC (Compiègne)":                   [47000, 93, 1800, 22, 4.0, 8.5],
    "UTT (Troyes)":                      [42000, 91, 1500, 22, 4.0, 8.0],
    "UTBM (Belfort-Montbéliard)":        [40000, 89, 1300, 23, 3.5, 7.5],

    # ──────── Grandes Écoles d'excellence ────────
    "ISAE-SUPAERO":                      [55000, 96, 4000, 11, 4.5, 8.0],
    "ENSTA Paris":                       [53000, 95, 3500, 14, 4.0, 7.0],
    "ENSAE Paris":                       [57000, 96, 4200, 9,  3.0, 6.0],
    "Télécom Paris":                     [56000, 97, 4800, 13, 4.0, 7.5],
    "Télécom SudParis":                  [48000, 92, 3600, 16, 3.8, 7.0],

    # ──────── Arts et Métiers / ENSAM ────────
    "Arts et Métiers (ENSAM)":           [46000, 93, 2500, 20, 3.5, 8.5],
    "Arts et Métiers Lille":             [44000, 91, 2300, 21, 3.3, 8.0],

    # ──────── Écoles spécialisées Informatique/Numérique ────────
    "ENSIMAG (Grenoble INP)":            [52000, 95, 3000, 15, 3.5, 6.5],
    "ENSEEIHT (Toulouse INP)":           [49000, 93, 2800, 17, 3.8, 7.0],
    "ENSEIRB-MATMECA (Bordeaux INP)":    [48000, 92, 2700, 16, 3.5, 7.0],
    "EPITA":                             [45000, 92, 10500, 15, 2.5, 8.5],
    "EFREI":                             [39000, 87, 9500, 18, 2.0, 9.0],

    # ──────── Écoles post-bac privées ────────
    "ECE Paris":                         [40000, 89, 10000, 20, 2.5, 8.5],
    "ESIEE Paris":                       [41000, 90, 8500, 19, 2.8, 7.5],
    "ESME Sudria":                       [38000, 86, 9000, 17, 2.2, 7.0],
    "ESILV (Léonard de Vinci)":          [42000, 90, 11000, 16, 2.5, 8.0],
    "EPF":                               [40000, 88, 9500, 22, 3.0, 7.5],

    # ──────── Écoles à dominante Chimie/Matériaux ────────
    "Chimie ParisTech (PSL)":            [50000, 93, 3000, 13, 4.5, 6.0],
    "ESPCI Paris (PSL)":                 [54000, 96, 1500, 8,  4.8, 5.5],
    "ENSCM (Montpellier)":              [41000, 89, 1800, 22, 4.0, 6.5],

    # ──────── Écoles à dominante Agro/Bio ────────
    "AgroParisTech":                     [44000, 91, 2000, 18, 5.0, 7.5],
    "ENSAT (Toulouse)":                  [39000, 87, 1200, 25, 4.5, 7.0],

    # ──────── Écoles à dominante Génie Civil / BTP ────────
    "ESTP Paris":                        [45000, 93, 8000, 15, 3.0, 8.0],
    "ENTPE (Lyon)":                      [43000, 90, 1500, 20, 3.8, 6.5],

    # ──────── Autres écoles reconnues ────────
    "ENSC Cognitique (Bordeaux)":        [41000, 88, 1800, 30, 3.5, 7.5],
    "ESTIA (Bidart)":                    [40000, 88, 5500, 20, 3.5, 8.0],
    "EIGSI (La Rochelle)":               [38000, 86, 7500, 22, 3.0, 7.5],
}

# =============================================================================
# ███████████████████████████████████████████████████████████████████████████████
# █  SECTION 2 : PARAMÈTRES DES MÉTHODES AMD                                 █
# ███████████████████████████████████████████████████████████████████████████████
# =============================================================================

# ── Noms affichés des critères ──
CRITERE_NOMS = ["g1 Salaire", "g2 Emploi", "g3 Coût", "g4 Diversité",
                "g5 DD&RS", "g6 Vie Asso."]
CRITERE_UNITES = ["€/an", "%", "€ (3 ans)", "%", "/5", "/10"]

# ── Sens d'optimisation : True = maximiser, False = minimiser ──
MAXIMISER = [True, True, False, True, True, True]

# ── Vecteur OWA (poids par rang, du meilleur au pire critère) ──
# Source : rapport AMD v1
W_OWA = [0.05, 0.15, 0.20, 0.20, 0.20, 0.20]

# ── Indices d'interaction pour Choquet (modèle 2-additif de Grabisch) ──
# I(g1, g2) = -0.05 → Redondance entre salaire et emploi
# I(g4, g6) = +0.05 → Synergie entre diversité sociale et vie associative
# Tous les autres indices d'interaction = 0
INTERACTIONS_CHOQUET = {
    (0, 1): -0.05,   # I(g1, g2) redondance
    (3, 5): +0.05,   # I(g4, g6) synergie
}

# ── Seuils ELECTRE Is (source : rapport AMD v1) ──
# q = seuil d'indifférence, p = seuil de préférence, v = seuil de veto
# Le veto n'est défini que sur g1, g2, g3, g6
SEUILS_ELECTRE = {
    0: {'q': 1500, 'p': 3000, 'v': 10000},   # g1 Salaire (€/an)
    1: {'q': 1.0,  'p': 3.0,  'v': 8.0},     # g2 Emploi (%)
    2: {'q': 500,  'p': 1500, 'v': 5000},     # g3 Coût (€)
    3: {'q': 2.0,  'p': 5.0},                 # g4 Diversité (%) – pas de veto
    4: {'q': 0.3,  'p': 0.8},                 # g5 DD&RS (/5) – pas de veto
    5: {'q': 0.5,  'p': 1.5,  'v': 4.0},     # g6 Vie associative (/10)
}

# ── Seuil de concordance globale λ pour ELECTRE Is ──
LAMBDA_ELECTRE = 0.65


# =============================================================================
# ███████████████████████████████████████████████████████████████████████████████
# █  SECTION 3 : FONCTIONS DE CALCUL — MOTEUR AMD                            █
# ███████████████████████████████████████████████████████████████████████████████
# =============================================================================

def normaliser_minmax(ecoles):
    """
    Normalise les performances brutes de toutes les écoles en utilités [0; 100]
    via la méthode min-max. Pour un critère à maximiser :
        u_j(a) = (g_j(a) - min_j) / (max_j - min_j) × 100
    Pour un critère à minimiser (g3) :
        u_j(a) = (max_j - g_j(a)) / (max_j - min_j) × 100

    Args:
        ecoles: dict {nom: [g1, g2, g3, g4, g5, g6]}

    Returns:
        dict {nom: [u1, u2, u3, u4, u5, u6]} avec u_j ∈ [0, 100]
    """
    noms = list(ecoles.keys())
    n_criteres = 6

    # Calcul des bornes min et max pour chaque critère sur les 50 écoles
    mins = [min(ecoles[n][j] for n in noms) for j in range(n_criteres)]
    maxs = [max(ecoles[n][j] for n in noms) for j in range(n_criteres)]

    utilites = {}
    for nom in noms:
        u = []
        for j in range(n_criteres):
            amplitude = maxs[j] - mins[j]
            if amplitude == 0:
                u.append(50.0)  # Cas dégénéré : toutes les écoles ont la même valeur
            elif MAXIMISER[j]:
                u.append((ecoles[nom][j] - mins[j]) / amplitude * 100)
            else:
                # Critère à minimiser : on inverse la normalisation
                u.append((maxs[j] - ecoles[nom][j]) / amplitude * 100)
        utilites[nom] = u

    return utilites


def methode_somme_ponderee(utilites, poids):
    """
    Somme Pondérée classique : S(a) = Σ_j  w_j × u_j(a)
    Approche à compensation totale : une très bonne note peut compenser
    une mauvaise note sur un autre critère.

    Args:
        utilites: dict {nom: [u1,...,u6]}
        poids: liste [w1,...,w6] (sera normalisée en interne)

    Returns:
        liste de tuples (nom, score) triée par score décroissant
    """
    # Normalisation des poids pour qu'ils somment à 1
    somme_w = sum(poids)
    if somme_w == 0:
        w_norm = [1/6] * 6
    else:
        w_norm = [w / somme_w for w in poids]

    scores = []
    for nom, u in utilites.items():
        score = sum(w_norm[j] * u[j] for j in range(6))
        scores.append((nom, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def methode_owa(utilites, poids):
    """
    Opérateur OWA (Ordered Weighted Averaging) de Yager.
    Les utilités normalisées de chaque école sont triées par ordre DÉCROISSANT,
    puis pondérées par le vecteur de rang W_OWA.

    Le vecteur W = (0.05, 0.15, 0.20, 0.20, 0.20, 0.20) donne un poids
    faible au meilleur critère et des poids égaux aux autres, ce qui favorise
    les profils ÉQUILIBRÉS plutôt que les écoles brillantes sur un seul axe.

    Note : les poids des curseurs (poids utilisateur) servent ici à pondérer
    les utilités AVANT le tri, créant une utilité pondérée par critère.

    Args:
        utilites: dict {nom: [u1,...,u6]}
        poids: liste [w1,...,w6] (poids utilisateur pour pondérer les utilités)

    Returns:
        liste de tuples (nom, score) triée par score décroissant
    """
    # Normalisation des poids utilisateur
    somme_w = sum(poids)
    if somme_w == 0:
        w_norm = [1/6] * 6
    else:
        w_norm = [w / somme_w for w in poids]

    scores = []
    for nom, u in utilites.items():
        # Pondération des utilités par les poids utilisateur
        u_pond = [w_norm[j] * u[j] * 6 for j in range(6)]
        # Tri par ordre décroissant (meilleure utilité pondérée en premier)
        u_triees = sorted(u_pond, reverse=True)
        # Application du vecteur OWA
        score = sum(W_OWA[k] * u_triees[k] for k in range(6))
        scores.append((nom, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def methode_choquet(utilites, poids):
    """
    Intégrale de Choquet avec modèle 2-additif de Grabisch.

    Formule simplifiée pour le modèle 2-additif :
        C_v(u) = Σ_i φ_i × u_i
                 + Σ_{I_ij > 0} I_ij × min(u_i, u_j)      [synergie]
                 - Σ_{I_ij < 0} |I_ij| × max(u_i, u_j)    [redondance]

    Les valeurs de Shapley (φ_i) sont fixées aux poids des curseurs.
    Les indices d'interaction encodent les dépendances entre critères :
        • I(g1, g2) = -0.05 : redondance salaire/emploi
        • I(g4, g6) = +0.05 : synergie diversité/vie associative

    Args:
        utilites: dict {nom: [u1,...,u6]}
        poids: liste [w1,...,w6] (valeurs de Shapley = poids utilisateur)

    Returns:
        liste de tuples (nom, score) triée par score décroissant
    """
    # Normalisation des poids → valeurs de Shapley
    somme_w = sum(poids)
    if somme_w == 0:
        shapley = [1/6] * 6
    else:
        shapley = [w / somme_w for w in poids]

    scores = []
    for nom, u in utilites.items():
        # Terme linéaire : Σ φ_i × u_i
        score = sum(shapley[j] * u[j] for j in range(6))

        # Termes d'interaction (modèle 2-additif)
        for (i, j), I_ij in INTERACTIONS_CHOQUET.items():
            if I_ij > 0:
                # Synergie → on ajoute I_ij × min(u_i, u_j)
                score += I_ij * min(u[i], u[j])
            else:
                # Redondance → on soustrait |I_ij| × max(u_i, u_j)
                score += I_ij * max(u[i], u[j])
                # Note : I_ij est négatif, donc += revient à soustraire

        scores.append((nom, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def methode_min(utilites, poids):
    """
    Méthode du Min (Maximin / critère de Wald).
    Logique purement pessimiste : le score d'une école est déterminé
    par sa PIRE performance normalisée, pondérée par les poids.

    S(a) = min_j { w_j × u_j(a) × 6 }

    Cette méthode n'accepte AUCUNE compensation : une seule utilité
    faible condamne l'école, même si elle excelle partout ailleurs.

    Note : Sur 50 écoles, le Min crée souvent des ex æquo car de
    nombreuses écoles peuvent avoir un même minimum à 0.

    Args:
        utilites: dict {nom: [u1,...,u6]}
        poids: liste [w1,...,w6]

    Returns:
        liste de tuples (nom, score) triée par score décroissant
    """
    # Normalisation des poids
    somme_w = sum(poids)
    if somme_w == 0:
        w_norm = [1/6] * 6
    else:
        w_norm = [w / somme_w for w in poids]

    scores = []
    for nom, u in utilites.items():
        # Score = minimum des utilités pondérées (×6 pour ramener à [0,100])
        score = min(w_norm[j] * u[j] * 6 for j in range(6))
        scores.append((nom, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def methode_electre_is(ecoles, poids):
    """
    ELECTRE Is — Méthode de surclassement non compensatoire.

    Pour chaque paire d'écoles (a, b), on calcule :
    1. La concordance partielle c_j(a,b) pour chaque critère j
    2. La concordance globale C(a,b) = Σ w_j × c_j / Σ w_j
    3. La discordance partielle d_j(a,b) (uniquement si un veto existe)
    4. Le degré de crédibilité σ(a,b) = C(a,b) × Π ajustement veto
    5. a surclasse b (a S b) si σ(a,b) ≥ λ

    Score net = nb(a surclasse •) − nb(• surclasse a)
    Le classement final est basé sur ce score net.

    Args:
        ecoles: dict {nom: [g1,...,g6]} (performances BRUTES)
        poids: liste [w1,...,w6]

    Returns:
        liste de tuples (nom, score_net) triée par score_net décroissant
    """
    noms = list(ecoles.keys())
    n = len(noms)

    # Normalisation des poids
    somme_w = sum(poids)
    if somme_w == 0:
        w_norm = [1/6] * 6
    else:
        w_norm = [w / somme_w for w in poids]

    def concordance_partielle(ga, gb, j):
        """
        Calcule c_j(a, b) : degré de concordance du critère j
        pour la proposition 'a est au moins aussi bonne que b'.
        """
        seuils = SEUILS_ELECTRE[j]
        q = seuils['q']
        p = seuils['p']

        if MAXIMISER[j]:
            diff = ga - gb  # Avantage de a sur b
        else:
            diff = gb - ga  # Pour g3 (à minimiser), on inverse

        if diff >= -q:
            return 1.0    # a est indifférent ou meilleur que b
        elif diff <= -p:
            return 0.0    # b est strictement préféré à a
        else:
            return (diff + p) / (p - q)  # Zone intermédiaire

    def discordance_partielle(ga, gb, j):
        """
        Calcule d_j(a, b) : degré de discordance (veto potentiel)
        du critère j pour la proposition 'a surclasse b'.
        """
        seuils = SEUILS_ELECTRE[j]
        if 'v' not in seuils:
            return 0.0  # Pas de veto sur ce critère

        p = seuils['p']
        v = seuils['v']

        if MAXIMISER[j]:
            diff = gb - ga  # Écart en faveur de b (désavantage de a)
        else:
            diff = ga - gb  # Pour g3 (minimiser), c'est a qui est pénalisé si plus cher

        if diff <= p:
            return 0.0    # Pas de discordance
        elif diff >= v:
            return 1.0    # Veto total
        else:
            return (diff - p) / (v - p)  # Discordance partielle

    # ── Construction de la matrice de surclassement ──
    surclasse = [[False] * n for _ in range(n)]

    for i in range(n):
        for k in range(n):
            if i == k:
                continue

            a = ecoles[noms[i]]
            b = ecoles[noms[k]]

            # 1. Concordance globale pondérée
            C_ab = sum(w_norm[j] * concordance_partielle(a[j], b[j], j)
                       for j in range(6))

            # 2. Degré de crédibilité avec ajustement par les discordances
            sigma = C_ab
            for j in range(6):
                d_j = discordance_partielle(a[j], b[j], j)
                if d_j > C_ab:
                    if C_ab < 1.0:
                        sigma *= (1.0 - d_j) / (1.0 - C_ab)
                    else:
                        sigma = 0.0

            # 3. Test de surclassement : σ(a,b) ≥ λ
            if sigma >= LAMBDA_ELECTRE:
                surclasse[i][k] = True

    # ── Calcul du score net pour chaque école ──
    scores = []
    for i in range(n):
        nb_surclasse = sum(1 for k in range(n) if surclasse[i][k])   # a S •
        nb_surclasse_par = sum(1 for k in range(n) if surclasse[k][i])  # • S a
        score_net = nb_surclasse - nb_surclasse_par
        scores.append((noms[i], score_net))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


# =============================================================================
# ███████████████████████████████████████████████████████████████████████████████
# █  SECTION 4 : INTERFACE GRAPHIQUE — STYLE RATP / MÉTRO PARISIEN           █
# ███████████████████████████████████████████████████████████████████████████████
# =============================================================================

class SimulateurAMD(tk.Tk):
    """
    Fenêtre principale du Simulateur AMD v2.0.
    Style institutionnel sobre et professionnel inspiré de la charte RATP :
    fond blanc/gris très clair, typographie noire, accents bleu nuit.
    """

    # ── Palette de couleurs RATP ──
    COULEURS = {
        'fond':          '#F5F5F5',  # Gris très clair (fond général)
        'fond_panneau':  '#FFFFFF',  # Blanc pur (panneaux)
        'bleu_ratp':     '#003366',  # Bleu nuit RATP (titres, accents)
        'bleu_clair':    '#1A5276',  # Bleu intermédiaire (sous-titres)
        'vert_metro':    '#27AE60',  # Vert métro (bouton action)
        'vert_fonce':    '#1E8449',  # Vert foncé (survol bouton)
        'texte':         '#1C1C1C',  # Noir profond (texte principal)
        'texte_gris':    '#555555',  # Gris moyen (texte secondaire)
        'bordure':       '#CCCCCC',  # Gris clair (bordures)
        'or':            '#D4AC0D',  # Or (médaille 1ère place)
        'argent':        '#95A5A6',  # Argent (2e place)
        'bronze':        '#BA6B2E',  # Bronze (3e place)
        'fond_top':      '#EBF5FB',  # Bleu très clair (fond Top 5)
        'ligne_paire':   '#F9F9F9',  # Alternance lignes tableau
    }

    def __init__(self):
        super().__init__()

        # ── Configuration de la fenêtre ──
        self.title("Simulateur AMD v2.0 — 50 Écoles d'Ingénieurs Françaises")
        self.configure(bg=self.COULEURS['fond'])
        self.geometry("1380x820")
        self.minsize(1200, 700)

        # ── Variables pour les curseurs de poids ──
        self.poids_vars = [tk.DoubleVar(value=round(1/6, 2)) for _ in range(6)]

        # ── Variable pour la méthode sélectionnée ──
        self.methode_var = tk.StringVar(value="Somme Pondérée")

        # ── Construction de l'interface ──
        self._creer_en_tete()
        self._creer_panneau_gauche()
        self._creer_panneau_droit()

    # ─────────────────────────────────────────────────────────────────────
    #  EN-TÊTE — Barre de titre style RATP
    # ─────────────────────────────────────────────────────────────────────
    def _creer_en_tete(self):
        """Crée la barre d'en-tête bleu nuit avec le titre de l'application."""
        barre = tk.Frame(self, bg=self.COULEURS['bleu_ratp'], height=60)
        barre.pack(fill='x', side='top')
        barre.pack_propagate(False)

        # Titre principal
        titre = tk.Label(
            barre,
            text="◆  SIMULATEUR AMD v2.0 — Aide Multicritère à la Décision",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg=self.COULEURS['bleu_ratp'],
            padx=20
        )
        titre.pack(side='left', fill='y')

        # Sous-titre à droite
        sous_titre = tk.Label(
            barre,
            text="50 Écoles d'Ingénieurs  │  5 Méthodes AMD  │  M1 MIAGE",
            font=("Segoe UI", 10),
            fg="#AAC4D7",
            bg=self.COULEURS['bleu_ratp'],
            padx=20
        )
        sous_titre.pack(side='right', fill='y')

    # ─────────────────────────────────────────────────────────────────────
    #  PANNEAU GAUCHE — Paramètres (Curseurs + Méthode + Bouton)
    # ─────────────────────────────────────────────────────────────────────
    def _creer_panneau_gauche(self):
        """Crée le panneau de saisie des paramètres (poids, méthode, bouton)."""
        # Conteneur principal gauche
        frame_gauche = tk.Frame(self, bg=self.COULEURS['fond'], width=440)
        frame_gauche.pack(side='left', fill='y', padx=(15, 5), pady=15)
        frame_gauche.pack_propagate(False)

        # ── Bloc Curseurs ──
        bloc_curseurs = tk.LabelFrame(
            frame_gauche,
            text="  🎛️  PARAMÈTRES — Poids des critères  ",
            font=("Segoe UI", 11, "bold"),
            fg=self.COULEURS['bleu_ratp'],
            bg=self.COULEURS['fond_panneau'],
            bd=1,
            relief='solid',
            padx=15,
            pady=10
        )
        bloc_curseurs.pack(fill='x', pady=(0, 10))

        # Explication
        tk.Label(
            bloc_curseurs,
            text="Ajustez l'importance de chaque critère (0.00 → 1.00) :",
            font=("Segoe UI", 9),
            fg=self.COULEURS['texte_gris'],
            bg=self.COULEURS['fond_panneau'],
            anchor='w'
        ).pack(fill='x', pady=(0, 8))

        # Création des 6 curseurs
        self.labels_poids = []
        icones = ["💰", "📊", "🏦", "🌍", "🌱", "🎉"]
        couleurs_curseurs = ["#2C3E50", "#2980B9", "#E74C3C", "#27AE60", "#16A085", "#8E44AD"]

        for j in range(6):
            frame_curseur = tk.Frame(bloc_curseurs, bg=self.COULEURS['fond_panneau'])
            frame_curseur.pack(fill='x', pady=3)

            # Icône + Nom du critère
            label_nom = tk.Label(
                frame_curseur,
                text=f"{icones[j]}  {CRITERE_NOMS[j]}",
                font=("Segoe UI", 9, "bold"),
                fg=couleurs_curseurs[j],
                bg=self.COULEURS['fond_panneau'],
                width=18,
                anchor='w'
            )
            label_nom.pack(side='left')

            # Curseur (slider)
            curseur = tk.Scale(
                frame_curseur,
                variable=self.poids_vars[j],
                from_=0.0,
                to=1.0,
                resolution=0.01,
                orient='horizontal',
                length=200,
                sliderlength=18,
                width=12,
                font=("Segoe UI", 8),
                fg=self.COULEURS['texte'],
                bg=self.COULEURS['fond_panneau'],
                troughcolor='#E8E8E8',
                highlightthickness=0,
                bd=0,
            )
            curseur.pack(side='left', padx=(5, 5))

            # Valeur affichée
            label_val = tk.Label(
                frame_curseur,
                text=f"{self.poids_vars[j].get():.2f}",
                font=("Consolas", 9, "bold"),
                fg=couleurs_curseurs[j],
                bg=self.COULEURS['fond_panneau'],
                width=5
            )
            label_val.pack(side='left')
            self.labels_poids.append(label_val)

            # Mise à jour dynamique de l'affichage du poids
            self.poids_vars[j].trace_add('write',
                lambda *args, idx=j, lbl=label_val: lbl.config(
                    text=f"{self.poids_vars[idx].get():.2f}"))

        # ── Bloc Méthode ──
        bloc_methode = tk.LabelFrame(
            frame_gauche,
            text="  🧮  MODÈLE DE DÉCISION  ",
            font=("Segoe UI", 11, "bold"),
            fg=self.COULEURS['bleu_ratp'],
            bg=self.COULEURS['fond_panneau'],
            bd=1,
            relief='solid',
            padx=15,
            pady=10
        )
        bloc_methode.pack(fill='x', pady=(0, 10))

        # Menu déroulant des méthodes
        methodes = [
            "Somme Pondérée",
            "Opérateur OWA",
            "Intégrale de Choquet",
            "Méthode du Min",
            "ELECTRE Is"
        ]

        combo = ttk.Combobox(
            bloc_methode,
            textvariable=self.methode_var,
            values=methodes,
            state='readonly',
            font=("Segoe UI", 10),
            width=30
        )
        combo.pack(fill='x', pady=(0, 5))

        # Description dynamique de la méthode
        self.label_desc_methode = tk.Label(
            bloc_methode,
            text="",
            font=("Segoe UI", 8, "italic"),
            fg=self.COULEURS['texte_gris'],
            bg=self.COULEURS['fond_panneau'],
            wraplength=380,
            justify='left',
            anchor='w'
        )
        self.label_desc_methode.pack(fill='x')
        self._maj_description_methode()
        self.methode_var.trace_add('write', lambda *a: self._maj_description_methode())

        # ── Bouton de lancement ──
        frame_bouton = tk.Frame(frame_gauche, bg=self.COULEURS['fond'])
        frame_bouton.pack(fill='x', pady=(5, 10))

        self.bouton = tk.Button(
            frame_bouton,
            text="▶  Lancer la recherche du compromis",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg=self.COULEURS['vert_metro'],
            activebackground=self.COULEURS['vert_fonce'],
            activeforeground="white",
            cursor="hand2",
            relief='flat',
            padx=20,
            pady=12,
            command=self._lancer_calcul
        )
        self.bouton.pack(fill='x')

        # Effet de survol sur le bouton
        self.bouton.bind('<Enter>', lambda e: self.bouton.config(
            bg=self.COULEURS['vert_fonce']))
        self.bouton.bind('<Leave>', lambda e: self.bouton.config(
            bg=self.COULEURS['vert_metro']))

        # ── Bloc Info (légende) ──
        bloc_info = tk.LabelFrame(
            frame_gauche,
            text="  ℹ️  LÉGENDE DES CRITÈRES  ",
            font=("Segoe UI", 10, "bold"),
            fg=self.COULEURS['bleu_clair'],
            bg=self.COULEURS['fond_panneau'],
            bd=1,
            relief='solid',
            padx=10,
            pady=8
        )
        bloc_info.pack(fill='x', pady=(0, 5))

        legende = [
            ("g1 Salaire",    "35k – 60k €/an",      "▲ MAX"),
            ("g2 Emploi",     "85 – 100 %",           "▲ MAX"),
            ("g3 Coût",       "0 – 15 000 € (3 ans)", "▼ MIN"),
            ("g4 Diversité",  "5 – 40 %",             "▲ MAX"),
            ("g5 DD&RS",      "1 – 5 (note)",         "▲ MAX"),
            ("g6 Vie Asso.",  "1 – 10 (note)",        "▲ MAX"),
        ]

        for nom, echelle, sens in legende:
            f = tk.Frame(bloc_info, bg=self.COULEURS['fond_panneau'])
            f.pack(fill='x', pady=1)
            tk.Label(f, text=nom, font=("Segoe UI", 8, "bold"),
                     fg=self.COULEURS['texte'], bg=self.COULEURS['fond_panneau'],
                     width=13, anchor='w').pack(side='left')
            tk.Label(f, text=echelle, font=("Segoe UI", 8),
                     fg=self.COULEURS['texte_gris'], bg=self.COULEURS['fond_panneau'],
                     width=18, anchor='w').pack(side='left')
            couleur_sens = "#E74C3C" if "MIN" in sens else "#27AE60"
            tk.Label(f, text=sens, font=("Segoe UI", 8, "bold"),
                     fg=couleur_sens, bg=self.COULEURS['fond_panneau'],
                     anchor='e').pack(side='right')

    # ─────────────────────────────────────────────────────────────────────
    #  PANNEAU DROIT — Résultats et Statistiques
    # ─────────────────────────────────────────────────────────────────────
    def _creer_panneau_droit(self):
        """Crée le panneau de visualisation des résultats."""
        # Conteneur principal droit
        self.frame_droit = tk.Frame(self, bg=self.COULEURS['fond'])
        self.frame_droit.pack(side='right', fill='both', expand=True,
                              padx=(5, 15), pady=15)

        # ── Zone Recommandation (école n°1) ──
        self.bloc_reco = tk.LabelFrame(
            self.frame_droit,
            text="  🏆  RECOMMANDATION MAJEURE  ",
            font=("Segoe UI", 12, "bold"),
            fg=self.COULEURS['bleu_ratp'],
            bg=self.COULEURS['fond_panneau'],
            bd=1,
            relief='solid',
            padx=15,
            pady=10
        )
        self.bloc_reco.pack(fill='x', pady=(0, 10))

        # Nom de l'école recommandée
        self.label_ecole_reco = tk.Label(
            self.bloc_reco,
            text="— En attente du calcul —",
            font=("Segoe UI", 18, "bold"),
            fg=self.COULEURS['bleu_ratp'],
            bg=self.COULEURS['fond_panneau'],
            anchor='w'
        )
        self.label_ecole_reco.pack(fill='x', pady=(0, 5))

        # Score de l'école
        self.label_score_reco = tk.Label(
            self.bloc_reco,
            text="",
            font=("Segoe UI", 11),
            fg=self.COULEURS['vert_metro'],
            bg=self.COULEURS['fond_panneau'],
            anchor='w'
        )
        self.label_score_reco.pack(fill='x')

        # Méthode utilisée
        self.label_methode_reco = tk.Label(
            self.bloc_reco,
            text="",
            font=("Segoe UI", 9, "italic"),
            fg=self.COULEURS['texte_gris'],
            bg=self.COULEURS['fond_panneau'],
            anchor='w'
        )
        self.label_methode_reco.pack(fill='x')

        # ── Zone Statistiques détaillées de l'école n°1 ──
        self.bloc_stats = tk.LabelFrame(
            self.frame_droit,
            text="  📋  STATISTIQUES DE L'ÉCOLE RECOMMANDÉE  ",
            font=("Segoe UI", 10, "bold"),
            fg=self.COULEURS['bleu_clair'],
            bg=self.COULEURS['fond_panneau'],
            bd=1,
            relief='solid',
            padx=10,
            pady=8
        )
        self.bloc_stats.pack(fill='x', pady=(0, 10))

        # Frame pour le tableau de stats
        self.frame_stats_table = tk.Frame(
            self.bloc_stats, bg=self.COULEURS['fond_panneau'])
        self.frame_stats_table.pack(fill='x')

        # Pré-remplissage du tableau vide
        self._creer_tableau_stats_vide()

        # ── Zone Top 5 ──
        self.bloc_top5 = tk.LabelFrame(
            self.frame_droit,
            text="  🗺️  HORIZON DES POSSIBLES — Top 5 du classement  ",
            font=("Segoe UI", 10, "bold"),
            fg=self.COULEURS['bleu_clair'],
            bg=self.COULEURS['fond_top'],
            bd=1,
            relief='solid',
            padx=10,
            pady=8
        )
        self.bloc_top5.pack(fill='both', expand=True)

        # Frame pour le tableau Top 5
        self.frame_top5_table = tk.Frame(
            self.bloc_top5, bg=self.COULEURS['fond_top'])
        self.frame_top5_table.pack(fill='both', expand=True)

        self._creer_top5_vide()

    # ─────────────────────────────────────────────────────────────────────
    #  MÉTHODES UTILITAIRES DE L'INTERFACE
    # ─────────────────────────────────────────────────────────────────────

    def _maj_description_methode(self):
        """Met à jour la description textuelle de la méthode sélectionnée."""
        descriptions = {
            "Somme Pondérée":
                "Approche classique à compensation totale. Le score est la "
                "moyenne pondérée des utilités normalisées. Une bonne note "
                "peut compenser une faiblesse.",
            "Opérateur OWA":
                "Approche sensible au profil de risque. Le vecteur W = (0.05, "
                "0.15, 0.20, 0.20, 0.20, 0.20) favorise les écoles aux profils "
                "équilibrés plutôt que les écoles extrêmes.",
            "Intégrale de Choquet":
                "Modèle 2-additif de Grabisch. Gère les dépendances : "
                "redondance salaire/emploi (I=-0.05), synergie "
                "diversité/vie associative (I=+0.05).",
            "Méthode du Min":
                "Logique purement pessimiste (Maximin de Wald). L'école "
                "est jugée uniquement sur sa plus mauvaise note normalisée. "
                "Aucune compensation possible.",
            "ELECTRE Is":
                "Surclassement non compensatoire. Utilise la concordance, "
                "la discordance et des vetos (g1, g2, g3, g6). Seuil λ = 0.65. "
                "Le score net trie les 50 écoles."
        }
        methode = self.methode_var.get()
        self.label_desc_methode.config(
            text=descriptions.get(methode, ""))

    def _creer_tableau_stats_vide(self):
        """Crée un tableau vide pour les statistiques de l'école recommandée."""
        for w in self.frame_stats_table.winfo_children():
            w.destroy()

        # En-têtes
        headers = ["Critère", "Perf. brute", "Utilité [0-100]"]
        for col, h in enumerate(headers):
            lbl = tk.Label(
                self.frame_stats_table, text=h,
                font=("Segoe UI", 9, "bold"),
                fg="white",
                bg=self.COULEURS['bleu_ratp'],
                padx=8, pady=4,
                anchor='center'
            )
            lbl.grid(row=0, column=col, sticky='nsew', padx=(0, 1))

        for j in range(6):
            bg = self.COULEURS['ligne_paire'] if j % 2 == 0 else self.COULEURS['fond_panneau']
            tk.Label(
                self.frame_stats_table,
                text=f"{CRITERE_NOMS[j]} ({CRITERE_UNITES[j]})",
                font=("Segoe UI", 9),
                fg=self.COULEURS['texte'],
                bg=bg, padx=8, pady=3, anchor='w'
            ).grid(row=j+1, column=0, sticky='nsew')

            tk.Label(
                self.frame_stats_table, text="—",
                font=("Consolas", 9),
                fg=self.COULEURS['texte_gris'],
                bg=bg, padx=8, pady=3, anchor='center'
            ).grid(row=j+1, column=1, sticky='nsew')

            tk.Label(
                self.frame_stats_table, text="—",
                font=("Consolas", 9),
                fg=self.COULEURS['texte_gris'],
                bg=bg, padx=8, pady=3, anchor='center'
            ).grid(row=j+1, column=2, sticky='nsew')

        # Configuration des colonnes pour un redimensionnement proportionnel
        self.frame_stats_table.columnconfigure(0, weight=2)
        self.frame_stats_table.columnconfigure(1, weight=1)
        self.frame_stats_table.columnconfigure(2, weight=1)

    def _creer_top5_vide(self):
        """Crée un tableau Top 5 vide."""
        for w in self.frame_top5_table.winfo_children():
            w.destroy()

        lbl = tk.Label(
            self.frame_top5_table,
            text="Cliquez sur « Lancer la recherche du compromis » pour afficher le classement.",
            font=("Segoe UI", 11, "italic"),
            fg=self.COULEURS['texte_gris'],
            bg=self.COULEURS['fond_top'],
            pady=30
        )
        lbl.pack(expand=True)

    def _afficher_stats_ecole(self, nom_ecole, utilites_ecole):
        """
        Remplit le tableau des statistiques avec les performances brutes
        et les utilités normalisées de l'école recommandée.
        """
        for w in self.frame_stats_table.winfo_children():
            w.destroy()

        perfs = ECOLES[nom_ecole]

        # En-têtes
        headers = ["Critère", "Perf. brute", "Utilité [0-100]"]
        for col, h in enumerate(headers):
            lbl = tk.Label(
                self.frame_stats_table, text=h,
                font=("Segoe UI", 9, "bold"),
                fg="white",
                bg=self.COULEURS['bleu_ratp'],
                padx=8, pady=4,
                anchor='center'
            )
            lbl.grid(row=0, column=col, sticky='nsew', padx=(0, 1))

        for j in range(6):
            bg = self.COULEURS['ligne_paire'] if j % 2 == 0 else self.COULEURS['fond_panneau']

            # Nom du critère
            tk.Label(
                self.frame_stats_table,
                text=f"{CRITERE_NOMS[j]} ({CRITERE_UNITES[j]})",
                font=("Segoe UI", 9),
                fg=self.COULEURS['texte'],
                bg=bg, padx=8, pady=3, anchor='w'
            ).grid(row=j+1, column=0, sticky='nsew')

            # Performance brute
            if j == 0:
                perf_txt = f"{perfs[j]:,} €".replace(",", " ")
            elif j == 1 or j == 3:
                perf_txt = f"{perfs[j]:.1f} %"
            elif j == 2:
                perf_txt = f"{perfs[j]:,} €".replace(",", " ")
            elif j == 4:
                perf_txt = f"{perfs[j]:.1f} / 5"
            else:
                perf_txt = f"{perfs[j]:.1f} / 10"

            tk.Label(
                self.frame_stats_table, text=perf_txt,
                font=("Consolas", 9, "bold"),
                fg=self.COULEURS['texte'],
                bg=bg, padx=8, pady=3, anchor='center'
            ).grid(row=j+1, column=1, sticky='nsew')

            # Utilité normalisée avec barre de couleur
            u = utilites_ecole[j]
            if u >= 75:
                couleur_u = "#27AE60"  # Vert
            elif u >= 40:
                couleur_u = "#F39C12"  # Orange
            else:
                couleur_u = "#E74C3C"  # Rouge

            tk.Label(
                self.frame_stats_table, text=f"{u:.1f}",
                font=("Consolas", 9, "bold"),
                fg=couleur_u,
                bg=bg, padx=8, pady=3, anchor='center'
            ).grid(row=j+1, column=2, sticky='nsew')

        self.frame_stats_table.columnconfigure(0, weight=2)
        self.frame_stats_table.columnconfigure(1, weight=1)
        self.frame_stats_table.columnconfigure(2, weight=1)

    def _afficher_top5(self, classement, utilites_dict):
        """
        Affiche le Top 5 dans un tableau avec rang, nom, score et
        mini-résumé des forces de chaque école.
        """
        for w in self.frame_top5_table.winfo_children():
            w.destroy()

        # En-têtes du Top 5
        headers = ["#", "École", "Score", "Forces principales"]
        col_widths = [3, 32, 8, 35]
        for col, (h, w) in enumerate(zip(headers, col_widths)):
            lbl = tk.Label(
                self.frame_top5_table, text=h,
                font=("Segoe UI", 9, "bold"),
                fg="white",
                bg=self.COULEURS['bleu_ratp'],
                padx=6, pady=5,
                anchor='center',
                width=w
            )
            lbl.grid(row=0, column=col, sticky='nsew', padx=(0, 1))

        # Couleurs des médailles
        medailles = {
            0: ("🥇", self.COULEURS['or']),
            1: ("🥈", self.COULEURS['argent']),
            2: ("🥉", self.COULEURS['bronze']),
            3: ("  4", self.COULEURS['texte_gris']),
            4: ("  5", self.COULEURS['texte_gris']),
        }

        for rang in range(min(5, len(classement))):
            nom, score = classement[rang]
            icone, couleur_rang = medailles[rang]

            bg = self.COULEURS['fond_top'] if rang % 2 == 0 else self.COULEURS['fond_panneau']

            # Rang / Médaille
            tk.Label(
                self.frame_top5_table, text=icone,
                font=("Segoe UI", 11),
                fg=couleur_rang, bg=bg,
                padx=6, pady=4, anchor='center'
            ).grid(row=rang+1, column=0, sticky='nsew')

            # Nom de l'école
            font_nom = ("Segoe UI", 10, "bold") if rang == 0 else ("Segoe UI", 9)
            tk.Label(
                self.frame_top5_table, text=nom,
                font=font_nom,
                fg=self.COULEURS['bleu_ratp'] if rang == 0 else self.COULEURS['texte'],
                bg=bg, padx=6, pady=4, anchor='w'
            ).grid(row=rang+1, column=1, sticky='nsew')

            # Score
            tk.Label(
                self.frame_top5_table, text=f"{score:.2f}",
                font=("Consolas", 10, "bold"),
                fg=self.COULEURS['vert_metro'],
                bg=bg, padx=6, pady=4, anchor='center'
            ).grid(row=rang+1, column=2, sticky='nsew')

            # Forces : les 2 meilleurs critères normalisés
            forces_txt = self._identifier_forces(nom, utilites_dict)
            tk.Label(
                self.frame_top5_table, text=forces_txt,
                font=("Segoe UI", 8),
                fg=self.COULEURS['texte_gris'],
                bg=bg, padx=6, pady=4, anchor='w'
            ).grid(row=rang+1, column=3, sticky='nsew')

        # Configuration des colonnes
        self.frame_top5_table.columnconfigure(0, weight=0)
        self.frame_top5_table.columnconfigure(1, weight=3)
        self.frame_top5_table.columnconfigure(2, weight=1)
        self.frame_top5_table.columnconfigure(3, weight=3)

    def _identifier_forces(self, nom_ecole, utilites_dict):
        """
        Identifie les 2 critères les plus forts d'une école
        pour afficher un résumé rapide de ses atouts.
        """
        if nom_ecole not in utilites_dict:
            return ""
        u = utilites_dict[nom_ecole]
        # Indices triés par utilité décroissante
        indices_tries = sorted(range(6), key=lambda j: u[j], reverse=True)
        noms_courts = ["Salaire", "Emploi", "Coût", "Diversité", "DD&RS", "Vie Asso."]
        top2 = [noms_courts[indices_tries[0]], noms_courts[indices_tries[1]]]
        return f"✦ {top2[0]}  ✦ {top2[1]}"

    # ─────────────────────────────────────────────────────────────────────
    #  MOTEUR PRINCIPAL — Lancement du calcul
    # ─────────────────────────────────────────────────────────────────────
    def _lancer_calcul(self):
        """
        Fonction déclenchée par le bouton « Lancer la recherche du compromis ».
        Récupère les poids, appelle la méthode sélectionnée, et met à jour
        le panneau de résultats.
        """
        # Récupération des poids des curseurs
        poids = [v.get() for v in self.poids_vars]

        # Normalisation min-max des 50 écoles
        utilites = normaliser_minmax(ECOLES)

        # Sélection et exécution de la méthode
        methode = self.methode_var.get()

        if methode == "Somme Pondérée":
            classement = methode_somme_ponderee(utilites, poids)
        elif methode == "Opérateur OWA":
            classement = methode_owa(utilites, poids)
        elif methode == "Intégrale de Choquet":
            classement = methode_choquet(utilites, poids)
        elif methode == "Méthode du Min":
            classement = methode_min(utilites, poids)
        elif methode == "ELECTRE Is":
            # ELECTRE Is utilise les performances brutes, pas les utilités
            classement = methode_electre_is(ECOLES, poids)
        else:
            return

        # ── Mise à jour de l'affichage ──
        if classement:
            # École n°1
            nom_top1, score_top1 = classement[0]

            self.label_ecole_reco.config(
                text=f"🏆  {nom_top1}",
                fg=self.COULEURS['bleu_ratp']
            )

            # Score formaté selon la méthode
            if methode == "ELECTRE Is":
                self.label_score_reco.config(
                    text=f"Score net de surclassement : {score_top1:+d}  "
                         f"(sur {len(ECOLES)} écoles)")
            else:
                self.label_score_reco.config(
                    text=f"Score : {score_top1:.2f} / 100")

            self.label_methode_reco.config(
                text=f"Méthode appliquée : {methode}  │  "
                     f"Base de données : {len(ECOLES)} écoles d'ingénieurs")

            # Statistiques détaillées de l'école n°1
            self._afficher_stats_ecole(nom_top1, utilites[nom_top1])

            # Top 5
            self._afficher_top5(classement, utilites)


# =============================================================================
# ███████████████████████████████████████████████████████████████████████████████
# █  SECTION 5 : LANCEMENT DE L'APPLICATION                                  █
# ███████████████████████████████████████████████████████████████████████████████
# =============================================================================

if __name__ == "__main__":
    app = SimulateurAMD()
    app.mainloop()
