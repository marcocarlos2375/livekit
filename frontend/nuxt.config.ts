export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],

  runtimeConfig: {
    livekitApiKey: process.env.LIVEKIT_API_KEY,
    livekitApiSecret: process.env.LIVEKIT_API_SECRET,
    public: {
      livekitUrl: process.env.LIVEKIT_URL || 'wss://test-n6s9zje1.livekit.cloud'
    }
  },

  app: {
    head: {
      title: 'Interview Simulator',
      meta: [
        { name: 'description', content: 'AI-powered job interview practice' }
      ]
    }
  }
})
