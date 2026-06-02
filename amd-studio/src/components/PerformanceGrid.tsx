import { motion } from 'framer-motion'
import { BarChart3 } from 'lucide-react'
import { CRITERES } from '../lib/data'
import { type Classement } from '../lib/methods'

type Props = {
  resultat: Classement | null
}

/**
 * Tableau des 6 performances de l'école n°1 avec :
 *   - icône colorée
 *   - valeur brute formatée
 *   - barre de progression normalisée [0; 100]
 *   - chip "Top", "Bon", "Moyen", "Faible"
 */
export function PerformanceGrid({ resultat }: Props) {
  if (!resultat) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.15, duration: 0.4 }}
      className="card p-5"
    >
      <header className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 rounded-lg bg-violet-100 flex items-center justify-center">
          <BarChart3 className="w-4 h-4 text-violet-600" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-stone-900">Performances détaillées</h3>
          <p className="text-xs text-stone-500">Brutes & normalisées sur les 50 écoles</p>
        </div>
      </header>

      <div className="space-y-2.5">
        {CRITERES.map((c, j) => {
          const brute = resultat.ecole.perfs[j]
          const u = resultat.utilites[j]
          return (
            <RowPerf
              key={c.id}
              icone={c.icone}
              code={c.id}
              label={c.label}
              brute={formatBrute(j, brute)}
              utilite={u}
              couleur={c.couleur}
              delay={0.05 + j * 0.04}
            />
          )
        })}
      </div>
    </motion.div>
  )
}

function formatBrute(j: number, val: number): string {
  if (j === 0 || j === 2) {
    return `${val.toLocaleString('fr-FR')} €`
  }
  if (j === 1 || j === 3) return `${val}%`
  if (j === 4) return `${val.toFixed(1)} / 5`
  return `${val.toFixed(1)} / 10`
}

function badgeFromUtilite(u: number) {
  if (u >= 80) return { label: 'Excellent', cls: 'bg-emerald-100 text-emerald-700' }
  if (u >= 60) return { label: 'Bon',       cls: 'bg-violet-100 text-violet-700' }
  if (u >= 40) return { label: 'Moyen',     cls: 'bg-amber-100 text-amber-700' }
  if (u >= 20) return { label: 'Faible',    cls: 'bg-orange-100 text-orange-700' }
  return { label: 'Critique', cls: 'bg-rose-100 text-rose-700' }
}

function RowPerf({
  icone, code, label, brute, utilite, couleur, delay,
}: {
  icone: string; code: string; label: string;
  brute: string; utilite: number; couleur: string; delay: number;
}) {
  const badge = badgeFromUtilite(utilite)
  return (
    <div className="grid grid-cols-[auto_1fr_auto_auto] items-center gap-3
                    py-2 border-b border-stone-100 last:border-0">
      {/* Icône + code/label */}
      <div className="flex items-center gap-2.5 min-w-0">
        <div
          className="w-9 h-9 rounded-lg flex items-center justify-center text-lg"
          style={{ backgroundColor: couleur + '18' }}
        >
          {icone}
        </div>
        <div className="min-w-0">
          <div className="text-sm font-semibold text-stone-900 leading-tight">
            <span className="font-mono text-stone-400 mr-1.5 text-xs">{code}</span>
            {label}
          </div>
          <div className="text-xs text-stone-500 mt-0.5">{brute}</div>
        </div>
      </div>

      {/* Barre de progression */}
      <div className="relative h-2 rounded-full bg-stone-100 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${utilite}%` }}
          transition={{ delay, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          className="absolute inset-y-0 left-0 rounded-full"
          style={{ backgroundColor: couleur }}
        />
      </div>

      {/* Valeur normalisée */}
      <div className="font-mono text-sm font-bold tabular-nums text-stone-700 w-12 text-right">
        {Math.round(utilite)}
      </div>

      {/* Chip qualité */}
      <span className={`chip ${badge.cls} w-20 justify-center`}>
        {badge.label}
      </span>
    </div>
  )
}
