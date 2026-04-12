/// <reference types="vite/client" />

/**
 * TypeScript Type Definitions for Vite Environment Variables
 * This ensures that 'import.meta.env' is correctly typed within the application.
 */
interface ImportMetaEnv {
  // The base URL for the backend API
  readonly VITE_API_URL: string
  // more env variables...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
