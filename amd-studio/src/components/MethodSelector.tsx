import { motion } from 'framer-motion'
import { METHODES, type MethodeId } from '../lib/methods'

type Props = {
  value: MethodeId
  onChange: (m: MethodeId) => void
}

/**
 * Sélecteur de méthode AMD sous forme de cartes empilées.
 * La carte sélectionnée bénéficie d'un fond dégradé, bordure violette et
 * d'un layout id pour l'animation de transition Framer Motion.
 */
export function MethodSelector({ value, onChange }: Props) {
  return (
    <div className="space-y-2">
      {METHODES.map(m => {
        const selected = m.id === value
        return (
          <button
            key={m.id}
            onClick={() => onChange(m.id)}
            className="relative w-full text-left rounded-xl overflow-hidden
                       focus:outline-none focus:ring-2 focus:ring-violet-400 focus:ring-offset-2"
          >
            {/* Fond animé pour la sélection */}
            {selected && (
              <motion.div
                layoutId="method-bg"
                className="absolute inset-0 bg-gradient-to-br from-violet-50 to-fuchsia-50
                           border-2 border-violet-500 rounded-xl"
                transition={{ type: 'spring', stiffness: 400, damping: 30 }}
              />
            )}

            {/* Fond carte inactive */}
            {!selected && (
              <div className="absolute inset-0 bg-white border border-stone-200
                              rounded-xl transition-colors hover:bg-stone-50
                              hover:border-stone-300" />
            )}

            {/* Contenu */}
            <div className="relative flex items-start gap-3 p-3">
              {/* Icône carrée */}
              <div className={`shrink-0 w-9 h-9 rounded-lg flex items-center justify-center
                               font-bold text-base transition-colors
                               ${selected
                                 ? 'bg-violet-600 text-white shadow-md shadow-violet-500/40'
                                 : 'bg-stone-100 text-stone-500'}`}>
                {m.icone}
              </div>

              {/* Texte */}
              <div className="flex-1 min-w-0">
                <div className={`text-sm font-bold leading-tight
                                 ${selected ? 'text-violet-900' : 'text-stone-800'}`}>
                  {m.label}
                </div>
                <div className={`text-xs leading-snug mt-0.5
                                 ${selected ? 'text-violet-700' : 'text-stone-500'}`}>
                  {m.description}
                </div>
              </div>

              {/* Indicateur de sélection */}
              {selected && (
                <motion.div
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="shrink-0 w-2 h-2 rounded-full bg-violet-600 mt-3.5"
                />
              )}
            </div>
          </button>
        )
      })}
    </div>
  )
}
