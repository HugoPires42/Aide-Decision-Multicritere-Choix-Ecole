import { motion } from 'framer-motion'
import { Trophy, TrendingUp } from 'lucide-react'
import { type Classement, METHODES, type MethodeId } from '../lib/methods'

type Props = {
  resultat: Classement | null
  methode: MethodeId
}

/**
 * Carte HÉRO : met en scène l'école n°1.
 * Trophée animé, gros score, barre de progression dégradée, badge de méthode.
 */
export function HeroCard({ resultat, methode }: Props) {
  const meta = METHODES.find(m => m.id === methode)!

  if (!resultat) {
    return (
      <div className="card p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-3 rounded-2xl bg-stone-100
                        flex items-center justify-center">
          <Trophy className="w-8 h-8 text-stone-400" />
        </div>
        <p className="text-stone-500 text-sm">
          Choisis ton profil et lance la recherche pour découvrir l'école
          qui te correspond le mieux.
        </p>
      </div>
    )
  }

  const isElectre = methode === 'electre'
  const scoreAffiche = isElectre
    ? `${resultat.score > 0 ? '+' : ''}${Math.round(resultat.score)}`
    : resultat.score.toFixed(1)

  const fillColor = resultat.scoreNormalise >= 75
    ? 'from-emerald-400 to-emerald-600'
    : resultat.scoreNormalise >= 50
      ? 'from-violet-500 to-fuchsia-600'
      : resultat.scoreNormalise >= 25
        ? 'from-amber-400 to-orange-500'
        : 'from-rose-400 to-rose-600'

  return (
    <motion.div
      key={resultat.ecole.nom + methode}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="card relative overflow-hidden"
    >
      {/* Fond dégradé doux */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-50/60 via-white to-fuchsia-50/40" />
      <div className="absolute -top-12 -right-12 w-48 h-48 rounded-full
                      bg-gradient-to-br from-amber-200/30 to-amber-300/10 blur-2xl" />

      <div className="relative p-6">
        <div className="flex items-start gap-5">
          {/* Trophée animé */}
          <motion.div
            initial={{ rotate: -15, scale: 0.7 }}
            animate={{ rotate: 0, scale: 1 }}
            transition={{ type: 'spring', stiffness: 200, damping: 12 }}
            className="relative shrink-0"
          >
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 blur-md opacity-40" />
            <div className="relative w-20 h-20 rounded-2xl bg-gradient-to-br
                            from-amber-300 via-amber-400 to-amber-600
                            shadow-lg shadow-amber-500/30
                            flex flex-col items-center justify-center">
              <Trophy className="w-7 h-7 text-white drop-shadow" fill="white" />
              <div className="text-white font-bold text-[10px] mt-0.5 tracking-wider">#1</div>
            </div>
          </motion.div>

          <div className="flex-1 min-w-0">
            {/* Badge de méthode */}
            <div className="flex items-center gap-2 mb-1">
              <span className="chip bg-violet-100 text-violet-700">
                <TrendingUp className="w-3 h-3" />
                Champion {meta.label}
              </span>
              <span className="chip bg-stone-100 text-stone-600">
                {resultat.ecole.groupe}
              </span>
            </div>

            {/* Nom de l'école */}
            <motion.h2
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
              className="text-3xl font-extrabold text-stone-900 tracking-tight leading-tight"
            >
              {resultat.ecole.nom}
            </motion.h2>

            <p className="text-sm text-stone-500 mt-1">
              {meta.description}
            </p>
          </div>

          {/* Gros score à droite */}
          <div className="text-right shrink-0">
            <motion.div
              key={scoreAffiche}
              initial={{ scale: 1.3, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 18 }}
              className="font-mono text-5xl font-extrabold tabular-nums
                         bg-gradient-to-br from-violet-600 to-fuchsia-600
                         bg-clip-text text-transparent leading-none"
            >
              {scoreAffiche}
            </motion.div>
            <div className="text-xs text-stone-400 mt-1.5 font-semibold uppercase tracking-wider">
              {meta.scoreLibelle}
            </div>
          </div>
        </div>

        {/* Barre de progression du score */}
        <div className="mt-5 pt-4 border-t border-stone-100">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-xs font-semibold text-stone-500 uppercase tracking-wider">
              Score d'agrégation
            </span>
            <span className="text-xs font-mono text-stone-400">
              {resultat.scoreNormalise.toFixed(1)} / 100
            </span>
          </div>
          <div className="h-3 rounded-full bg-stone-100 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${resultat.scoreNormalise}%` }}
              transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
              className={`h-full rounded-full bg-gradient-to-r ${fillColor}
                          shimmer-bar`}
              style={{
                backgroundImage: 'linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%)',
              }}
            />
          </div>
        </div>
      </div>
    </motion.div>
  )
}
