import { useRef } from 'react'
import { motion } from 'framer-motion'
import type { Critere } from '../lib/data'

type Props = {
  critere: Critere
  value: number
  onChange: (v: number) => void
}

/**
 * Slider personnalisé pour un poids de critère.
 * Affiche l'icône, le nom, les bornes, le sens d'optimisation, et un
 * curseur interactif avec valeur en temps réel.
 */
export function WeightControl({ critere, value, onChange }: Props) {
  const trackRef = useRef<HTMLDivElement>(null)
  const dragging = useRef(false)

  // Conversion clic/glissement → valeur [0, 1] arrondie à 0.01
  function valueFromEvent(e: React.PointerEvent | PointerEvent) {
    if (!trackRef.current) return
    const rect = trackRef.current.getBoundingClientRect()
    const x = Math.max(0, Math.min(rect.width, e.clientX - rect.left))
    const v = Math.round((x / rect.width) * 100) / 100
    onChange(v)
  }

  function onPointerDown(e: React.PointerEvent) {
    dragging.current = true
    ;(e.target as HTMLElement).setPointerCapture(e.pointerId)
    valueFromEvent(e)
  }

  function onPointerMove(e: React.PointerEvent) {
    if (!dragging.current) return
    valueFromEvent(e)
  }

  function onPointerUp(e: React.PointerEvent) {
    dragging.current = false
    ;(e.target as HTMLElement).releasePointerCapture(e.pointerId)
  }

  const pct = Math.max(0, Math.min(1, value)) * 100
  const sensColor = critere.max ? 'text-emerald-600' : 'text-rose-500'
  const sensIcone = critere.max ? '▲' : '▼'

  return (
    <div className="group">
      {/* Ligne titre + valeur */}
      <div className="flex items-center justify-between mb-1.5">
        <div className="flex items-center gap-2">
          <span className="text-lg leading-none">{critere.icone}</span>
          <div>
            <div className="text-sm font-semibold text-stone-900 leading-tight">
              <span className="font-mono text-stone-400 mr-1">{critere.id}</span>
              {critere.label}
            </div>
            <div className="text-[10px] text-stone-400 leading-tight">
              {critere.bornes} {critere.unite}
              <span className={`ml-2 font-semibold ${sensColor}`}>
                {sensIcone} {critere.max ? 'maximiser' : 'minimiser'}
              </span>
            </div>
          </div>
        </div>
        <motion.div
          key={value.toFixed(2)}
          initial={{ scale: 1.2, opacity: 0.5 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.15 }}
          className="font-mono text-sm font-bold tabular-nums"
          style={{ color: critere.couleur }}
        >
          {value.toFixed(2)}
        </motion.div>
      </div>

      {/* Slider personnalisé */}
      <div
        ref={trackRef}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        className="relative h-7 flex items-center cursor-pointer select-none touch-none"
      >
        {/* Rail */}
        <div className="absolute inset-x-0 h-2 rounded-full bg-stone-100" />
        {/* Remplissage coloré */}
        <div
          className="absolute h-2 rounded-full"
          style={{
            width: `${pct}%`,
            backgroundColor: critere.couleur,
            boxShadow: `0 0 0 0 ${critere.couleur}40`,
          }}
        />
        {/* Thumb */}
        <motion.div
          animate={{ left: `${pct}%` }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
          className="absolute -translate-x-1/2 w-5 h-5 rounded-full bg-white
                     border-2 shadow-md hover:scale-110 transition-transform"
          style={{ borderColor: critere.couleur }}
        />
      </div>
    </div>
  )
}
