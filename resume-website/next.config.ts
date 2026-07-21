import type { NextConfig } from "next";

const previewBasePath = process.env.PREVIEW_BASE_PATH;
const staticExport = process.env.STATIC_EXPORT === "1" || Boolean(previewBasePath);

const nextConfig: NextConfig = {
  ...(staticExport
    ? {
        output: "export",
        ...(previewBasePath
          ? {
              basePath: previewBasePath,
              assetPrefix: `${previewBasePath}/`,
            }
          : {}),
      }
    : {}),
};

export default nextConfig;
