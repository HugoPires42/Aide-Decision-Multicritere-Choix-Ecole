import { motion } from 'framer-motion'
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, ResponsiveContainer,
} from 'recharts'
import { Activity } from 'lucide-react'
import { CRITERES } from '../lib/data'
import { type Classement } from '../lib/methods'

type Props = {
  resultat: Classement | null
}

/**
 * Radar chart des 6 utilités normalisées de l'école n°1.
 * Permet de visualiser d'un coup d'œil la "forme" du profil :
 *   un profil rond = équilibré, un profil pointu = spécialisé.
 */
export function RadarProfile({ resultat }: Props) {
  if (!resultat) return null

  // Transformation pour Recharts
  const data = CRITERES.map((c, i) => ({
    critere: c.label.split(' ')[0],   // version courte pour le radar
    utilite: Math.round(resultat.utilites[i]),
    fullMark: 100,
  }))

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1, duration: 0.4 }}
      className="card p-5"
    >
      <header className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center">
            <Activity className="w-4 h-4 text-emerald-600" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-stone-900">Profil radar</h3>
            <p className="text-xs text-stone-500">Forces & faiblesses sur les 6 critères</p>
          </div>
        </div>
      </header>

      <div className="h-[260px] -mx-2">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data} margin={{ top: 8, right: 24, bottom: 8, left: 24 }}>
            <defs>
              <linearGradient id="radarFill" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#a78bfa" stopOpacity={0.7} />
                <stop offset="100%" stopColor="#ec4899" stopOpacity={0.5} />
              </linearGradient>
            </defs>
            <PolarGrid stroke="#e7e5e4" strokeDasharray="2 4" />
            <PolarAngleAxis
              dataKey="critere"
              tick={{ fontSize: 11, fontWeight: 600, fill: '#57534e' }}
            />
            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={{ fontSize: 9, fill: '#a8a29e' }}
              axisLine={false}
            />
            <Radar
              name="Utilité"
              dataKey="utilite"
              stroke="#7c3aed"
              strokeWidth={2}
              fill="url(#radarFill)"
              fillOpacity={1}
              isAnimationActive
              animationDuration={800}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  )
}
