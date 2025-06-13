// https://nuxt.com/docs/api/configuration/nuxt-config
const isDev = process.env.NODE_ENV === 'development'
const isProd = process.env.NODE_ENV === 'production'

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', 'shadcn-nuxt', '@vite-pwa/nuxt'],
  css: ['~/assets/css/tailwind.css'],
  
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: './components/ui'
  },
  
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  
  // Vite configuration
  vite: {
    css: {
      devSourcemap: true,
    }
  },
  
  // Development server configuration
  nitro: {
    esbuild: {
      options: {
        target: 'esnext'
      }
    },
    // Only apply cache headers in production
    routeRules: isProd ? {
      '/**': {
        headers: {
          'Cache-Control': 'max-age=31536000, immutable'
        }
      }
    } : {}
  },
  
  // Experimental features to improve CSS handling
  experimental: {
    payloadExtraction: false,
  },

  // Enable SSR for consistent styling
  ssr: true,
  
  // App configuration
  app: {
    head: {
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
    },
  },
  
  pwa: {
    // Completely disable PWA in development to prevent caching issues  
    disable: isDev,
    manifest: {
      name: 'AI Resume Analyzer & Job Recommender',
      short_name: 'ResumeAI',
      description: 'Enhance your resume and find job opportunities.',
      icons: [
        {
          src: 'icons/test.jpg',
          sizes: '64x64',
          type: 'image/jpg'
        }
      ]
    },
    workbox: {
      navigateFallback: '/',
      globPatterns: [],
      globIgnores: [
        '**/node_modules/***',
        '_nuxt/builds/***'
      ],
    },
    devOptions: {
      enabled: false, // Disable in development
      type: 'module',
      suppressWarnings: true,
    },
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    }
  },

  // Development server configuration
  devServer: {
    port: 3000,
    host: '0.0.0.0'
  },
  
  // Development-specific configurations
  ...(process.env.NODE_ENV === 'development' ? {
    // Force CSS regeneration in development
    hooks: {
      'build:before': () => {
        console.log('🔄 Building CSS...')
      }
    }
  } : {}),

  // Vue configuration to handle hydration warnings
  vue: {
    compilerOptions: {
      isCustomElement: (tag) => false,
    }
  }
})