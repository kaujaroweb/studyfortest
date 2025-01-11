/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  mode: 'jit',
  content: [
   'templates/**/*.html',       // Archivos HTML principales       // Archivos CSS adicionales
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'], // Define the Poppins font
      },

    },
  },
  plugins: [],
}

