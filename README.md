# 🎓 Aide à la Décision Multicritère — Choix d'école d'ingénieurs

> Projet académique du **M1 MIAGE** (Université Paris-Dauphine · PSL) — cours de **Décision Multicritère**.
> Application interactive permettant à un futur étudiant de classer **50 écoles d'ingénieurs françaises** selon **5 méthodes d'agrégation AMD** et son propre profil de préférences.

---

## 🧪 Trois implémentations

Le dépôt contient trois versions successives du simulateur. La logique métier (les 5 méthodes AMD, la base des 50 écoles, les seuils ELECTRE, les interactions de Choquet) est strictement identique d'une version à l'autre — seule la couche d'interface évolue.

| Version | Stack | UI | Statut |
| --- | --- | --- | --- |
| [`amd_ecoles_v2.py`](amd_ecoles_v2.py) | Python 3 + Tkinter | Style RATP / Métro Parisien (sobre, institutionnel) | Itération 1 |
| [`amd_ecoles_v3.py`](amd_ecoles_v3.py) | Python 3 + Tkinter (Canvas custom) | Refonte palette « Aurora » (indigo / violet) | Itération 2 |
| [`amd-studio/`](amd-studio/) | Vite + **React 18 + TypeScript** + Tailwind + Framer Motion + Recharts | Application web moderne, animations, radar chart | **Version finale ✨** |

---

## 🚀 Démarrage rapide

### ⚛️ Version web (recommandée)

```bash
cd amd-studio
npm install        # 1 seule fois — installe ~180 packages
npm run dev        # ouvre http://localhost:5173 automatiquement
```

Pour générer une version de production statique (`dist/`) :

```bash
npm run build
npm run preview
```

### 🐍 Versions Python (tkinter)

Aucune dépendance externe (uniquement la bibliothèque standard).

```bash
python amd_ecoles_v3.py    # version « Aurora » (recommandée)
python amd_ecoles_v2.py    # version « RATP »
```

> ⚠️ Tkinter est livré avec Python sous Windows et macOS. Sous Linux, installer `python3-tk` au préalable.

---

## 🧮 Les 5 méthodes AMD implémentées

| # | Méthode | Type | Particularité |
| - | --- | --- | --- |
| 1 | **Somme Pondérée** | Compensation totale | `S(a) = Σ wⱼ × uⱼ(a)` — agrégation linéaire de référence |
| 2 | **Opérateur OWA** (Yager) | Pondération par rang | `W = (0.05, 0.15, 0.20, 0.20, 0.20, 0.20)` — favorise les profils équilibrés |
| 3 | **Intégrale de Choquet** | 2-additif (Grabisch) | Indices d'interaction : `I(g1,g2) = −0.05` (redondance), `I(g4,g6) = +0.05` (synergie) |
| 4 | **Méthode du Min** | Maximin de Wald | Pessimisme pur — la pire utilité commande le score |
| 5 | **ELECTRE Is** | Surclassement non compensatoire | Concordance + discordance + vetos · seuil `λ = 0.65` |

Toutes les méthodes s'appuient sur une normalisation **min-max** des performances brutes sur l'échelle `[0 ; 100]`, avec inversion pour le critère à minimiser (g3 Coût).

---

## 📊 Les 6 critères de décision

| Code | Critère | Sens | Échelle | Couleur |
| --- | --- | --- | --- | --- |
| `g1` | Salaire moyen à la sortie | ▲ Maximiser | 35 000 – 60 000 €/an | 💜 violet |
| `g2` | Taux d'emploi à 6 mois | ▲ Maximiser | 85 – 100 % | 💙 bleu |
| `g3` | Coût total de scolarité (3 ans) | ▼ **Minimiser** | 0 – 15 000 € | ❤️ rouge |
| `g4` | Diversité sociale (boursiers) | ▲ Maximiser | 5 – 40 % | 💚 émeraude |
| `g5` | Engagement DD&RS | ▲ Maximiser | 1 – 5 (note) | 🩵 teal |
| `g6` | Vie associative | ▲ Maximiser | 1 – 10 (note) | 🧡 ambre |

### Seuils ELECTRE Is

| Critère | q (indifférence) | p (préférence) | v (veto) |
| --- | --- | --- | --- |
| g1 Salaire | 1 500 € | 3 000 € | 10 000 € |
| g2 Emploi | 1 % | 3 % | 8 % |
| g3 Coût | 500 € | 1 500 € | 5 000 € |
| g4 Diversité | 2 % | 5 % | — |
| g5 DD&RS | 0.3 | 0.8 | — |
| g6 Vie asso. | 0.5 | 1.5 | 4.0 |

---

## 🏫 Les 50 écoles intégrées

La base de données (`amd-studio/src/lib/data.ts` côté web, et `ECOLES` côté Python) couvre **10 grands groupes** représentatifs du paysage français :

