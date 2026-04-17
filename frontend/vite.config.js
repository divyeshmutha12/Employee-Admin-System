import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Proxy API requests to FastAPI so we avoid CORS issues in development.
    // Any request starting with /employees goes to http://localhost:8000.
    proxy: {
      "/employees": "http://localhost:8000",
    },
  },
});
