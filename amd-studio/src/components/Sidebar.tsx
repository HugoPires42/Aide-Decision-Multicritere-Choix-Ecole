import { motion } from 'framer-motion'
import { Settings2, Calculator, Wand2, Play } from 'lucide-react'
import { CRITERES, PRESETS, type Preset } from '../lib/data'
import { type MethodeId } from '../lib/methods'
import { WeightControl } from './WeightControl'
import { MethodSelector } from './MethodSelector'
import { PresetChips } from './PresetChips'

type Props = {
  poids: number[]
  methode: MethodeId
  onPoidsChange: (idx: number, v: number) => void
  onPresetPick: (p: Preset['poids']) => void
  onMethodeChange: (m: MethodeId) => void
  onLaunch: () => void
}

/**
 * Panneau latéral gauche — saisie des poids, choix de la méthode et bouton
 * d'action principal. Fenêtre fixée à 400 px de largeur sur grand écran.
 */
export function Sidebar({
  poids,
  methode,
  onPoidsChange,
  onPresetPick,
  onMethodeChange,
  onLaunch,
}: Props) {
  const sommePoids = poids.reduce((a, b) => a + b, 0)

  return (
    <aside className="space-y-4">

      {/* ── Carte 1 : profil étudiant ─────────────────────────────────── */}
      <section className="card p-5">
        <header className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-violet-100 flex items-center justify-center">
              <Settings2 className="w-4 h-4 text-violet-600" />
            </div>
            <div>
              <h2 className="text-base font-bold text-stone-900">Ton profil</h2>
              <p className="text-xs text-stone-500">Pondère chaque critère</p>
            </div>
          </div>
          <div className="text-right">
            <div className="font-mono text-xs text-stone-400">total</div>
            <div className="font-mono text-sm font-bold text-violet-700 tabular-nums">
              {sommePoids.toFixed(2)}
            </div>
          </div>
        </header>

        <div className="space-y-3.5">
          {CRITERES.map((c, idx) => (
            <WeightControl
              key={c.id}
              critere={c}
              value={poids[idx]}
              onChange={v => onPoidsChange(idx, v)}
            />
          ))}
        </div>

        {/* Profils-types */}
        <div className="mt-5 pt-4 border-t border-stone-100">
          <div className="flex items-center gap-1.5 mb-2.5">
            <Wand2 className="w-3.5 h-3.5 text-stone-400" />
            <span className="text-xs font-semibold text-stone-500 uppercase tracking-wider">
              Profils types
            </span>
          </div>
          <PresetChips onPick={onPresetPick} />
        </div>
      </section>

      {/* ── Carte 2 : modèle de décision ──────────────────────────────── */}
      <section className="card p-5">
        <header className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-lg bg-fuchsia-100 flex items-center justify-center">
            <Calculator className="w-4 h-4 text-fuchsia-600" />
          </div>
          <div>
            <h2 className="text-base font-bold text-stone-900">Méthode AMD</h2>
            <p className="text-xs text-stone-500">Choisis ton modèle de décision</p>
          </div>
        </header>
        <MethodSelector value={methode} onChange={onMethodeChange} />
      </section>

      {/* ── Bouton de lancement ───────────────────────────────────────── */}
      <motion.button
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.98 }}
        onClick={onLaunch}
        className="relative w-full overflow-hidden rounded-2xl group"
      >
        <div className="absolute inset-0 bg-gradient-to-br from-violet-600 via-fuchsia-600 to-pink-500" />
        <div className="absolute inset-0 bg-gradient-to-br from-violet-700 via-fuchsia-700 to-pink-600
                        opacity-0 group-hover:opacity-100 transition-opacity" />
        <div className="absolute inset-0 opacity-50 mix-blend-overlay"
             style={{ backgroundImage: 'radial-gradient(circle at 30% 50%, white 0%, transparent 60%)' }} />

        <div className="relative px-6 py-4 flex items-center justify-center gap-3 text-white">
          <Play className="w-5 h-5 fill-white" />
          <span className="font-bold tracking-wide uppercase text-sm">
            Lancer la recherche du compromis
          </span>
        </div>
      </motion.button>

      <p className="text-center text-xs text-stone-400 pt-2">
        M1 MIAGE · Décision Multicritère · Dauphine-PSL
      </p>
    </aside>
  )
}
