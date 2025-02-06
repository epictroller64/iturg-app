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
      }
    ],
  },
};

export default nextConfig;
