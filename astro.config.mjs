import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import rehypeTableScope from './src/plugins/rehype-table-scope.mjs';

export default defineConfig({
  site: 'http://localhost:4321',
  integrations: [mdx(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    shikiConfig: { theme: 'github-light' },
    rehypePlugins: [rehypeTableScope],
  }
});
