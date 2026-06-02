// =============================================================================
//  data.ts — Base de données : 50 écoles d'ingénieurs + configuration critères
// =============================================================================

/** Une école = un nom + 6 performances brutes (g1 → g6). */
export type Ecole = {
  nom: string
  groupe: string
  perfs: [number, number, number, number, number, number]
}

/**
 * Définition d'un critère AMD.
 *  - `max`  : true = à maximiser, false = à minimiser (g3 Coût)
 *  - `seuils` : seuils ELECTRE Is (q indifférence, p préférence, v veto)
 */
export type Critere = {
  id: 'g1' | 'g2' | 'g3' | 'g4' | 'g5' | 'g6'
  label: string
  unite: string
  bornes: string
  max: boolean
  couleur: string
  couleurClasse: string  // classe Tailwind associée
  icone: string
  seuils: { q: number; p: number; v?: number }
}

// ── Définition des 6 critères ────────────────────────────────────────────────

export const CRITERES: Critere[] = [
  {
    id: 'g1',
    label: 'Salaire à la sortie',
    unite: '€/an',
    bornes: '35 000 – 60 000',
    max: true,
    couleur: '#8b5cf6',
    couleurClasse: 'crit-salaire',
    icone: '💰',
    seuils: { q: 1500, p: 3000, v: 10000 },
  },
  {
    id: 'g2',
    label: 'Emploi à 6 mois',
    unite: '%',
    bornes: '85 – 100',
    max: true,
    couleur: '#3b82f6',
    couleurClasse: 'crit-emploi',
    icone: '💼',
    seuils: { q: 1, p: 3, v: 8 },
  },
  {
    id: 'g3',
    label: 'Coût total (3 ans)',
    unite: '€',
    bornes: '0 – 15 000',
    max: false,
    couleur: '#f43f5e',
    couleurClasse: 'crit-cout',
    icone: '🏛️',
    seuils: { q: 500, p: 1500, v: 5000 },
  },
  {
    id: 'g4',
    label: 'Diversité sociale',
    unite: '%',
    bornes: '5 – 40',
    max: true,
    couleur: '#10b981',
    couleurClasse: 'crit-divers',
    icone: '🤝',
    seuils: { q: 2, p: 5 },
  },
  {
    id: 'g5',
    label: 'Engagement DD&RS',
    unite: '/5',
    bornes: '1 – 5',
    max: true,
    couleur: '#14b8a6',
    couleurClasse: 'crit-ddrs',
    icone: '🌱',
    seuils: { q: 0.3, p: 0.8 },
  },
  {
    id: 'g6',
    label: 'Vie associative',
    unite: '/10',
    bornes: '1 – 10',
    max: true,
    couleur: '#f59e0b',
    couleurClasse: 'crit-vie',
    icone: '🎉',
    seuils: { q: 0.5, p: 1.5, v: 4 },
  },
]

// ── Base de 50 écoles d'ingénieurs françaises ────────────────────────────────
//   Données réalistes mais simulées (sources : palmarès USINE / L'Étudiant /
//   Le Figaro / classements DD&RS). Format : [salaire, emploi%, coût€, div%, ddrs/5, vie/10]

