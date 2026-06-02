/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      colors: {
        // Couleurs spécifiques aux 6 critères AMD
        crit: {
          salaire: '#8b5cf6',   // violet (g1)
          emploi:  '#3b82f6',   // bleu (g2)
          cout:    '#f43f5e',   // rose-rouge (g3 - à minimiser)
          divers:  '#10b981',   // émeraude (g4)
          ddrs:    '#14b8a6',   // teal (g5)
          vie:     '#f59e0b',   // ambre (g6)
        },
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(124, 58, 237, 0.4)' },
          '50%':      { boxShadow: '0 0 0 12px rgba(124, 58, 237, 0)' },
        },
        'shimmer': {
          '0%':   { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'shimmer': 'shimmer 3s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
