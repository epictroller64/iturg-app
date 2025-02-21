import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.okidoki.st',
      },
      {
        protocol: 'https',
        hostname: '*.soov.ee',
      },
      {
        protocol: 'https',
        hostname: '*.upload.ee'
      },
      {
        protocol: 'https',
        hostname: 'i.imgur.com'
      },
      {
        protocol: 'https',
        hostname: 'business.ideal.ee'
      }
    ],
  },
};

export default nextConfig;
