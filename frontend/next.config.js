/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  basePath: process.env.NODE_ENV === 'production' ? '/T-Parser' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/T-Parser' : '',
  images: {
    unoptimized: true,
    domains: ['krisha.kz'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
