import { PRESETS, type Preset } from '../lib/data'

type Props = {
  onPick: (poids: Preset['poids']) => void
}

/**
 * Boutons "profils-types" pour appliquer des poids prédéfinis en un clic.
 */
export function PresetChips({ onPick }: Props) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {PRESETS.map(p => (
        <button
          key={p.id}
          onClick={() => onPick(p.poids)}
          title={p.description}
          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-full
                     bg-stone-100 hover:bg-violet-100 hover:text-violet-900
                     text-stone-700 text-xs font-semibold
                     border border-stone-200 hover:border-violet-300
                     transition-all duration-150 active:scale-95"
        >
          <span>{p.icone}</span>
          {p.label}
        </button>
      ))}
    </div>
  )
}
