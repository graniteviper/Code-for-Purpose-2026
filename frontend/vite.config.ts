import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

/**
 * Vite Configuration File
 * Configures the build tool, development server, and path aliases.
 */
export default defineConfig({
  // Use the React plugin for Vite
  plugins: [react()],
  
  resolve: {
    alias: {
      // Allows using '@' as a shorthand for the './src' directory in imports
      "@": path.resolve(__dirname, "./src"),
    },
  },
  
  server: {
    // Proxy API requests to the backend server during local development
    // This avoids CORS issues and simplifies the frontend fetch calls
    proxy: {
      '/query': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
