import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        tapas: resolve(__dirname, 'tapas.html'),
        packages: resolve(__dirname, 'packages.html'),
        planner: resolve(__dirname, 'planner.html'),
        about: resolve(__dirname, 'about.html'),
        contact: resolve(__dirname, 'contact.html')
      }
    }
  }
});