export const ECOLES: Ecole[] = [
  // Groupe Centrale
  { nom: 'CentraleSupélec',            groupe: 'Centrale',   perfs: [58000, 97, 4500, 12, 4.0, 8.5] },
  { nom: 'Centrale Lyon',              groupe: 'Centrale',   perfs: [52000, 95, 3800, 14, 4.2, 8.0] },
  { nom: 'Centrale Lille',             groupe: 'Centrale',   perfs: [48000, 93, 3500, 16, 3.8, 7.5] },
  { nom: 'Centrale Nantes',            groupe: 'Centrale',   perfs: [49000, 94, 3200, 18, 4.5, 8.0] },
  { nom: 'Centrale Marseille',         groupe: 'Centrale',   perfs: [46000, 91, 3000, 17, 3.5, 7.0] },

  // Mines / IMT
  { nom: 'Mines Paris (PSL)',          groupe: 'Mines',      perfs: [60000, 98, 5000, 10, 3.5, 7.0] },
  { nom: 'Mines Saint-Étienne',        groupe: 'Mines',      perfs: [47000, 92, 2800, 20, 4.0, 7.5] },
  { nom: 'Mines Nancy',                groupe: 'Mines',      perfs: [46000, 91, 2500, 19, 3.8, 7.0] },
  { nom: 'IMT Atlantique',             groupe: 'Mines',      perfs: [48000, 93, 2600, 22, 4.5, 7.5] },
  { nom: 'IMT Mines Albi',             groupe: 'Mines',      perfs: [43000, 89, 2200, 24, 4.2, 6.5] },

  // Groupe INSA
  { nom: 'INSA Lyon',                  groupe: 'INSA',       perfs: [45000, 94, 1200, 30, 4.5, 9.0] },
  { nom: 'INSA Toulouse',              groupe: 'INSA',       perfs: [44000, 92, 1100, 28, 4.3, 8.5] },
  { nom: 'INSA Rennes',                groupe: 'INSA',       perfs: [43000, 91, 1000, 27, 4.0, 8.0] },
  { nom: 'INSA Rouen',                 groupe: 'INSA',       perfs: [42000, 90, 1000, 26, 3.8, 7.5] },
  { nom: 'INSA Strasbourg',            groupe: 'INSA',       perfs: [43000, 91, 1100, 25, 4.0, 7.5] },

  // Polytech
  { nom: 'Polytech Nice Sophia',       groupe: 'Polytech',   perfs: [38000, 88,  800, 25, 3.0, 7.5] },
  { nom: 'Polytech Montpellier',       groupe: 'Polytech',   perfs: [37000, 87,  700, 28, 3.2, 7.0] },
  { nom: 'Polytech Grenoble',          groupe: 'Polytech',   perfs: [39000, 89,  900, 24, 3.5, 7.5] },
  { nom: 'Polytech Nantes',            groupe: 'Polytech',   perfs: [38000, 88,  750, 26, 3.3, 7.0] },
  { nom: 'Polytech Lille',             groupe: 'Polytech',   perfs: [37000, 87,  700, 27, 3.0, 6.5] },

  // Universités de Technologie
  { nom: 'UTC Compiègne',              groupe: 'UT',         perfs: [47000, 93, 1800, 22, 4.0, 8.5] },
  { nom: 'UTT Troyes',                 groupe: 'UT',         perfs: [42000, 91, 1500, 22, 4.0, 8.0] },
  { nom: 'UTBM Belfort-Montbéliard',   groupe: 'UT',         perfs: [40000, 89, 1300, 23, 3.5, 7.5] },

  // Grandes écoles spécialisées
  { nom: 'ISAE-SUPAERO',               groupe: 'Excellence', perfs: [55000, 96, 4000, 11, 4.5, 8.0] },
  { nom: 'ENSTA Paris',                groupe: 'Excellence', perfs: [53000, 95, 3500, 14, 4.0, 7.0] },
  { nom: 'ENSAE Paris',                groupe: 'Excellence', perfs: [57000, 96, 4200,  9, 3.0, 6.0] },
  { nom: 'Télécom Paris',              groupe: 'Excellence', perfs: [56000, 97, 4800, 13, 4.0, 7.5] },
  { nom: 'Télécom SudParis',           groupe: 'Excellence', perfs: [48000, 92, 3600, 16, 3.8, 7.0] },

  // Arts et Métiers
  { nom: 'Arts et Métiers (ENSAM)',    groupe: 'ENSAM',      perfs: [46000, 93, 2500, 20, 3.5, 8.5] },
  { nom: 'Arts et Métiers Lille',      groupe: 'ENSAM',      perfs: [44000, 91, 2300, 21, 3.3, 8.0] },

  // Spécialisées Informatique
  { nom: 'ENSIMAG (Grenoble INP)',     groupe: 'Info',       perfs: [52000, 95, 3000, 15, 3.5, 6.5] },
  { nom: 'ENSEEIHT (Toulouse INP)',    groupe: 'Info',       perfs: [49000, 93, 2800, 17, 3.8, 7.0] },
  { nom: 'ENSEIRB-MATMECA',            groupe: 'Info',       perfs: [48000, 92, 2700, 16, 3.5, 7.0] },
  { nom: 'EPITA',                      groupe: 'Info',       perfs: [45000, 92, 10500, 15, 2.5, 8.5] },
  { nom: 'EFREI',                      groupe: 'Info',       perfs: [39000, 87, 9500, 18, 2.0, 9.0] },

  // Post-bac privées
  { nom: 'ECE Paris',                  groupe: 'Privée',     perfs: [40000, 89, 10000, 20, 2.5, 8.5] },
  { nom: 'ESIEE Paris',                groupe: 'Privée',     perfs: [41000, 90, 8500, 19, 2.8, 7.5] },
  { nom: 'ESME Sudria',                groupe: 'Privée',     perfs: [38000, 86, 9000, 17, 2.2, 7.0] },
  { nom: 'ESILV (Léonard de Vinci)',   groupe: 'Privée',     perfs: [42000, 90, 11000, 16, 2.5, 8.0] },
  { nom: 'EPF',                        groupe: 'Privée',     perfs: [40000, 88, 9500, 22, 3.0, 7.5] },

  // Chimie / Matériaux
  { nom: 'Chimie ParisTech (PSL)',     groupe: 'Chimie',     perfs: [50000, 93, 3000, 13, 4.5, 6.0] },
  { nom: 'ESPCI Paris (PSL)',          groupe: 'Chimie',     perfs: [54000, 96, 1500,  8, 4.8, 5.5] },
  { nom: 'ENSCM Montpellier',          groupe: 'Chimie',     perfs: [41000, 89, 1800, 22, 4.0, 6.5] },

  // Agro / Bio
  { nom: 'AgroParisTech',              groupe: 'Agro',       perfs: [44000, 91, 2000, 18, 5.0, 7.5] },
  { nom: 'ENSAT Toulouse',             groupe: 'Agro',       perfs: [39000, 87, 1200, 25, 4.5, 7.0] },

  // Génie civil / BTP
  { nom: 'ESTP Paris',                 groupe: 'BTP',        perfs: [45000, 93, 8000, 15, 3.0, 8.0] },
  { nom: 'ENTPE Lyon',                 groupe: 'BTP',        perfs: [43000, 90, 1500, 20, 3.8, 6.5] },

  // Autres
  { nom: 'ENSC Cognitique Bordeaux',   groupe: 'Autre',      perfs: [41000, 88, 1800, 30, 3.5, 7.5] },
  { nom: 'ESTIA Bidart',               groupe: 'Autre',      perfs: [40000, 88, 5500, 20, 3.5, 8.0] },
  { nom: 'EIGSI La Rochelle',          groupe: 'Autre',      perfs: [38000, 86, 7500, 22, 3.0, 7.5] },
]

