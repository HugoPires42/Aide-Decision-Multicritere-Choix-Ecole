# -*- coding: utf-8 -*-
"""
================================================================================
  SIMULATEUR AMD v3.0 — Aide Multicritère à la Décision
  50 Écoles d'Ingénieurs Françaises  ·  M1 MIAGE — Décision Multicritère
================================================================================

  Refonte complète de l'interface graphique pour une expérience ludique,
  moderne et lisible. Le moteur de calcul (5 méthodes) reste identique à v2.

  ── Méthodes AMD implémentées ──
     1. Somme Pondérée (normalisation min-max [0;100])
     2. Opérateur OWA de Yager  (W = 0.05 / 0.15 / 0.20 / 0.20 / 0.20 / 0.20)
     3. Intégrale de Choquet (modèle 2-additif de Grabisch)
          · I(g1, g2) = -0.05   →  redondance salaire / emploi
          · I(g4, g6) = +0.05   →  synergie diversité / vie associative
     4. Méthode du Min (Maximin / Wald)
     5. ELECTRE Is (concordance / discordance / vetos, λ = 0.65)

  ── Critères ──
     g1  Salaire moyen à la sortie  (€/an)         → MAX
     g2  Taux d'emploi à 6 mois     (%)            → MAX
     g3  Coût total sur 3 ans       (€)            → MIN
     g4  Diversité sociale          (%)            → MAX
     g5  Engagement DD&RS           (note /5)      → MAX
     g6  Vie associative            (note /10)     → MAX

  ── Design ──
     Style "Aurora" : palette violet/indigo moderne, header en dégradé,
     cartes blanches à bordure subtile, sliders personnalisés au Canvas,
     barres de progression colorées, cartes méthode cliquables, bouton
     d'action prééminent. Inspiration : Linear / Vercel / shadcn-ui.
================================================================================
"""

import tkinter as tk
from tkinter import ttk


# =============================================================================
# █  SECTION 1 — BASE DE DONNÉES : 50 ÉCOLES D'INGÉNIEURS FRANÇAISES         █
# =============================================================================
# Format : "Nom" : [g1, g2, g3, g4, g5, g6]
#   g1 salaire (€/an)  g2 emploi (%)  g3 coût (€)  g4 diversité (%)
#   g5 DD&RS (/5)      g6 vie asso. (/10)

ECOLES = {
    # ──────── Groupe Centrale ────────
    "Centrale Paris (CentraleSupélec)": [58000, 97, 4500, 12, 4.0, 8.5],
    "Centrale Lyon":                    [52000, 95, 3800, 14, 4.2, 8.0],
    "Centrale Lille":                   [48000, 93, 3500, 16, 3.8, 7.5],
    "Centrale Nantes":                  [49000, 94, 3200, 18, 4.5, 8.0],
    "Centrale Marseille":               [46000, 91, 3000, 17, 3.5, 7.0],

    # ──────── Mines ────────
    "Mines Paris (PSL)":                [60000, 98, 5000, 10, 3.5, 7.0],
    "Mines Saint-Étienne":              [47000, 92, 2800, 20, 4.0, 7.5],
    "Mines Nancy":                      [46000, 91, 2500, 19, 3.8, 7.0],
    "IMT Atlantique":                   [48000, 93, 2600, 22, 4.5, 7.5],
    "IMT Mines Albi":                   [43000, 89, 2200, 24, 4.2, 6.5],

    # ──────── Groupe INSA ────────
    "INSA Lyon":                        [45000, 94, 1200, 30, 4.5, 9.0],
    "INSA Toulouse":                    [44000, 92, 1100, 28, 4.3, 8.5],
    "INSA Rennes":                      [43000, 91, 1000, 27, 4.0, 8.0],
    "INSA Rouen":                       [42000, 90, 1000, 26, 3.8, 7.5],
    "INSA Strasbourg":                  [43000, 91, 1100, 25, 4.0, 7.5],

    # ──────── Réseau Polytech ────────
    "Polytech Nice Sophia":             [38000, 88,  800, 25, 3.0, 7.5],
    "Polytech Montpellier":             [37000, 87,  700, 28, 3.2, 7.0],
    "Polytech Grenoble":                [39000, 89,  900, 24, 3.5, 7.5],
    "Polytech Nantes":                  [38000, 88,  750, 26, 3.3, 7.0],
    "Polytech Lille":                   [37000, 87,  700, 27, 3.0, 6.5],

    # ──────── Universités de Technologie ────────
    "UTC (Compiègne)":                  [47000, 93, 1800, 22, 4.0, 8.5],
    "UTT (Troyes)":                     [42000, 91, 1500, 22, 4.0, 8.0],
    "UTBM (Belfort-Montbéliard)":       [40000, 89, 1300, 23, 3.5, 7.5],

    # ──────── Grandes écoles d'excellence ────────
    "ISAE-SUPAERO":                     [55000, 96, 4000, 11, 4.5, 8.0],
    "ENSTA Paris":                      [53000, 95, 3500, 14, 4.0, 7.0],
    "ENSAE Paris":                      [57000, 96, 4200,  9, 3.0, 6.0],
    "Télécom Paris":                    [56000, 97, 4800, 13, 4.0, 7.5],
    "Télécom SudParis":                 [48000, 92, 3600, 16, 3.8, 7.0],

    # ──────── Arts et Métiers ────────
    "Arts et Métiers (ENSAM)":          [46000, 93, 2500, 20, 3.5, 8.5],
    "Arts et Métiers Lille":            [44000, 91, 2300, 21, 3.3, 8.0],

    # ──────── Spécialisées Informatique / Numérique ────────
    "ENSIMAG (Grenoble INP)":           [52000, 95, 3000, 15, 3.5, 6.5],
    "ENSEEIHT (Toulouse INP)":          [49000, 93, 2800, 17, 3.8, 7.0],
    "ENSEIRB-MATMECA (Bordeaux INP)":   [48000, 92, 2700, 16, 3.5, 7.0],
    "EPITA":                            [45000, 92,10500, 15, 2.5, 8.5],
    "EFREI":                            [39000, 87, 9500, 18, 2.0, 9.0],

    # ──────── Post-bac privées ────────
    "ECE Paris":                        [40000, 89,10000, 20, 2.5, 8.5],
    "ESIEE Paris":                      [41000, 90, 8500, 19, 2.8, 7.5],
    "ESME Sudria":                      [38000, 86, 9000, 17, 2.2, 7.0],
    "ESILV (Léonard de Vinci)":         [42000, 90,11000, 16, 2.5, 8.0],
    "EPF":                              [40000, 88, 9500, 22, 3.0, 7.5],

    # ──────── Chimie / Matériaux ────────
    "Chimie ParisTech (PSL)":           [50000, 93, 3000, 13, 4.5, 6.0],
    "ESPCI Paris (PSL)":                [54000, 96, 1500,  8, 4.8, 5.5],
    "ENSCM (Montpellier)":              [41000, 89, 1800, 22, 4.0, 6.5],

    # ──────── Agro / Bio ────────
    "AgroParisTech":                    [44000, 91, 2000, 18, 5.0, 7.5],
    "ENSAT (Toulouse)":                 [39000, 87, 1200, 25, 4.5, 7.0],

    # ──────── Génie civil / BTP ────────
    "ESTP Paris":                       [45000, 93, 8000, 15, 3.0, 8.0],
    "ENTPE (Lyon)":                     [43000, 90, 1500, 20, 3.8, 6.5],

    # ──────── Autres écoles reconnues ────────
    "ENSC Cognitique (Bordeaux)":       [41000, 88, 1800, 30, 3.5, 7.5],
    "ESTIA (Bidart)":                   [40000, 88, 5500, 20, 3.5, 8.0],
    "EIGSI (La Rochelle)":              [38000, 86, 7500, 22, 3.0, 7.5],
}


