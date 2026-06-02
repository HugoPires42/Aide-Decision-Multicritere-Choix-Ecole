// =============================================================================
//  methods.ts — Moteur AMD : 5 méthodes d'agrégation multicritère
// =============================================================================
//   1. Somme Pondérée            (compensation totale)
//   2. Opérateur OWA (Yager)     (favorise les profils équilibrés)
//   3. Intégrale de Choquet      (modèle 2-additif de Grabisch)
//   4. Méthode du Min (Wald)     (pessimisme pur)
//   5. ELECTRE Is                (surclassement non compensatoire)
// =============================================================================

import { CRITERES, ECOLES, type Ecole } from './data'

/** Identifiants des 5 méthodes disponibles. */
export type MethodeId =
  | 'somme'
  | 'owa'
  | 'choquet'
  | 'min'
  | 'electre'

/** Métadonnées d'affichage de chaque méthode. */
export const METHODES: {
  id: MethodeId
  label: string
  short: string
  icone: string
  description: string
  scoreLibelle: string
}[] = [
  {
    id: 'somme',
    label: 'Somme Pondérée',
    short: 'WSum',
    icone: '∑',
    description: 'Agrégation classique à compensation totale. Une bonne note peut compenser une faiblesse.',
    scoreLibelle: 'sur 100',
  },
  {
    id: 'owa',
    label: 'Opérateur OWA',
    short: 'OWA',
    icone: '↺',
    description: 'Pondération par rang (W = 0.05 / 0.15 / 0.20×4). Favorise les profils équilibrés.',
    scoreLibelle: 'sur 100',
  },
  {
    id: 'choquet',
    label: 'Intégrale de Choquet',
    short: 'Choq.',
    icone: '∮',
    description: 'Modèle 2-additif de Grabisch. Gère redondance (g1↔g2) et synergie (g4↔g6).',
    scoreLibelle: 'sur 100',
  },
  {
    id: 'min',
    label: 'Méthode du Min',
    short: 'Min',
    icone: '↓',
    description: 'Maximin de Wald : logique pessimiste pure. Aucune compensation possible.',
    scoreLibelle: 'sur 100',
  },
  {
    id: 'electre',
    label: 'ELECTRE Is',
    short: 'ELECTRE',
    icone: '⇄',
    description: 'Surclassement avec concordance, discordance et vetos. Seuil λ = 0.65.',
    scoreLibelle: 'score net',
  },
]

// ── Paramètres globaux ───────────────────────────────────────────────────────

/** Vecteur de pondération OWA par rang (du meilleur au pire critère). */
const W_OWA = [0.05, 0.15, 0.20, 0.20, 0.20, 0.20]

/** Indices d'interaction du modèle de Choquet 2-additif (Grabisch). */
const INTERACTIONS: Array<[number, number, number]> = [
  [0, 1, -0.05],  // I(g1, g2) — redondance salaire/emploi
  [3, 5, +0.05],  // I(g4, g6) — synergie diversité/vie associative
]

/** Seuil de concordance globale λ pour ELECTRE Is. */
const LAMBDA_ELECTRE = 0.65

// =============================================================================
//  Types des résultats
// =============================================================================

/** Une école classée avec son score (échelle dépendante de la méthode). */
export type Classement = {
  ecole: Ecole
  score: number
  /** Score ramené en [0; 100] pour affichage homogène des barres. */
  scoreNormalise: number
  /** Utilités normalisées des 6 critères (toujours en [0; 100]). */
  utilites: [number, number, number, number, number, number]
  rang: number
}

// =============================================================================
//  Normalisation min-max [0 ; 100]
// =============================================================================

/**
 * Normalise chaque performance brute selon le min-max sur les 50 écoles.
 *   - Maximiser : u_j = (g_j - min) / (max - min) × 100
 *   - Minimiser : u_j = (max - g_j) / (max - min) × 100
 */
