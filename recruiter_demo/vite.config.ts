import { defineConfig, type ProxyOptions } from "vite";
import react from "@vitejs/plugin-react";

/**
 * ADK api_server uses Origin-check middleware on POST. The browser sends
 * Origin: http://localhost:5173 while the proxied Host is :8000 → 403
 * "Forbidden: origin not allowed". Stripping Origin makes the request pass
 * (see google.adk.cli.adk_web_server._OriginCheckMiddleware).
 */
function adkProxy(): ProxyOptions {
  const target = "http://127.0.0.1:8000";
  return {
    target,
    changeOrigin: true,
    configure(proxy) {
      proxy.on("proxyReq", (proxyReq) => {
        proxyReq.removeHeader("origin");
        proxyReq.removeHeader("referer");
      });
    },
  };
}

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    strictPort: true,
    port: 5173,
    proxy: {
      "/run": adkProxy(),
      "/run_sse": adkProxy(),
      "/apps": adkProxy(),
      "/list-apps": adkProxy(),
    },
  },
});
