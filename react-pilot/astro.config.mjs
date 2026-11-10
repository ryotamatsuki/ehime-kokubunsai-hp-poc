import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

export default defineConfig({
  site: 'https://ryotamatsuki.github.io',
  base: '/ehime-kokubunsai-hp-poc/react-pilot',
  output: 'static',
  integrations: [react()],
});