# =============================================================================
# █  SECTION 2 — PARAMÈTRES DES MÉTHODES AMD                                 █
# =============================================================================

# Noms et unités d'affichage des 6 critères
CRITERE_NOMS   = ["Salaire", "Emploi 6 mois", "Coût total",
                  "Diversité sociale", "Engagement DD&RS", "Vie associative"]
CRITERE_CODES  = ["g1", "g2", "g3", "g4", "g5", "g6"]
CRITERE_UNITES = ["€/an", "%", "€ (3 ans)", "%", "/5", "/10"]
CRITERE_BORNES = ["35k – 60k", "85 – 100", "0 – 15 000",
                  "5 – 40", "1 – 5", "1 – 10"]

# True = critère à maximiser ; False = à minimiser
MAXIMISER = [True, True, False, True, True, True]

# Vecteur OWA par rang (du meilleur critère au pire)  — source : rapport AMD v1
W_OWA = [0.05, 0.15, 0.20, 0.20, 0.20, 0.20]

# Indices d'interaction du modèle de Choquet 2-additif (Grabisch)
INTERACTIONS_CHOQUET = {
    (0, 1): -0.05,   # I(g1, g2) — redondance salaire / emploi
    (3, 5): +0.05,   # I(g4, g6) — synergie diversité / vie associative
}

# Seuils ELECTRE Is : q (indifférence), p (préférence), v (veto si applicable)
SEUILS_ELECTRE = {
    0: {'q': 1500, 'p': 3000, 'v': 10000},   # g1  Salaire (€/an)
    1: {'q': 1.0,  'p': 3.0,  'v': 8.0},     # g2  Emploi (%)
    2: {'q': 500,  'p': 1500, 'v': 5000},    # g3  Coût (€)
    3: {'q': 2.0,  'p': 5.0},                # g4  Diversité (%) — pas de veto
    4: {'q': 0.3,  'p': 0.8},                # g5  DD&RS (/5) — pas de veto
    5: {'q': 0.5,  'p': 1.5,  'v': 4.0},     # g6  Vie associative (/10)
}

# Seuil de concordance globale λ pour ELECTRE Is
LAMBDA_ELECTRE = 0.65


# =============================================================================
# █  SECTION 3 — MOTEUR DE CALCUL : 5 MÉTHODES AMD                           █
# =============================================================================

def normaliser_minmax(ecoles):
    """
    Normalisation min-max des performances brutes vers [0 ; 100].

      • Critère à maximiser  : u_j(a) = (g_j(a) − min_j) / (max_j − min_j) × 100
      • Critère à minimiser  : u_j(a) = (max_j − g_j(a)) / (max_j − min_j) × 100

    Args :
        ecoles : dict { nom : [g1, …, g6] }
    Retour :
        dict { nom : [u1, …, u6] }  avec  u_j ∈ [0, 100]
    """
    noms = list(ecoles.keys())
    mins = [min(ecoles[n][j] for n in noms) for j in range(6)]
    maxs = [max(ecoles[n][j] for n in noms) for j in range(6)]

    utilites = {}
    for nom in noms:
        u = []
        for j in range(6):
            amp = maxs[j] - mins[j]
            if amp == 0:
                u.append(50.0)
            elif MAXIMISER[j]:
                u.append((ecoles[nom][j] - mins[j]) / amp * 100)
            else:
                u.append((maxs[j] - ecoles[nom][j]) / amp * 100)
        utilites[nom] = u
    return utilites


def _normer_poids(poids):
    """Normalise une liste de poids pour qu'elle somme à 1.
    Retombe sur 1/6 uniforme si tout est nul (cas pathologique)."""
    s = sum(poids)
    return [1/6] * 6 if s == 0 else [w / s for w in poids]


