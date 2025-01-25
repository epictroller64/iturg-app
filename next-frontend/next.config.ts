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
      }
    ],
  },
};

export default nextConfig;
