# 🎓 AMD Studio v3.0

**Simulateur d'Aide Multicritère à la Décision** — choisis ton école d'ingénieurs avec la science de la décision.

> Refonte complète en stack web moderne (Vite + React + TypeScript + Tailwind + Framer Motion + Recharts).
> Le moteur AMD implémente les 5 méthodes du rapport sur une base de 50 écoles d'ingénieurs françaises.

---

## 🚀 Démarrage rapide

```bash
# 1. Installer les dépendances (1 seule fois)
npm install

# 2. Lancer le serveur de développement
npm run dev
```

L'application s'ouvre automatiquement à l'adresse <http://localhost:5173>.

Pour générer une version de production :

```bash
npm run build
npm run preview      # pour servir le dossier dist/
```

---

## 🧮 Méthodes AMD implémentées

| Méthode             | Type                          | Particularité                                          |
| ------------------- | ----------------------------- | ------------------------------------------------------ |
| Somme Pondérée      | Compensation totale            | Référence — agrégation linéaire des utilités          |
| Opérateur OWA       | Pondération par rang           | `W = (0.05, 0.15, 0.20, 0.20, 0.20, 0.20)` (Yager)    |
| Intégrale de Choquet | Modèle 2-additif (Grabisch)   | I(g1,g2) = −0.05 · I(g4,g6) = +0.05                    |
| Méthode du Min      | Maximin pessimiste (Wald)      | Aucune compensation                                    |
| ELECTRE Is          | Surclassement non compensatoire | Concordance + discordance + vetos · λ = 0.65         |

## 📊 Les 6 critères

| Code | Critère              | Sens         | Échelle              |
| ---- | -------------------- | ------------ | -------------------- |
| g1   | Salaire à la sortie  | ▲ MAX        | 35 000 – 60 000 €/an |
| g2   | Emploi à 6 mois      | ▲ MAX        | 85 – 100 %           |
| g3   | Coût total (3 ans)   | ▼ MIN        | 0 – 15 000 €         |
| g4   | Diversité sociale    | ▲ MAX        | 5 – 40 %             |
| g5   | Engagement DD&RS     | ▲ MAX        | 1 – 5 (note)         |
| g6   | Vie associative      | ▲ MAX        | 1 – 10 (note)        |

---

## 🎨 Stack technique

- **Vite 6** — bundler/dev server ultra rapide
- **React 18 + TypeScript** — typage strict, état réactif
- **Tailwind CSS 3** — design system utility-first
- **Framer Motion** — animations fluides
- **Recharts** — radar chart pour visualiser le profil de l'école n°1
- **Lucide React** — icônes vectorielles cohérentes

---

## 📁 Structure

```
amd-studio/
├── src/
│   ├── lib/
│   │   ├── data.ts       # 50 écoles + config des 6 critères + profils-types
│   │   └── methods.ts    # Moteur AMD (5 méthodes) + normalisation
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── WeightControl.tsx    # Slider personnalisé
│   │   ├── MethodSelector.tsx
│   │   ├── PresetChips.tsx
│   │   ├── HeroCard.tsx         # Carte champion #1
│   │   ├── RadarProfile.tsx     # Radar chart 6 critères
│   │   ├── PerformanceGrid.tsx  # Tableau brutes + normalisées
│   │   └── Top5Board.tsx        # Top 5 alternatives
│   ├── App.tsx                  # Layout + état global
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
└── tailwind.config.js
```

---

## ✨ Ce qui change par rapport à la version Python (tkinter)

| Aspect           | Python / tkinter v3                  | Web v3 (cette version)                              |
| ---------------- | ------------------------------------ | --------------------------------------------------- |
| Recalcul         | Au clic du bouton                    | Instantané à chaque mouvement de slider             |
| Visualisations   | Barres rectangulaires                | + Radar chart Recharts animé                        |
| Animations       | Aucune                               | Framer Motion (entrée, hover, transitions)         |
| Sliders          | Canvas custom statique               | Slider pointer-event avec spring physics            |
| Typo             | Segoe UI (système Windows)           | Inter + JetBrains Mono (via Google Fonts)           |
| Couleurs         | Palette violette fixe                | + dégradés, glassmorphism, badges qualité          |
| Responsive       | Non                                  | Adapte le layout au format de la fenêtre            |
| Accessibilité    | Limitée                              | Boutons focus visibles, lecteurs d'écran            |

---

M1 MIAGE · Décision Multicritère · Université Paris-Dauphine