// =============================================================================
//  PROFILS PRÉSÉLECTIONNÉS — boutons rapides dans la sidebar
// =============================================================================

export type Preset = {
  id: string
  label: string
  icone: string
  description: string
  poids: [number, number, number, number, number, number]
}

export const PRESETS: Preset[] = [
  {
    id: 'balance',
    label: 'Équilibré',
    icone: '⚖️',
    description: 'Tous les critères au même niveau',
    poids: [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
  },
  {
    id: 'salary',
    label: 'Carriériste',
    icone: '💰',
    description: 'Priorité salaire + emploi',
    poids: [0.40, 0.30, 0.05, 0.05, 0.05, 0.15],
  },
  {
    id: 'student',
    label: 'Étudiant',
    icone: '🎓',
    description: 'Vie associative + accessibilité',
    poids: [0.10, 0.10, 0.10, 0.25, 0.10, 0.35],
  },
  {
    id: 'ecolo',
    label: 'Engagé',
    icone: '🌍',
    description: 'DD&RS + diversité sociale',
    poids: [0.10, 0.10, 0.20, 0.15, 0.35, 0.10],
  },
  {
    id: 'budget',
    label: 'Petit budget',
    icone: '💸',
    description: 'Coût scolarité prioritaire',
    poids: [0.10, 0.20, 0.45, 0.10, 0.05, 0.10],
  },
]