def methode_somme_ponderee(utilites, poids):
    """
    Somme Pondérée — agrégation compensatoire classique.
        S(a) = Σ_j  w_j × u_j(a)
    """
    w = _normer_poids(poids)
    scores = [(nom, sum(w[j] * u[j] for j in range(6)))
              for nom, u in utilites.items()]
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def methode_owa(utilites, poids):
    """
    Opérateur OWA de Yager.

    Les utilités sont d'abord pondérées par les poids utilisateur, puis
    triées par ordre décroissant et combinées via le vecteur W_OWA.
    Le vecteur W = (0.05, 0.15, 0.20, 0.20, 0.20, 0.20) accorde une pénalité
    au meilleur score → favorise les profils ÉQUILIBRÉS.
    """
    w = _normer_poids(poids)
    scores = []
    for nom, u in utilites.items():
        # On ramène à l'échelle [0, 100] via le facteur ×6 (poids initiaux ≈ 1/6)
        u_pond = [w[j] * u[j] * 6 for j in range(6)]
        u_tri  = sorted(u_pond, reverse=True)
        scores.append((nom, sum(W_OWA[k] * u_tri[k] for k in range(6))))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def methode_choquet(utilites, poids):
    """
    Intégrale de Choquet — modèle 2-additif de Grabisch.

        C(a) = Σ_i φ_i × u_i(a)
              + Σ_{I_ij > 0} I_ij × min(u_i, u_j)        (synergie)
              + Σ_{I_ij < 0} |I_ij| × max(u_i, u_j) × −1 (redondance)

    Valeurs de Shapley φ_i = poids des curseurs.
    """
    shap = _normer_poids(poids)
    scores = []
    for nom, u in utilites.items():
        s = sum(shap[j] * u[j] for j in range(6))
        for (i, j), I_ij in INTERACTIONS_CHOQUET.items():
            if I_ij > 0:
                s += I_ij * min(u[i], u[j])   # synergie : récompense le min
            else:
                s += I_ij * max(u[i], u[j])   # redondance : pénalise le max
        scores.append((nom, s))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def methode_min(utilites, poids):
    """
    Méthode du Min (Maximin de Wald) — logique pessimiste pure.
        S(a) = min_j  { w_j × u_j(a) × 6 }
    Aucune compensation : une seule faiblesse condamne l'école.
    """
    w = _normer_poids(poids)
    scores = [(nom, min(w[j] * u[j] * 6 for j in range(6)))
              for nom, u in utilites.items()]
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def methode_electre_is(ecoles, poids):
    """
    ELECTRE Is — méthode de surclassement non compensatoire.

    Pour chaque paire (a, b) :
        1) Concordance partielle  c_j(a, b)  pour chaque critère
        2) Concordance globale    C(a, b) = Σ w_j × c_j(a, b)
        3) Discordance partielle  d_j(a, b)  si veto défini
        4) Crédibilité            σ(a, b)   = C × Π ajustement veto
        5) Surclassement          a S b  ⇔  σ(a, b) ≥ λ

    Score net = (nb d'écoles surclassées par a) − (nb d'écoles surclassant a)
    """
    noms = list(ecoles.keys())
    n = len(noms)
    w = _normer_poids(poids)

    def c_part(ga, gb, j):
        q, p = SEUILS_ELECTRE[j]['q'], SEUILS_ELECTRE[j]['p']
        diff = (ga - gb) if MAXIMISER[j] else (gb - ga)
        if diff >= -q: return 1.0
        if diff <= -p: return 0.0
        return (diff + p) / (p - q)

    def d_part(ga, gb, j):
        s = SEUILS_ELECTRE[j]
        if 'v' not in s: return 0.0
        p, v = s['p'], s['v']
        diff = (gb - ga) if MAXIMISER[j] else (ga - gb)
        if diff <= p: return 0.0
        if diff >= v: return 1.0
        return (diff - p) / (v - p)

    # Matrice de surclassement
    surclasse = [[False] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if i == k:
                continue
            a, b = ecoles[noms[i]], ecoles[noms[k]]
            C = sum(w[j] * c_part(a[j], b[j], j) for j in range(6))
            sigma = C
            for j in range(6):
                d = d_part(a[j], b[j], j)
                if d > C:
                    sigma = sigma * (1.0 - d) / (1.0 - C) if C < 1.0 else 0.0
            if sigma >= LAMBDA_ELECTRE:
                surclasse[i][k] = True

    scores = []
    for i in range(n):
        plus  = sum(1 for k in range(n) if surclasse[i][k])
        moins = sum(1 for k in range(n) if surclasse[k][i])
        scores.append((noms[i], plus - moins))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


# =============================================================================
# █  SECTION 4 — DESIGN SYSTEM : PALETTE, ICÔNES, HELPERS CANVAS             █
# =============================================================================

# ── Palette « Aurora » — moderne, douce, claire ──
P = {
    # Surfaces
    'bg':         '#F4F6FB',   # arrière-plan général (très léger gris bleuté)
    'surface':    '#FFFFFF',   # cartes
    'surface_2':  '#F8FAFD',   # zone alternée / lignes paires
    'overlay':    '#EEF2FF',   # halo doux (sélection / 1ère ligne)
    # Header dégradé
    'h1':         '#1E1B4B',   # indigo profond
    'h2':         '#4338CA',   # indigo
    'h3':         '#7C3AED',   # violet
    # Couleur de marque
    'primary':    '#6366F1',
    'primary_d':  '#4F46E5',
    'primary_dd': '#4338CA',
    'accent':     '#EC4899',   # rose accent
    # Sémantique
    'success':    '#10B981',
    'success_d':  '#059669',
    'warning':    '#F59E0B',
    'danger':     '#EF4444',
    # Texte
    'text':       '#0F172A',
    'text_2':     '#475569',
    'text_3':     '#94A3B8',
    'text_inv':   '#FFFFFF',
    'text_inv_2': '#C7D2FE',
    # Bordures
    'border':     '#E2E8F0',
    'border_2':   '#CBD5E1',
    'border_l':   '#F1F5F9',
    # Médailles
    'gold':       '#F59E0B',
    'silver':     '#94A3B8',
    'bronze':     '#B45309',
    # Track de slider
    'track':      '#E0E7FF',
}

# Couleur dédiée à chaque critère (utilisée pour sliders et barres de score)
CRIT_COULEURS = [
    '#EC4899',   # g1 Salaire        — rose
    '#3B82F6',   # g2 Emploi         — bleu
    '#EF4444',   # g3 Coût           — rouge (à minimiser)
    '#10B981',   # g4 Diversité      — vert
    '#06B6D4',   # g5 DD&RS          — cyan
    '#F59E0B',   # g6 Vie associative — ambre
]

# Icônes (emoji) associées à chaque critère
CRIT_ICONES = ['💰', '💼', '🏛️', '🤝', '🌱', '🎉']

# Fontes
FONT_FAM = "Segoe UI"
F_DISPLAY = (FONT_FAM, 26, "bold")
F_TITLE   = (FONT_FAM, 18, "bold")
F_H1      = (FONT_FAM, 14, "bold")
F_H2      = (FONT_FAM, 11, "bold")
F_BODY    = (FONT_FAM, 10)
F_BODY_B  = (FONT_FAM, 10, "bold")
F_SMALL   = (FONT_FAM, 9)
F_SMALL_B = (FONT_FAM, 9, "bold")
F_CAPTION = (FONT_FAM, 8)
F_NUM_BIG = ("Consolas", 28, "bold")
F_NUM_MED = ("Consolas", 11, "bold")
F_NUM_SM  = ("Consolas", 9, "bold")


# ── Helpers de dessin sur Canvas ──

def _hex_to_rgb(c):
    """Convertit '#RRGGBB' → (R, G, B)."""
    c = c.lstrip('#')
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hex(r, g, b):
    """Convertit (R, G, B) → '#RRGGBB'."""
    return f'#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}'


def draw_h_gradient(canvas, x, y, w, h, c1, c2, c3=None):
    """
    Trace un dégradé HORIZONTAL sur le Canvas, de (x, y) à (x+w, y+h).
    Accepte 2 ou 3 couleurs (dégradé à 2 ou 3 paliers).
    """
    if c3 is None:
        r1, g1, b1 = _hex_to_rgb(c1)
        r2, g2, b2 = _hex_to_rgb(c2)
        for i in range(w):
            t = i / max(w - 1, 1)
            col = _rgb_to_hex(int(r1 + (r2 - r1) * t),
                              int(g1 + (g2 - g1) * t),
                              int(b1 + (b2 - b1) * t))
            canvas.create_line(x + i, y, x + i, y + h, fill=col)
    else:
        mid = w // 2
        draw_h_gradient(canvas, x, y, mid, h, c1, c2)
        draw_h_gradient(canvas, x + mid, y, w - mid, h, c2, c3)


def round_rect(canvas, x1, y1, x2, y2, r=12, **kwargs):
    """
    Dessine un rectangle aux coins arrondis sur un Canvas.
    Utilise un polygone smooth pour un rendu fluide.
    """
    r = max(0, min(r, abs(x2 - x1) // 2, abs(y2 - y1) // 2))
    if r <= 0:
        return canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1,
        x2, y1 + r, x2, y2 - r, x2, y2,
        x2 - r, y2, x1 + r, y2, x1, y2,
        x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# =============================================================================
# █  SECTION 5 — WIDGETS PERSONNALISÉS                                       █
# =============================================================================

class FancySlider(tk.Canvas):
    """
    Slider horizontal dessiné au Canvas avec :
      • un rail arrondi gris clair,
      • un remplissage à la couleur du critère,
      • un thumb circulaire blanc cerclé.
    Valeurs continues dans [0, 1], pas de 0.01.
    """

    THUMB_R = 9   # rayon du thumb

    def __init__(self, parent, variable, color, bg, width=210, height=26):
        super().__init__(parent, width=width, height=height,
                         bg=bg, highlightthickness=0, bd=0, cursor='hand2')
        self.var = variable
        self.color = color
        self.bg_color = bg
        self.w = width
        self.h = height
        self.pad = self.THUMB_R + 2
        self._draw()
        self.bind('<Button-1>', self._on_drag)
        self.bind('<B1-Motion>', self._on_drag)
        self.var.trace_add('write', lambda *a: self._draw())

    def _v_to_x(self, v):
        return self.pad + max(0.0, min(1.0, v)) * (self.w - 2 * self.pad)

    def _x_to_v(self, x):
        x = max(self.pad, min(self.w - self.pad, x))
        return round((x - self.pad) / (self.w - 2 * self.pad) * 100) / 100

    def _draw(self):
        self.delete('all')
        ym = self.h // 2
        # Rail (track)
        round_rect(self, self.pad, ym - 3, self.w - self.pad, ym + 3,
                   r=3, fill=P['track'], outline='')
        # Remplissage proportionnel
        v = self.var.get()
        xt = self._v_to_x(v)
        if v > 0.001:
            round_rect(self, self.pad, ym - 3, xt, ym + 3,
                       r=3, fill=self.color, outline='')
        # Ombre douce sous le thumb (offset 1 px vers le bas)
        self.create_oval(xt - self.THUMB_R, ym - self.THUMB_R + 1,
                         xt + self.THUMB_R, ym + self.THUMB_R + 1,
                         fill=P['border_2'], outline='')
        # Thumb : disque blanc cerclé de la couleur du critère
        self.create_oval(xt - self.THUMB_R, ym - self.THUMB_R,
                         xt + self.THUMB_R, ym + self.THUMB_R,
                         fill='#FFFFFF', outline=self.color, width=2)

    def _on_drag(self, e):
        self.var.set(self._x_to_v(e.x))


class SliderRow(tk.Frame):
    """
    Ligne complète d'un critère dans la sidebar :
        [icône]  Nom du critère              [valeur en %]
                 Bornes & sens
                 ────●─────────────  (FancySlider)
    """

    def __init__(self, parent, idx, var):
        super().__init__(parent, bg=P['surface'])
        self.idx = idx
        self.var = var
        color = CRIT_COULEURS[idx]

        # ── Ligne 1 : icône + nom + valeur numérique ──
        head = tk.Frame(self, bg=P['surface'])
        head.pack(fill='x')

        tk.Label(head, text=CRIT_ICONES[idx], font=(FONT_FAM, 14),
                 bg=P['surface']).pack(side='left')

        nom = tk.Label(head,
                       text=f"  {CRITERE_CODES[idx]}  {CRITERE_NOMS[idx]}",
                       font=F_BODY_B, fg=P['text'], bg=P['surface'])
        nom.pack(side='left')

        self.lbl_val = tk.Label(head, text=f"{var.get():.2f}",
                                font=F_NUM_MED, fg=color, bg=P['surface'])
        self.lbl_val.pack(side='right')

        var.trace_add('write', lambda *a: self.lbl_val.config(
            text=f"{self.var.get():.2f}"))

        # ── Ligne 2 : bornes et sens d'optimisation ──
        sens_txt = "▲ Maximiser" if MAXIMISER[idx] else "▼ Minimiser"
        sens_col = P['success_d'] if MAXIMISER[idx] else P['danger']

        meta = tk.Frame(self, bg=P['surface'])
        meta.pack(fill='x', pady=(2, 2))

        tk.Label(meta, text=f"{CRITERE_BORNES[idx]} {CRITERE_UNITES[idx]}",
                 font=F_CAPTION, fg=P['text_3'], bg=P['surface']
                 ).pack(side='left')

        tk.Label(meta, text=sens_txt, font=F_CAPTION, fg=sens_col,
                 bg=P['surface']).pack(side='right')

        # ── Ligne 3 : le slider ──
        FancySlider(self, var, color, bg=P['surface'],
                    width=340, height=24).pack(pady=(2, 0), anchor='w')


class MethodCard(tk.Frame):
    """
    Carte cliquable pour sélectionner une méthode AMD.
    Lorsqu'elle est sélectionnée :
        • bande de couleur primary sur le côté gauche,
        • fond bleu très pâle,
        • texte en gras + couleur primary_dd.
    """

    def __init__(self, parent, name, hint, value, group_var, on_pick):
        super().__init__(parent, bg=P['surface'])
        self.value = value
        self.group_var = group_var
        self.on_pick = on_pick

        # Barre verticale d'indicateur de sélection (3 px)
        self.bar = tk.Frame(self, width=4, bg=P['border'])
        self.bar.pack(side='left', fill='y')
        self.bar.pack_propagate(False)

        # Conteneur du texte
        self.box = tk.Frame(self, bg=P['surface'])
        self.box.pack(side='left', fill='both', expand=True,
                      padx=12, pady=8)

        self.lbl_name = tk.Label(self.box, text=name, font=F_BODY_B,
                                 bg=P['surface'], fg=P['text_2'], anchor='w')
        self.lbl_name.pack(fill='x')

        self.lbl_hint = tk.Label(self.box, text=hint, font=F_CAPTION,
                                 bg=P['surface'], fg=P['text_3'], anchor='w',
                                 wraplength=290, justify='left')
        self.lbl_hint.pack(fill='x')

        # Bindings : tous les widgets de la carte
        for w in (self, self.box, self.lbl_name, self.lbl_hint, self.bar):
            w.bind('<Button-1>', self._select)
            w.bind('<Enter>', self._enter)
            w.bind('<Leave>', self._leave)
            w.configure(cursor='hand2')

        group_var.trace_add('write', lambda *a: self._refresh())
        self._refresh()

    def _select(self, _=None):
        self.group_var.set(self.value)
        if self.on_pick:
            self.on_pick()

    def _enter(self, _=None):
        if self.group_var.get() != self.value:
            self._apply_bg(P['border_l'])

    def _leave(self, _=None):
        if self.group_var.get() != self.value:
            self._apply_bg(P['surface'])

    def _apply_bg(self, color):
        self.configure(bg=color)
        self.box.configure(bg=color)
        self.lbl_name.configure(bg=color)
        self.lbl_hint.configure(bg=color)

    def _refresh(self):
        is_sel = (self.group_var.get() == self.value)
        if is_sel:
            self.bar.configure(bg=P['primary'])
            self._apply_bg(P['overlay'])
            self.lbl_name.configure(fg=P['primary_dd'])
            self.lbl_hint.configure(fg=P['text_2'])
        else:
            self.bar.configure(bg=P['border'])
            self._apply_bg(P['surface'])
            self.lbl_name.configure(fg=P['text_2'])
            self.lbl_hint.configure(fg=P['text_3'])


class PrimaryButton(tk.Canvas):
    """
    Bouton d'action principal dessiné au Canvas :
        • forme arrondie,
        • dégradé indigo → violet,
        • effets de survol (assombri) et de clic (très assombri).
    """

    def __init__(self, parent, text, command, bg, width=340, height=52):
        super().__init__(parent, width=width, height=height,
                         bg=bg, highlightthickness=0, bd=0, cursor='hand2')
        self.text = text
        self.command = command
        self.w = width
        self.h = height
        self.bg_color = bg
        self._state = 'normal'
        self._draw()
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def _colors(self):
        if self._state == 'press':
            return P['primary_dd'], '#3730A3'
        if self._state == 'hover':
            return P['primary_d'], P['primary_dd']
        return P['primary'], P['primary_d']

    def _draw(self):
        self.delete('all')
        c1, c2 = self._colors()
        # Ombre légère
        round_rect(self, 2, 4, self.w - 2, self.h, r=14,
                   fill=P['border_2'], outline='')
        # Corps du bouton (dégradé simulé par 2 rectangles arrondis)
        round_rect(self, 0, 0, self.w - 4, self.h - 4, r=14,
                   fill=c1, outline='')
        # Bande inférieure plus foncée (illusion de dégradé)
        round_rect(self, 0, self.h // 2 - 2, self.w - 4, self.h - 4, r=14,
                   fill=c2, outline='')
        # Couvercle supérieur clair (illusion de dégradé)
        round_rect(self, 0, 0, self.w - 4, self.h // 2 + 2, r=14,
                   fill=c1, outline='')
        # Texte
        self.create_text((self.w - 4) // 2, (self.h - 4) // 2,
                         text=self.text, font=(FONT_FAM, 12, "bold"),
                         fill='#FFFFFF')

    def _on_enter(self, _):
        self._state = 'hover'
        self._draw()

    def _on_leave(self, _):
        self._state = 'normal'
        self._draw()

    def _on_press(self, _):
        self._state = 'press'
        self._draw()

    def _on_release(self, _):
        self._state = 'hover'
        self._draw()
        if self.command:
            self.command()


class HeroCard(tk.Frame):
    """
    Carte « Recommandation majeure » avec :
        • badge médaille d'or animé,
        • nom de l'école en gros,
        • méthode appliquée,
        • barre de progression colorée pour le score,
        • valeur numérique en grand format.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=P['surface'])

        # ── Canvas de fond (dégradé bleu pâle + badge médaille) ──
        self.bg = tk.Canvas(self, height=170, bg=P['surface'],
                            highlightthickness=0, bd=0)
        self.bg.pack(fill='both', expand=True)

        # Marqueurs pour redessiner
        self.bg.bind('<Configure>', lambda e: self._render())

        # États
        self.nom = "— Lancez le calcul pour découvrir votre école —"
        self.methode = ""
        self.score = 0.0
        self.score_txt = "—"
        self.is_electre = False

    def set_result(self, nom, score, methode):
        self.nom = nom
        self.methode = methode
        self.is_electre = (methode == "ELECTRE Is")
        if self.is_electre:
            # Score net : nombre signé d'écoles surclassées
            self.score = max(0.0, min(100.0,
                            (score + len(ECOLES)) / (2 * len(ECOLES)) * 100))
            sign = "+" if score >= 0 else ""
            self.score_txt = f"{sign}{int(score)}"
        else:
            self.score = max(0.0, min(100.0, score))
            self.score_txt = f"{score:.1f}"
        self._render()

    def reset(self):
        self.nom = "— Lancez le calcul pour découvrir votre école —"
        self.methode = ""
        self.score = 0.0
        self.score_txt = "—"
        self.is_electre = False
        self._render()

    def _render(self):
        self.bg.delete('all')
        W = self.bg.winfo_width() or 700
        H = self.bg.winfo_height() or 170

        # Fond dégradé doux (overlay violet → blanc cassé)
        draw_h_gradient(self.bg, 0, 0, W, H, P['overlay'], '#FAF5FF')

        # Bordure arrondie subtile
        round_rect(self.bg, 1, 1, W - 1, H - 1, r=16,
                   fill='', outline=P['border'], width=1)

        # ── Médaille (cercle doré avec couronne) ──
        cx, cy, r = 70, 70, 38
        # Lueur extérieure
        self.bg.create_oval(cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6,
                            fill='#FEF3C7', outline='')
        # Disque d'or
        self.bg.create_oval(cx - r, cy - r, cx + r, cy + r,
                            fill=P['gold'], outline='#D97706', width=2)
        # Reflet
        self.bg.create_oval(cx - r + 6, cy - r + 6, cx + r - 18, cy + r - 24,
                            fill='#FCD34D', outline='')
        # Couronne / symbole
        self.bg.create_text(cx, cy - 4, text="♛", font=(FONT_FAM, 28, "bold"),
                            fill='#FFFFFF')
        self.bg.create_text(cx, cy + 22, text="#1", font=(FONT_FAM, 10, "bold"),
                            fill='#7C2D12')

        # ── Étiquette « VOTRE RECOMMANDATION » ──
        self.bg.create_text(135, 30, text="VOTRE RECOMMANDATION",
                            font=(FONT_FAM, 9, "bold"),
                            fill=P['primary_dd'], anchor='w')

        # ── Nom de l'école (taille adaptée si trop long) ──
        font_size = 22 if len(self.nom) < 32 else (18 if len(self.nom) < 40 else 15)
        self.bg.create_text(135, 60, text=self.nom,
                            font=(FONT_FAM, font_size, "bold"),
                            fill=P['text'], anchor='w')

        # ── Méthode utilisée ──
        if self.methode:
            self.bg.create_text(135, 90,
                                text=f"Modèle appliqué : {self.methode}",
                                font=F_SMALL, fill=P['text_2'], anchor='w')

        # ── Barre de score (à droite) ──
        bar_x = 135
        bar_y = 120
        bar_w = max(200, W - bar_x - 180)
        bar_h = 14
        # Fond du rail
        round_rect(self.bg, bar_x, bar_y, bar_x + bar_w, bar_y + bar_h,
                   r=7, fill='#FFFFFF', outline=P['border'], width=1)
        # Remplissage
        fill_w = int(bar_w * self.score / 100)
        if fill_w > 6:
            # Couleur selon le score
            if self.score >= 75:
                col = P['success']
            elif self.score >= 50:
                col = P['primary']
            elif self.score >= 25:
                col = P['warning']
            else:
                col = P['danger']
            round_rect(self.bg, bar_x + 2, bar_y + 2,
                       bar_x + fill_w - 2, bar_y + bar_h - 2,
                       r=6, fill=col, outline='')

        # Libellé de la barre
        self.bg.create_text(bar_x, bar_y - 14,
                            text=("SCORE NET" if self.is_electre
                                  else "SCORE D'AGRÉGATION"),
                            font=(FONT_FAM, 8, "bold"),
                            fill=P['text_3'], anchor='w')
        self.bg.create_text(bar_x + bar_w, bar_y - 14,
                            text=("(normalisé)" if self.is_electre
                                  else "/ 100"),
                            font=(FONT_FAM, 8),
                            fill=P['text_3'], anchor='e')

        # ── Grand score à droite ──
        self.bg.create_text(W - 80, 70, text=self.score_txt,
                            font=F_NUM_BIG, fill=P['primary_dd'])
        self.bg.create_text(W - 80, 105,
                            text=("score net" if self.is_electre else "sur 100"),
                            font=F_CAPTION, fill=P['text_3'])


# =============================================================================
# █  SECTION 6 — FENÊTRE PRINCIPALE                                          █
# =============================================================================

class SimulateurAMD(tk.Tk):
    """Fenêtre principale du simulateur AMD v3.0."""

    def __init__(self):
        super().__init__()

        # ── Configuration de la fenêtre ──
        self.title("Simulateur AMD v3.0 — Choisis ton école d'ingénieurs")
        self.configure(bg=P['bg'])
        self.geometry("1480x920")
        self.minsize(1280, 820)

        # ── États ──
        # 6 poids initialisés à 1/6 (~0.17)
        self.poids_vars = [tk.DoubleVar(value=round(1/6, 2)) for _ in range(6)]
        self.methode_var = tk.StringVar(value="Somme Pondérée")

        # ── Construction ──
        self._build_header()
        self._build_body()

    # -------------------------------------------------------------------------
    #  HEADER — barre supérieure avec dégradé indigo → violet
    # -------------------------------------------------------------------------
    def _build_header(self):
        """Header de 84 px avec dégradé et titre."""
        self.header_h = 84
        self.header = tk.Canvas(self, height=self.header_h,
                                bg=P['h2'], highlightthickness=0, bd=0)
        self.header.pack(fill='x', side='top')
        self.header.bind('<Configure>', lambda e: self._render_header())

    def _render_header(self):
        """Redessine le header (appelé sur redimensionnement)."""
        self.header.delete('all')
        W = self.header.winfo_width()
        H = self.header_h

        # Dégradé à 3 paliers : indigo profond → indigo → violet
        draw_h_gradient(self.header, 0, 0, W, H, P['h1'], P['h2'], P['h3'])

        # Décor : 3 cercles flous à droite (sphères stylisées)
        for cx, cy, r, col in [
            (W - 90,  18, 50, '#A78BFA'),
            (W - 180, 50, 35, '#C4B5FD'),
            (W - 60,  60, 22, '#DDD6FE'),
        ]:
            self.header.create_oval(cx - r, cy - r, cx + r, cy + r,
                                    fill=col, outline='', stipple='gray25')

        # Pastille « AMD » à gauche
        round_rect(self.header, 24, 18, 88, 66, r=14,
                   fill='#FFFFFF', outline='')
        self.header.create_text(56, 42, text="AMD", font=(FONT_FAM, 16, "bold"),
                                fill=P['primary_dd'])

        # Titre principal
        self.header.create_text(108, 30, anchor='w',
                                text="Décision Multicritère — Studio des Écoles",
                                font=(FONT_FAM, 18, "bold"), fill='#FFFFFF')
        # Sous-titre
        self.header.create_text(108, 56, anchor='w',
                                text="50 écoles d'ingénieurs  ·  5 méthodes AMD  ·  6 critères",
                                font=(FONT_FAM, 10), fill=P['text_inv_2'])

        # Compteur d'écoles à droite (pastille)
        n = len(ECOLES)
        right_x = W - 240
        round_rect(self.header, right_x, 22, right_x + 130, 62, r=20,
                   fill='', outline='#FFFFFF', width=2)
        self.header.create_text(right_x + 26, 42, text=str(n),
                                font=(FONT_FAM, 22, "bold"), fill='#FFFFFF')
        self.header.create_text(right_x + 50, 36, anchor='w',
                                text="écoles",
                                font=(FONT_FAM, 9, "bold"), fill='#FFFFFF')
        self.header.create_text(right_x + 50, 50, anchor='w',
                                text="dans la base",
                                font=(FONT_FAM, 8), fill=P['text_inv_2'])

    # -------------------------------------------------------------------------
    #  BODY — disposition à 2 colonnes : sidebar (380 px) + main
    # -------------------------------------------------------------------------
    def _build_body(self):
        """Construit la zone sous le header (sidebar + main)."""
        body = tk.Frame(self, bg=P['bg'])
        body.pack(fill='both', expand=True, padx=16, pady=16)

        # Sidebar gauche (largeur fixe)
        self.sidebar = tk.Frame(body, bg=P['bg'], width=400)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)

        # Zone principale droite (étirable)
        self.main = tk.Frame(body, bg=P['bg'])
        self.main.pack(side='left', fill='both', expand=True, padx=(16, 0))

        self._build_sidebar()
        self._build_main()

    # =========================================================================
    #  SIDEBAR
    # =========================================================================
    def _build_sidebar(self):
        """Construit la sidebar : poids + sélection méthode + bouton."""

        # ── Carte 1 : poids des critères ──
        card_w = self._card(self.sidebar, "Votre profil étudiant",
                            "Pondérez l'importance de chaque critère")
        card_w.pack(fill='x', pady=(0, 14))

        for j in range(6):
            row = SliderRow(card_w, j, self.poids_vars[j])
            row.pack(fill='x', padx=18, pady=6)
            if j < 5:
                tk.Frame(card_w, bg=P['border_l'], height=1
                         ).pack(fill='x', padx=18)

        # Boutons rapides d'attribution des poids
        quick = tk.Frame(card_w, bg=P['surface'])
        quick.pack(fill='x', padx=18, pady=(10, 16))
        tk.Label(quick, text="Profils types :", font=F_CAPTION,
                 fg=P['text_3'], bg=P['surface']
                 ).pack(side='left')
        for label, preset in [("Équilibré", "balance"),
                              ("Salaire+", "money"),
                              ("Étudiant", "student"),
                              ("Eco", "eco")]:
            tk.Label(quick, text=f"  {label}", font=F_SMALL_B,
                     fg=P['primary_d'], bg=P['surface'], cursor='hand2'
                     ).pack(side='left', padx=2)
            quick.winfo_children()[-1].bind(
                '<Button-1>', lambda e, p=preset: self._preset(p))

        # ── Carte 2 : méthode de décision ──
        card_m = self._card(self.sidebar, "Modèle de décision",
                            "Choisissez la méthode AMD à appliquer")
        card_m.pack(fill='x', pady=(0, 14))

        methodes = [
            ("Somme Pondérée",      "Compensation totale, agrégation classique"),
            ("Opérateur OWA",       "Favorise les profils équilibrés (W rang)"),
            ("Intégrale de Choquet", "Modélise redondance & synergie entre critères"),
            ("Méthode du Min",      "Pessimiste pur — aucune compensation"),
            ("ELECTRE Is",          "Surclassement non compensatoire avec vetos"),
        ]

        cards_box = tk.Frame(card_m, bg=P['surface'])
        cards_box.pack(fill='x', padx=14, pady=(0, 14))
        for name, hint in methodes:
            mc = MethodCard(cards_box, name, hint, name,
                            self.methode_var, on_pick=None)
            mc.pack(fill='x', pady=3)

        # ── Bouton de lancement ──
        btn_holder = tk.Frame(self.sidebar, bg=P['bg'])
        btn_holder.pack(fill='x', pady=(0, 4))
        self.btn = PrimaryButton(
            btn_holder,
            text="▶  LANCER LA RECHERCHE DU COMPROMIS",
            command=self._lancer_calcul, bg=P['bg'],
            width=400, height=56)
        self.btn.pack()

        # ── Note de bas de sidebar ──
        tk.Label(self.sidebar,
                 text="M1 MIAGE  ·  Décision Multicritère  ·  Université Paris-Dauphine",
                 font=F_CAPTION, fg=P['text_3'], bg=P['bg']
                 ).pack(side='bottom', pady=(10, 0))

    # =========================================================================
    #  ZONE PRINCIPALE — Hero + Stats + Top 5
    # =========================================================================
    def _build_main(self):
        """Construit la zone principale (3 cartes empilées)."""

        # ── Carte Hero : recommandation #1 ──
        hero_card = self._card(self.main, "")
        hero_card.pack(fill='x', pady=(0, 14))
        # Supprime l'en-tête pour laisser le Hero gérer son propre rendu
        hero_card.pack_propagate(False)
        hero_card.configure(height=190)
        for w in hero_card.winfo_children():
            w.destroy()
        self.hero = HeroCard(hero_card)
        self.hero.pack(fill='both', expand=True, padx=18, pady=18)

        # ── Carte Stats détaillées ──
        stats_card = self._card(
            self.main, "Performances détaillées de la recommandation",
            "Performances brutes et utilités normalisées par critère")
        stats_card.pack(fill='x', pady=(0, 14))

        self.stats_box = tk.Frame(stats_card, bg=P['surface'])
        self.stats_box.pack(fill='x', padx=18, pady=(0, 18))
        self._build_stats_empty()

        # ── Carte Top 5 ──
        top_card = self._card(
            self.main, "Horizon des possibles",
            "Les 5 meilleures écoles selon votre profil")
        top_card.pack(fill='both', expand=True)

        self.top_box = tk.Frame(top_card, bg=P['surface'])
        self.top_box.pack(fill='both', expand=True, padx=18, pady=(0, 18))
        self._build_top_empty()

    # =========================================================================
    #  HELPERS — création d'une carte (titre + sous-titre + corps blanc)
    # =========================================================================
    def _card(self, parent, title, subtitle=""):
        """
        Crée une carte blanche avec bordure subtile et un header titre/sous-titre.
        Retourne le Frame du corps de la carte (à remplir par l'appelant).
        """
        outer = tk.Frame(parent, bg=P['border'])
        inner = tk.Frame(outer, bg=P['surface'])
        inner.pack(fill='both', expand=True, padx=1, pady=1)

        if title:
            head = tk.Frame(inner, bg=P['surface'])
            head.pack(fill='x', padx=18, pady=(16, 0))
            tk.Label(head, text=title, font=F_H1,
                     fg=P['text'], bg=P['surface']
                     ).pack(anchor='w')
            if subtitle:
                tk.Label(head, text=subtitle, font=F_SMALL,
                         fg=P['text_3'], bg=P['surface']
                         ).pack(anchor='w', pady=(2, 12))
            else:
                tk.Frame(head, bg=P['surface'], height=12).pack()

        return outer

    # =========================================================================
    #  STATS — barres horizontales colorées par critère
    # =========================================================================
    def _build_stats_empty(self):
        """Tableau de stats vide (placeholder)."""
        for w in self.stats_box.winfo_children():
            w.destroy()
        ph = tk.Label(self.stats_box,
                      text="Lancez le calcul pour voir le détail des performances.",
                      font=(FONT_FAM, 10, "italic"), fg=P['text_3'],
                      bg=P['surface'], pady=40)
        ph.pack()

    def _build_stats_filled(self, nom, utilites_ecole):
        """Affiche les 6 critères de l'école avec barre de progression."""
        for w in self.stats_box.winfo_children():
            w.destroy()
        perfs = ECOLES[nom]

        for j in range(6):
            row = tk.Frame(self.stats_box, bg=P['surface'])
            row.pack(fill='x', pady=4)

            # Icône colorée
            ic = tk.Label(row, text=CRIT_ICONES[j], font=(FONT_FAM, 14),
                          bg=P['surface'])
            ic.pack(side='left', padx=(0, 10))

            # Nom + code
            left = tk.Frame(row, bg=P['surface'], width=160)
            left.pack(side='left')
            left.pack_propagate(False)
            tk.Label(left, text=f"{CRITERE_CODES[j]}  {CRITERE_NOMS[j]}",
                     font=F_SMALL_B, fg=P['text'],
                     bg=P['surface']).pack(anchor='w')
            tk.Label(left, text=f"{CRITERE_UNITES[j]}",
                     font=F_CAPTION, fg=P['text_3'],
                     bg=P['surface']).pack(anchor='w')

            # Valeur brute
            perf_txt = self._format_brute(j, perfs[j])
            tk.Label(row, text=perf_txt, font=F_NUM_MED,
                     fg=P['text'], bg=P['surface'], width=14, anchor='e'
                     ).pack(side='left', padx=(0, 14))

            # Barre de progression de l'utilité normalisée
            u = utilites_ecole[j]
            bar = tk.Canvas(row, height=22, bg=P['surface'],
                            highlightthickness=0, bd=0)
            bar.pack(side='left', fill='x', expand=True)
            bar.bind('<Configure>', lambda e, b=bar, val=u,
                     c=CRIT_COULEURS[j]: self._draw_util_bar(b, val, c))

            # Valeur normalisée à droite
            col_u = (P['success_d'] if u >= 70
                     else P['warning'] if u >= 40 else P['danger'])
            tk.Label(row, text=f"{u:5.1f}", font=F_NUM_MED,
                     fg=col_u, bg=P['surface'], width=6, anchor='e'
                     ).pack(side='left', padx=(10, 0))

    def _format_brute(self, j, val):
        """Format d'affichage selon le critère."""
        if j == 0 or j == 2:
            return f"{val:,} €".replace(",", " ")
        if j == 1 or j == 3:
            return f"{val:.0f} %"
        if j == 4:
            return f"{val:.1f} / 5"
        return f"{val:.1f} / 10"

    def _draw_util_bar(self, canvas, value, color):
        """Trace une barre horizontale arrondie remplie à `value`%."""
        canvas.delete('all')
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 10 or h < 10:
            return
        # Rail
        round_rect(canvas, 0, h // 2 - 6, w, h // 2 + 6, r=6,
                   fill=P['border_l'], outline='')
        # Remplissage
        fill_w = int(w * max(0.0, min(100.0, value)) / 100)
        if fill_w > 6:
            round_rect(canvas, 0, h // 2 - 6, fill_w, h // 2 + 6, r=6,
                       fill=color, outline='')
        # Repère des 50 %
        canvas.create_line(w // 2, h // 2 - 9, w // 2, h // 2 + 9,
                           fill=P['border_2'], dash=(1, 2))

    # =========================================================================
    #  TOP 5 — liste des 5 meilleures écoles
    # =========================================================================
    def _build_top_empty(self):
        """Placeholder du Top 5."""
        for w in self.top_box.winfo_children():
            w.destroy()
        tk.Label(self.top_box,
                 text="Le classement s'affichera ici après le calcul.",
                 font=(FONT_FAM, 10, "italic"), fg=P['text_3'],
                 bg=P['surface'], pady=40).pack()

    def _build_top_filled(self, classement, utilites_dict, methode):
        """Construit la liste détaillée du Top 5."""
        for w in self.top_box.winfo_children():
            w.destroy()

        # En-tête de colonnes
        head = tk.Frame(self.top_box, bg=P['surface'])
        head.pack(fill='x', pady=(0, 6))
        tk.Label(head, text="Rang", font=F_CAPTION, fg=P['text_3'],
                 bg=P['surface'], width=5, anchor='w').pack(side='left')
        tk.Label(head, text="École", font=F_CAPTION, fg=P['text_3'],
                 bg=P['surface'], anchor='w').pack(side='left', padx=(10, 0))
        tk.Label(head, text="Score", font=F_CAPTION, fg=P['text_3'],
                 bg=P['surface'], width=8, anchor='e').pack(side='right')
        tk.Label(head, text="Forces", font=F_CAPTION, fg=P['text_3'],
                 bg=P['surface'], width=24, anchor='w').pack(side='right',
                                                              padx=(0, 24))

        # Médailles
        medailles = [
            ("🥇", P['gold']),
            ("🥈", P['silver']),
            ("🥉", P['bronze']),
            ("4", P['text_3']),
            ("5", P['text_3']),
        ]

        for rang in range(min(5, len(classement))):
            nom, score = classement[rang]
            badge, badge_col = medailles[rang]
            is_top = (rang == 0)

            # Conteneur ligne (avec halo pour la 1ère place)
            row_bg = P['overlay'] if is_top else (
                P['surface_2'] if rang % 2 else P['surface'])

            row_wrap = tk.Frame(self.top_box, bg=row_bg)
            row_wrap.pack(fill='x', pady=2)

            row = tk.Frame(row_wrap, bg=row_bg)
            row.pack(fill='x', padx=10, pady=8)

            # Badge médaille
            badge_lbl = tk.Label(row, text=badge,
                                 font=(FONT_FAM, 16, "bold")
                                 if rang < 3 else F_NUM_MED,
                                 fg=badge_col, bg=row_bg, width=4, anchor='w')
            badge_lbl.pack(side='left')

            # Nom (en gras pour la 1ère)
            name_font = ((FONT_FAM, 12, "bold") if is_top
                         else (FONT_FAM, 10, "bold"))
            tk.Label(row, text=nom, font=name_font,
                     fg=P['primary_dd'] if is_top else P['text'],
                     bg=row_bg, anchor='w'
                     ).pack(side='left', padx=(2, 0))

            # Score (formaté selon la méthode)
            if methode == "ELECTRE Is":
                sign = "+" if score >= 0 else ""
                score_txt = f"{sign}{int(score)}"
            else:
                score_txt = f"{score:.1f}"
            score_col = (P['primary_dd'] if is_top else P['success_d'])
            tk.Label(row, text=score_txt, font=F_NUM_MED,
                     fg=score_col, bg=row_bg, width=8, anchor='e'
                     ).pack(side='right')

            # Forces (2 meilleurs critères normalisés)
            forces_txt = self._top2_forces(nom, utilites_dict)
            tk.Label(row, text=forces_txt, font=F_SMALL,
                     fg=P['text_2'], bg=row_bg, width=24, anchor='w'
                     ).pack(side='right', padx=(0, 24))

    def _top2_forces(self, nom, utilites_dict):
        """Retourne une chaîne avec les 2 critères les plus forts."""
        if nom not in utilites_dict:
            return ""
        u = utilites_dict[nom]
        idx_tri = sorted(range(6), key=lambda j: u[j], reverse=True)
        a, b = idx_tri[0], idx_tri[1]
        noms_court = ["Salaire", "Emploi", "Coût⁻¹",
                      "Diversité", "DD&RS", "Vie asso."]
        return f"{CRIT_ICONES[a]} {noms_court[a]}   {CRIT_ICONES[b]} {noms_court[b]}"

    # =========================================================================
    #  PROFILS PRÉSÉLECTIONNÉS — boutons rapides
    # =========================================================================
    def _preset(self, kind):
        """
        Applique un profil-type aux 6 poids.
            balance : tous à 1/6
            money   : salaire et emploi prédominants
            student : vie associative + diversité prédominants
            eco     : DD&RS prédominant, coût modéré
        """
        if kind == "balance":
            vals = [1/6] * 6
        elif kind == "money":
            vals = [0.40, 0.30, 0.05, 0.05, 0.05, 0.15]
        elif kind == "student":
            vals = [0.10, 0.10, 0.10, 0.25, 0.10, 0.35]
        else:  # eco
            vals = [0.10, 0.10, 0.20, 0.15, 0.35, 0.10]
        for i, v in enumerate(vals):
            self.poids_vars[i].set(round(v, 2))

    # =========================================================================
    #  CALCUL — bouton principal
    # =========================================================================
    def _lancer_calcul(self):
        """Calcule le classement avec la méthode et les poids sélectionnés."""
        poids = [v.get() for v in self.poids_vars]
        utilites = normaliser_minmax(ECOLES)

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
            classement = methode_electre_is(ECOLES, poids)
        else:
            return

        if not classement:
            return

        nom_top1, score_top1 = classement[0]

        # ── Mise à jour des 3 cartes ──
        self.hero.set_result(nom_top1, score_top1, methode)
        self._build_stats_filled(nom_top1, utilites[nom_top1])
        self._build_top_filled(classement, utilites, methode)


# =============================================================================
# █  SECTION 7 — LANCEMENT                                                   █
# =============================================================================

if __name__ == "__main__":
    app = SimulateurAMD()
    app.mainloop()