- **Centrale** (CentraleSupélec, Lyon, Lille, Nantes, Marseille)
- **Mines / IMT** (Paris-PSL, Saint-Étienne, Nancy, Atlantique, Albi)
- **INSA** (Lyon, Toulouse, Rennes, Rouen, Strasbourg)
- **Polytech** (Nice, Montpellier, Grenoble, Nantes, Lille)
- **Universités de Technologie** (UTC, UTT, UTBM)
- **Grandes écoles d'excellence** (ISAE-SUPAERO, ENSTA, ENSAE, Télécom Paris/SudParis)
- **Arts et Métiers** (ENSAM + Lille)
- **Spécialisées Info/Num** (ENSIMAG, ENSEEIHT, ENSEIRB-MATMECA, EPITA, EFREI)
- **Post-bac privées** (ECE, ESIEE, ESME, ESILV, EPF)
- **Niches** (Chimie ParisTech, ESPCI, AgroParisTech, ENSAT, ESTP, ENTPE, ENSC, ESTIA, EIGSI)

Données simulées mais cohérentes avec les classements publics (USINE Nouvelle, L'Étudiant, Le Figaro, palmarès DD&RS).

---

## ✨ Profils-types intégrés (version web)

Cinq profils-types préconfigurés pour explorer rapidement différents arbitrages :

| Profil | Pondération dominante |
| --- | --- |
| ⚖️ Équilibré | Tous les critères à `1/6` |
| 💰 Carriériste | Salaire (`0.40`) + Emploi (`0.30`) |
| 🎓 Étudiant | Vie associative (`0.35`) + Diversité (`0.25`) |
| 🌍 Engagé | DD&RS (`0.35`) + Coût (`0.20`) |
| 💸 Petit budget | Coût (`0.45`) prioritaire |

---

## 📁 Structure du dépôt

```
.
├── amd_ecoles_v2.py              ← Python · UI RATP
├── amd_ecoles_v3.py              ← Python · UI Aurora (refonte)
│
├── amd-studio/                   ← Application web (version finale)
│   ├── src/
│   │   ├── lib/
│   │   │   ├── data.ts           ← 50 écoles + 6 critères + profils-types
│   │   │   └── methods.ts        ← Moteur AMD (5 méthodes)
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── WeightControl.tsx     ← Slider custom (pointer events)
│   │   │   ├── MethodSelector.tsx
│   │   │   ├── PresetChips.tsx
│   │   │   ├── HeroCard.tsx          ← Carte champion #1
│   │   │   ├── RadarProfile.tsx      ← Radar chart Recharts
│   │   │   ├── PerformanceGrid.tsx   ← Tableau perfs détaillé
│   │   │   └── Top5Board.tsx
│   │   ├── App.tsx               ← Layout + état + recalcul réactif
│   │   ├── main.tsx
│   │   └── index.css             ← Tailwind + tokens design
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md                 ← Doc spécifique à l'app web
│
├── rapport_AMD_v1.docx           ← Rapport d'équipe (version finale)
├── Rapport_AMD_v0.docx           ← Rapport (version intermédiaire)
├── Rapport_AMD_test.pdf          ← Export test
├── projet2026.pdf                ← Énoncé du projet
├── projet_decision_sources.pdf   ← Sources et bibliographie
│
└── README.md                     ← (ce fichier)
```

---

## 🧠 Concepts théoriques mobilisés

Cours de référence : **Décision Multicritère** (M1 MIAGE Dauphine — supports `c1_AD.pdf`, `c2_AMD.pdf`, `c2_AMD_2/3/4.pdf`).

- Modèles d'agrégation **compensatoires** vs **non compensatoires**
- **Utilités normalisées** (min-max)
- **Opérateurs symétriques** (OWA, attitude au risque via le vecteur W)
- **Capacités 2-additives** de Grabisch (Shapley + indices d'interaction)
- **Surclassement** ELECTRE Is (concordance, discordance, crédibilité, vetos)
- Sensibilité d'un classement aux pondérations et aux seuils

---

## 🎨 Stack & choix techniques (version web)

| Outil | Rôle | Version |
| --- | --- | --- |
| **Vite** | Bundler / dev server | 6.x |
| **React** | UI déclarative | 18.x |
| **TypeScript** | Typage strict du moteur AMD | 5.x |
| **Tailwind CSS** | Design system utility-first | 3.x |
| **Framer Motion** | Animations (spring physics, layoutId, transitions) | 11.x |
| **Recharts** | Radar chart 6 critères | 2.x |
| **Lucide React** | Icônes vectorielles cohérentes | 0.4.x |

**Choix de design** :

- Recalcul **instantané** à chaque mouvement de slider (pas de bouton "calculer" obligatoire)
- Sliders avec **pointer events** + animation spring (Framer Motion) au lieu des `<input type="range">` natifs
- **Layout id** Framer pour la transition fluide de la sélection de méthode
- Palette « Aurora » : violet `#7c3aed` + rose `#ec4899`, contraste accessible (WCAG AA)
- Une couleur dédiée par critère, cohérente entre sliders, barres, badges

---

## 👤 Auteur

**Hugo Soulier-Pires** — M1 MIAGE 2025-2026
Université Paris-Dauphine · PSL Research University

---

## 📜 Licence

Projet académique. Code libre de réutilisation à des fins éducatives.
