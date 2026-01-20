import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    host: true,            // allow access from network / Pinggy
    port: 5173,            // SvelteKit dev port
    strictPort: true,
    allowedHosts: [
	'yscld-91-10-184-139.a.free.pinggy.link',
	"ckgru-91-10-184-139.a.free.pinggy.link",
	'localhost'
	],
    proxy: {
      '/api': 'http://127.0.0.1:5000' // forward API calls to Flask
    }
  }
});