// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/eslint-module',
    'nuxt-quasar-ui',
    'nuxt-mdi',
  ],
  quasar: {
    plugins: [
      'Notify',
    ],
    config: {
      brand: {
        primary: '#20808d',
        secondary: '#13343b',
      },
    },
  },
  css: ['@/assets/css/tailwind.css', '@/assets/css/main.css'],
  runtimeConfig: {
    baseURL: 'http://195.58.50.204:8080/api/v1',
    headers: {},
    public: {
      baseURL: 'http://195.58.50.204:8080/api/v1',
      headers: {},
    },
  },

});
