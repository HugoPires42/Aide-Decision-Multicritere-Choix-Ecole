import { Compass, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'
import { ECOLES } from '../lib/data'

/**
 * Bandeau supérieur de l'application.
 * Dégradé violet → rose, logo "compas", titre et statistiques rapides.
 */
export function Header() {
  return (
    <header className="relative overflow-hidden">
      {/* Fond dégradé animé */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-600 via-fuchsia-600 to-pink-500" />
      <div className="absolute inset-0 opacity-30"
           style={{
             backgroundImage: 'radial-gradient(circle at 30% 50%, white 0%, transparent 50%)',
           }} />

      {/* Cercles décoratifs flous */}
      <div className="absolute -top-20 -right-20 w-64 h-64 rounded-full bg-white/10 blur-3xl" />
      <div className="absolute -bottom-12 left-1/4 w-48 h-48 rounded-full bg-violet-300/20 blur-3xl" />

      <div className="relative max-w-[1440px] mx-auto px-6 py-5">
        <div className="flex items-center justify-between">
          {/* Logo + titre */}
          <div className="flex items-center gap-4">
            <motion.div
              initial={{ rotate: -10, scale: 0.8, opacity: 0 }}
              animate={{ rotate: 0, scale: 1, opacity: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 15 }}
              className="w-12 h-12 rounded-2xl bg-white shadow-lg shadow-violet-900/30
                         flex items-center justify-center"
            >
              <Compass className="w-6 h-6 text-violet-600" strokeWidth={2.5} />
            </motion.div>

            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold text-white tracking-tight">
                  AMD Studio
                </h1>
                <span className="chip bg-white/20 text-white backdrop-blur-sm border border-white/30">
                  <Sparkles className="w-3 h-3" />
                  v3.0
                </span>
              </div>
              <p className="text-sm text-white/80 mt-0.5">
                Choisis ton école d'ingénieurs avec la science de la décision
              </p>
            </div>
          </div>

          {/* Statistiques rapides */}
          <div className="hidden md:flex items-center gap-3">
            <Stat value={ECOLES.length.toString()} label="écoles" />
            <Stat value="5" label="méthodes" />
            <Stat value="6" label="critères" />
          </div>
        </div>
      </div>
    </header>
  )
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-xl px-4 py-2.5">
      <div className="text-xl font-bold text-white leading-none">{value}</div>
      <div className="text-xs text-white/80 mt-1">{label}</div>
    </div>
  )
}
