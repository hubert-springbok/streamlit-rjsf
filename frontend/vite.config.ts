import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import viteTsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
    // base: '/component/react_jsonform_component.react_jsonform_component',
    base: '',
    plugins: [react(), viteTsconfigPaths()],
    server: {    
        // this ensures that the browser opens upon server start
        open: true,
        port: 3000, 
    },
    build: {
        chunkSizeWarningLimit: 1000,
        outDir: "../streamlit_rjsf/build"
    }
})