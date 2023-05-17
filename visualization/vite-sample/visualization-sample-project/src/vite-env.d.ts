/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_DIAGRAM_TYPE: string
  }

  
interface ImportMeta {
    readonly env: ImportMetaEnv
  }