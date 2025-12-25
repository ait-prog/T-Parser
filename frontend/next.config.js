/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production'
const basePath = isProd ? '/T-Parser' : ''

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
if (isProd) {
  console.log('Production build with basePath:', basePath)
}

module.exports = nextConfig

