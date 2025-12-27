/** @type {import('next').NextConfig} */
// Для GitHub Pages всегда используем basePath
// Можно переопределить через переменную окружения GITHUB_PAGES_BASE_PATH
const githubPagesBasePath = process.env.GITHUB_PAGES_BASE_PATH || '/T-Parser'
const isProd = process.env.NODE_ENV === 'production' || process.env.GITHUB_ACTIONS === 'true'
const basePath = isProd ? githubPagesBasePath : ''

const nextConfig = {
  reactStrictMode: true,
  output: 'export', // Для статического экспорта (GitHub Pages)
  trailingSlash: true,
  basePath: basePath,
  assetPrefix: basePath,
  images: {
    unoptimized: true, // Для статического экспорта
    domains: ['krisha.kz'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}

// Логирование для отладки
console.log('Next.js Config:', {
  NODE_ENV: process.env.NODE_ENV,
  GITHUB_ACTIONS: process.env.GITHUB_ACTIONS,
  basePath: basePath,
  isProd: isProd
})

module.exports = nextConfig

