import { useMemo, useState } from 'react'
import { AnimatePresence } from 'framer-motion'

import { Header } from './components/Header'
import { Sidebar } from './components/Sidebar'
import { HeroCard } from './components/HeroCard'
import { RadarProfile } from './components/RadarProfile'
import { PerformanceGrid } from './components/PerformanceGrid'
import { Top5Board } from './components/Top5Board'

import { classer, type Classement, type MethodeId } from './lib/methods'

/**
 * Composant racine. Centralise :
 *   - état des poids (6 sliders),
 *   - méthode AMD sélectionnée,
 *   - dernier classement calculé,
 *   - actions (changement poids/preset/méthode, lancement).
 */
export default function App() {
  // 6 poids initialisés à 1/6 (profil équilibré)
  const [poids, setPoids] = useState<number[]>(
    Array(6).fill(Math.round((1/6) * 100) / 100)
  )
  const [methode, setMethode] = useState<MethodeId>('somme')

  // Lancement initial pour avoir un état "champion" dès l'arrivée
  const [classement, setClassement] = useState<Classement[]>(() =>
    classer('somme', Array(6).fill(1/6))
  )

  const topResult = classement[0] ?? null

  // Recalcul instantané à chaque changement
  function recalculer(nextPoids?: number[], nextMethode?: MethodeId) {
    const p = nextPoids ?? poids
    const m = nextMethode ?? methode
    setClassement(classer(m, p))
  }

  function changePoids(idx: number, v: number) {
    const next = poids.map((p, i) => (i === idx ? v : p))
    setPoids(next)
    recalculer(next, methode)
  }

  function pickPreset(p: number[]) {
    const next = p.map(v => Math.round(v * 100) / 100)
    setPoids(next)
    recalculer(next, methode)
  }

  function changeMethode(m: MethodeId) {
    setMethode(m)
    recalculer(poids, m)
  }

  // Le bouton "Lancer" force un recalcul (utile pour ressentir la transition)
  function launch() {
    recalculer(poids, methode)
  }

  // Statistique : combien d'écoles ex æquo en tête ? (utile pour la méthode Min)
  const exAequo = useMemo(() => {
    if (classement.length < 2) return 0
    const ref = classement[0].score
    return classement.filter(c => Math.abs(c.score - ref) < 1e-6).length
  }, [classement])

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 max-w-[1440px] mx-auto w-full px-4 sm:px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-[400px_1fr] gap-6">

          {/* ── PANNEAU GAUCHE ─────────────────────────────────────── */}
          <Sidebar
            poids={poids}
            methode={methode}
            onPoidsChange={changePoids}
            onPresetPick={pickPreset}
            onMethodeChange={changeMethode}
            onLaunch={launch}
          />

          {/* ── PANNEAU DROIT ──────────────────────────────────────── */}
          <section className="space-y-6">
            <AnimatePresence mode="wait">
              <HeroCard
                key={topResult?.ecole.nom ?? 'empty'}
                resultat={topResult}
                methode={methode}
              />
            </AnimatePresence>

            {/* Avertissement ex æquo (Méthode du Min) */}
            {exAequo > 5 && methode === 'min' && (
              <div className="rounded-xl bg-amber-50 border border-amber-200 p-4 text-sm text-amber-900">
                <span className="font-bold">{exAequo} écoles ex æquo</span> en tête —
                la méthode du Min crée des plateaux lorsque plusieurs écoles ont
                exactement le même critère minimum.
              </div>
            )}

            {/* Radar + Performances en grille 2 colonnes (1 sur mobile) */}
            <div className="grid grid-cols-1 xl:grid-cols-[1fr_1.2fr] gap-6">
              <RadarProfile resultat={topResult} />
              <PerformanceGrid resultat={topResult} />
            </div>

            <Top5Board classement={classement} methode={methode} />

            {/* Footer */}
            <footer className="text-center text-xs text-stone-400 pt-4 pb-2">
              Calculs effectués en temps réel sur 50 écoles d'ingénieurs ·
              Normalisation min-max relative à la base · TypeScript + React
            </footer>
          </section>

        </div>
      </main>
    </div>
  )
}
