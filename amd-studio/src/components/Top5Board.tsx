import { motion } from 'framer-motion'
import { Layers } from 'lucide-react'
import { CRITERES } from '../lib/data'
import { type Classement, type MethodeId } from '../lib/methods'

type Props = {
  classement: Classement[]
  methode: MethodeId
}

const MEDAILLES = [
  { emoji: '🥇', tone: 'from-amber-100 to-yellow-50',   ring: 'ring-amber-300' },
  { emoji: '🥈', tone: 'from-slate-100 to-slate-50',     ring: 'ring-slate-300' },
  { emoji: '🥉', tone: 'from-orange-100 to-amber-50',    ring: 'ring-orange-300' },
  { emoji: '4',  tone: 'from-stone-50 to-stone-50',      ring: 'ring-stone-200' },
  { emoji: '5',  tone: 'from-stone-50 to-stone-50',      ring: 'ring-stone-200' },
]

/**
 * Liste des 5 premières écoles avec leur score, leurs 2 critères les plus
 * forts (mini-icônes), et une barre de score à droite.
 */
export function Top5Board({ classement, methode }: Props) {
  if (classement.length === 0) return null
  const top5 = classement.slice(0, 5)
  const isElectre = methode === 'electre'

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2, duration: 0.4 }}
      className="card p-5"
    >
      <header className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-fuchsia-100 flex items-center justify-center">
            <Layers className="w-4 h-4 text-fuchsia-600" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-stone-900">Horizon des possibles</h3>
            <p className="text-xs text-stone-500">Les 5 écoles les plus alignées avec ton profil</p>
          </div>
        </div>
        <span className="chip bg-stone-100 text-stone-600">
          5 / {classement.length}
        </span>
      </header>

      <div className="space-y-2">
        {top5.map((r, idx) => (
          <Row5 key={r.ecole.nom} entry={r} idx={idx} isElectre={isElectre} />
        ))}
      </div>
    </motion.div>
  )
}

function Row5({
  entry, idx, isElectre,
}: { entry: Classement; idx: number; isElectre: boolean }) {
  const meda = MEDAILLES[idx]
  const isTop = idx === 0

  // 2 critères les plus forts
  const indicesTries = entry.utilites
    .map((u, j) => ({ u, j }))
    .sort((a, b) => b.u - a.u)
    .slice(0, 2)

  const scoreAffiche = isElectre
    ? `${entry.score > 0 ? '+' : ''}${Math.round(entry.score)}`
    : entry.score.toFixed(1)

  return (
    <motion.div
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: idx * 0.06, duration: 0.3 }}
      className={`grid grid-cols-[auto_1fr_auto_auto] items-center gap-3
                  p-3 rounded-xl bg-gradient-to-r ${meda.tone}
                  border ${isTop ? 'border-amber-200' : 'border-stone-100'}
                  ring-1 ${meda.ring}/30
                  hover:scale-[1.005] transition-transform`}
    >
      {/* Médaille */}
      <div className={`w-10 h-10 rounded-xl bg-white shadow-sm
                       flex items-center justify-center
                       ${idx < 3 ? 'text-xl' : 'font-mono font-bold text-stone-500'}`}>
        {meda.emoji}
      </div>

      {/* Nom + groupe */}
      <div className="min-w-0">
        <div className={`text-sm leading-tight truncate
                         ${isTop ? 'font-bold text-stone-900' : 'font-semibold text-stone-800'}`}>
          {entry.ecole.nom}
        </div>
        <div className="text-[11px] text-stone-500 mt-0.5 flex items-center gap-1.5">
          <span>{entry.ecole.groupe}</span>
          <span className="text-stone-300">·</span>
          <span className="font-medium">Forces :</span>
          {indicesTries.map(({ j }) => (
            <span
              key={j}
              className="inline-flex items-center gap-0.5"
              title={CRITERES[j].label}
            >
              <span>{CRITERES[j].icone}</span>
            </span>
          ))}
        </div>
      </div>

      {/* Barre de score */}
      <div className="hidden sm:block w-32">
        <div className="h-1.5 rounded-full bg-white/70 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${entry.scoreNormalise}%` }}
            transition={{ delay: 0.2 + idx * 0.07, duration: 0.6 }}
            className="h-full rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-500"
          />
        </div>
        <div className="text-[10px] text-stone-500 mt-1 text-right font-mono tabular-nums">
          {entry.scoreNormalise.toFixed(0)} / 100
        </div>
      </div>

      {/* Score numérique */}
      <div className="text-right shrink-0">
        <div className={`font-mono font-bold tabular-nums
                         ${isTop ? 'text-2xl text-violet-700' : 'text-lg text-stone-700'}`}>
          {scoreAffiche}
        </div>
      </div>
    </motion.div>
  )
}
