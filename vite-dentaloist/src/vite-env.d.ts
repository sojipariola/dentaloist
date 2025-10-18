/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string
  // add other VITE_ vars if needed later
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