function normaliser(ecoles: Ecole[]): Map<string, [number, number, number, number, number, number]> {
  const mins = [0, 0, 0, 0, 0, 0].map((_, j) =>
    Math.min(...ecoles.map(e => e.perfs[j]))
  )
  const maxs = [0, 0, 0, 0, 0, 0].map((_, j) =>
    Math.max(...ecoles.map(e => e.perfs[j]))
  )

  const out = new Map<string, [number, number, number, number, number, number]>()
  for (const e of ecoles) {
    const u = [0, 0, 0, 0, 0, 0] as [number, number, number, number, number, number]
    for (let j = 0; j < 6; j++) {
      const amp = maxs[j] - mins[j]
      if (amp === 0) {
        u[j] = 50
      } else if (CRITERES[j].max) {
        u[j] = ((e.perfs[j] - mins[j]) / amp) * 100
      } else {
        u[j] = ((maxs[j] - e.perfs[j]) / amp) * 100
      }
    }
    out.set(e.nom, u)
  }
  return out
}

/** Normalise les poids saisis pour qu'ils somment à 1. */
function normerPoids(poids: number[]): number[] {
  const s = poids.reduce((a, b) => a + b, 0)
  if (s === 0) return [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
  return poids.map(w => w / s)
}

// =============================================================================
//  1. Somme Pondérée — S(a) = Σ w_j × u_j(a)
// =============================================================================
function sommePonderee(
  utilites: Map<string, number[]>,
  poids: number[]
): Map<string, number> {
  const w = normerPoids(poids)
  const out = new Map<string, number>()
  for (const [nom, u] of utilites) {
    let s = 0
    for (let j = 0; j < 6; j++) s += w[j] * u[j]
    out.set(nom, s)
  }
  return out
}

// =============================================================================
//  2. Opérateur OWA — pondération des utilités triées par ordre décroissant
// =============================================================================
function owa(
  utilites: Map<string, number[]>,
  poids: number[]
): Map<string, number> {
  const w = normerPoids(poids)
  const out = new Map<string, number>()
  for (const [nom, u] of utilites) {
    // On pondère d'abord par les poids utilisateur (×6 pour rester sur [0,100])
    const uPond = u.map((uj, j) => w[j] * uj * 6)
    // Tri décroissant puis combinaison via W_OWA
    const uTri = [...uPond].sort((a, b) => b - a)
    let s = 0
    for (let k = 0; k < 6; k++) s += W_OWA[k] * uTri[k]
    out.set(nom, s)
  }
  return out
}

// =============================================================================
//  3. Intégrale de Choquet — modèle 2-additif de Grabisch
//     C(a) = Σ φ_i × u_i  +  Σ I_ij × min(u_i,u_j)  −  Σ |I_ij| × max(u_i,u_j)
// =============================================================================
function choquet(
  utilites: Map<string, number[]>,
  poids: number[]
): Map<string, number> {
  const shapley = normerPoids(poids)
  const out = new Map<string, number>()
  for (const [nom, u] of utilites) {
    let s = 0
    for (let j = 0; j < 6; j++) s += shapley[j] * u[j]
    for (const [i, j, Iij] of INTERACTIONS) {
      if (Iij > 0) s += Iij * Math.min(u[i], u[j])   // synergie
      else         s += Iij * Math.max(u[i], u[j])   // redondance (Iij < 0)
    }
    out.set(nom, s)
  }
  return out
}

// =============================================================================
//  4. Méthode du Min — S(a) = min_j { w_j × u_j(a) × 6 }
// =============================================================================
function minWald(
  utilites: Map<string, number[]>,
  poids: number[]
): Map<string, number> {
  const w = normerPoids(poids)
  const out = new Map<string, number>()
  for (const [nom, u] of utilites) {
    let mn = Infinity
    for (let j = 0; j < 6; j++) {
      const v = w[j] * u[j] * 6
      if (v < mn) mn = v
    }
    out.set(nom, mn)
  }
  return out
}

// =============================================================================
//  5. ELECTRE Is — surclassement avec concordance, discordance et vetos
// =============================================================================
function electreIs(
  ecoles: Ecole[],
  poids: number[]
): Map<string, number> {
  const w = normerPoids(poids)
  const n = ecoles.length

  /** Concordance partielle c_j(a, b) pour le critère j. */
  function cPart(ga: number, gb: number, j: number): number {
    const c = CRITERES[j]
    const { q, p } = c.seuils
    const diff = c.max ? (ga - gb) : (gb - ga)
    if (diff >= -q) return 1
    if (diff <= -p) return 0
    return (diff + p) / (p - q)
  }

  /** Discordance partielle d_j(a, b) pour le critère j (si veto défini). */
  function dPart(ga: number, gb: number, j: number): number {
    const c = CRITERES[j]
    if (c.seuils.v === undefined) return 0
    const { p, v } = c.seuils
    const diff = c.max ? (gb - ga) : (ga - gb)
    if (diff <= p) return 0
    if (diff >= v!) return 1
    return (diff - p) / (v! - p)
  }

  // Construction de la matrice de surclassement
  const surclasse: boolean[][] = Array.from({ length: n }, () =>
    new Array(n).fill(false)
  )

  for (let i = 0; i < n; i++) {
    for (let k = 0; k < n; k++) {
      if (i === k) continue
      const a = ecoles[i].perfs
      const b = ecoles[k].perfs

      // Concordance globale C(a, b)
      let C = 0
      for (let j = 0; j < 6; j++) C += w[j] * cPart(a[j], b[j], j)

      // Crédibilité σ(a, b) ajustée par les discordances
      let sigma = C
      for (let j = 0; j < 6; j++) {
        const d = dPart(a[j], b[j], j)
        if (d > C) {
          sigma = C < 1 ? sigma * (1 - d) / (1 - C) : 0
        }
      }

      if (sigma >= LAMBDA_ELECTRE) surclasse[i][k] = true
    }
  }

  // Score net : (surclassements émis) − (surclassements subis)
  const out = new Map<string, number>()
  for (let i = 0; i < n; i++) {
    let plus = 0
    let moins = 0
    for (let k = 0; k < n; k++) {
      if (surclasse[i][k]) plus++
      if (surclasse[k][i]) moins++
    }
    out.set(ecoles[i].nom, plus - moins)
  }
  return out
}

// =============================================================================
//  API PUBLIQUE
// =============================================================================

/**
 * Calcule le classement complet des 50 écoles selon la méthode et les poids.
 * Retourne un tableau trié (meilleure école en première position).
 */
export function classer(
  methode: MethodeId,
  poids: number[]
): Classement[] {
  const utilites = normaliser(ECOLES)

  let scores: Map<string, number>
  switch (methode) {
    case 'somme':   scores = sommePonderee(utilites, poids); break
    case 'owa':     scores = owa(utilites, poids); break
    case 'choquet': scores = choquet(utilites, poids); break
    case 'min':     scores = minWald(utilites, poids); break
    case 'electre': scores = electreIs(ECOLES, poids); break
  }

  // Normalisation des scores en [0 ; 100] pour les barres de progression
  const vals = [...scores.values()]
  const mn = Math.min(...vals)
  const mx = Math.max(...vals)
  const amp = mx - mn

  const result: Classement[] = ECOLES.map(e => {
    const sc = scores.get(e.nom)!
    const normalise = amp === 0 ? 50 : ((sc - mn) / amp) * 100
    return {
      ecole: e,
      score: sc,
      scoreNormalise: normalise,
      utilites: utilites.get(e.nom)!,
      rang: 0,
    }
  })

  // Tri décroissant par score brut + attribution des rangs (1-based)
  result.sort((a, b) => b.score - a.score)
  result.forEach((r, i) => (r.rang = i + 1))
  return result
}
