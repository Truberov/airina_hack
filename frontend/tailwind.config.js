/** @type {import('tailwindcss').Config} */
export default {
  prefix: 'tw-',
  content: [
    './pages/**/*.{vue}',
    './components/**/*.{vue}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#20808d',
        secondary: '#13343b',
      },
    },
    screens: {
      desktop: '1440px',
      laptop: '1000px',
      tablet: '640px',
      mobile: '320px',
    },
  },
  plugins: [],
};
