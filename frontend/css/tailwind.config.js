module.exports = {
  content: [
    "./public/**/*.{html,js}",
    "./assets/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        'primary-green': '#10B981',
        'primary-blue': '#3B82F6',
        'secondary-orange': '#F59E0B',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}