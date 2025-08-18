/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./src/App.tsx",
    "./src/main.tsx"
  ],
  darkMode: 'class', // Enable dark mode with class strategy
  theme: {
    extend: {},
  },
  plugins: [],
  safelist: [
    'bg-blue-500',
    'text-white',
    'rounded-md',
    'hover:bg-blue-600',
    'bg-gray-100',
    'text-gray-600',
    'bg-red-100',
    'text-red-700',
    'bg-green-100',
    'text-green-700',
    // Dark mode classes
    'dark:bg-gray-900',
    'dark:bg-gray-800',
    'dark:text-white',
    'dark:text-gray-300',
    'dark:border-gray-700',
    'dark:hover:bg-gray-700',
    'dark:hover:text-white'
  ]
} 