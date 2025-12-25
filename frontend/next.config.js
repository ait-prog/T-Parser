/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export', // Для статического экспорта (GitHub Pages)
  trailingSlash: true,
  basePath: process.env.NODE_ENV === 'production' ? '/T-Parser' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/T-Parser' : '',
  images: {
    unoptimized: true, // Для статического экспорта
    domains: ['krisha.kz'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig

