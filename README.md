# Aide à la décision multicritère — choix d'une école d'ingénieurs

Projet du cours de Décision Multicritère, M1 MIAGE, Université Paris-Dauphine (PSL),
2025-2026.

L'application permet de classer cinquante écoles d'ingénieurs françaises selon
cinq méthodes d'agrégation multicritère et un profil de préférences saisi par
l'utilisateur.

## Versions

Le dépôt contient trois implémentations successives. Le moteur de calcul
(données, méthodes, seuils ELECTRE, interactions de Choquet) est identique
d'une version à l'autre ; seule l'interface évolue.

| Fichier              | Pile technique                                    | Statut              |
| -------------------- | ------------------------------------------------- | ------------------- |
| `amd_ecoles_v2.py`   | Python 3, Tkinter                                 | Première itération  |
| `amd_ecoles_v3.py`   | Python 3, Tkinter (Canvas personnalisé)           | Refonte de l'UI     |
| `amd-studio/`        | Vite, React 18, TypeScript, Tailwind CSS          | Version finale      |

## Exécution

### Version web

```bash
cd amd-studio
npm install
npm run dev
```

L'application est servie sur `http://localhost:5173`. Pour produire un
build statique dans `dist/` :

```bash
npm run build
```

### Versions Python

Aucune dépendance hors de la bibliothèque standard.

```bash
python amd_ecoles_v3.py
```

Sous Linux, le paquet `python3-tk` doit être installé au préalable.

## Méthodes implémentées

| Méthode              | Type                                                                |
| -------------------- | ------------------------------------------------------------------- |
| Somme pondérée       | Agrégation compensatoire linéaire                                   |
| Opérateur OWA        | Pondération par rang, W = (0.05, 0.15, 0.20, 0.20, 0.20, 0.20)      |
| Intégrale de Choquet | Modèle 2-additif de Grabisch                                        |
| Méthode du min       | Maximin de Wald, sans compensation                                  |
| ELECTRE Is           | Surclassement avec seuil de concordance λ = 0.65                    |

Les utilités sont obtenues par normalisation min-max des performances brutes
sur l'intervalle [0 ; 100], inversée pour le critère à minimiser.

Paramètres du modèle de Choquet 2-additif :

- I(g1, g2) = −0.05  — redondance entre salaire et taux d'emploi
- I(g4, g6) = +0.05  — synergie entre diversité sociale et vie associative

## Critères

| Code | Critère                          | Sens       | Échelle              |
| ---- | -------------------------------- | ---------- | -------------------- |
| g1   | Salaire moyen à la sortie        | maximiser  | 35 000 – 60 000 €/an |
| g2   | Taux d'emploi à six mois         | maximiser  | 85 – 100 %           |
| g3   | Coût total de scolarité (3 ans)  | minimiser  | 0 – 15 000 €         |
| g4   | Diversité sociale (boursiers)    | maximiser  | 5 – 40 %             |
| g5   | Engagement DD&RS                 | maximiser  | 1 – 5                |
| g6   | Vie associative                  | maximiser  | 1 – 10               |

Seuils ELECTRE Is :

| Critère | q (indifférence) | p (préférence) | v (veto) |
| ------- | ---------------- | -------------- | -------- |
| g1      | 1 500 €          | 3 000 €        | 10 000 € |
| g2      | 1 %              | 3 %            | 8 %      |
| g3      | 500 €            | 1 500 €        | 5 000 € |
| g4      | 2 %              | 5 %            | —        |
| g5      | 0,3              | 0,8            | —        |
| g6      | 0,5              | 1,5            | 4,0      |

## Base de données

La base couvre cinquante écoles d'ingénieurs françaises, réparties entre les
principaux groupes : Centrale, Mines / IMT, INSA, Polytech, universités de
technologie, grandes écoles spécialisées (ISAE-SUPAERO, ENSTA, ENSAE,
Télécom), Arts et Métiers, écoles d'informatique, post-bac privées, chimie,
agronomie et génie civil. Les performances brutes sont simulées mais
calibrées sur les classements publics (L'Usine Nouvelle, L'Étudiant,
palmarès DD&RS).

## Structure du dépôt

```
.
├── amd_ecoles_v2.py
├── amd_ecoles_v3.py
├── amd-studio/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── data.ts          (50 écoles, 6 critères, profils-types)
│   │   │   └── methods.ts       (moteur AMD)
│   │   ├── components/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── rapport_AMD_v1.docx
├── projet2026.pdf
├── projet_decision_sources.pdf
└── README.md
```

## Auteur

Hugo Soulier-Pires — M1 MIAGE, Université Paris-Dauphine (PSL), 2025-2026.
