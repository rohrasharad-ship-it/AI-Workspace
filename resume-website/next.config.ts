import type { NextConfig } from "next";

const previewBasePath = process.env.PREVIEW_BASE_PATH;

const nextConfig: NextConfig = {
  ...(previewBasePath
    ? {
        output: "export",
        basePath: previewBasePath,
        assetPrefix: `${previewBasePath}/`,
      }
    : {}),
};

export default nextConfig;
