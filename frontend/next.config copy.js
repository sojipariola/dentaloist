//frontend/next.config.js

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove the rewrites() function completely
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  },
  reactStrictMode: true,
  images: {
    domains: ['localhost'],
  },
  // Add CORS headers for your own API routes if you have any
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, PUT, DELETE, OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ];
  },
};

module.exports = nextConfig;