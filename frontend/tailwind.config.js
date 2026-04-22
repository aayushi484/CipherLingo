/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        arch: {
          bg: '#E9E9E9',
          surface: '#ffffff',
          dark: '#0f0f0f',
          text: '#111111',
          muted: '#888888',
          border: '#e0e0e0',
        }
      },
      fontFamily: {
        sans: ['"Helvetica Neue"', 'Helvetica', 'Inter', 'Arial', 'sans-serif'],
      },
      letterSpacing: {
        widest: '.25em',
      }
    },
  },
  plugins: [],
}
