import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://theorembank.example', // update to real URL later
  markdown: {
    // Enable $...$ inline math and $$...$$ block math rendering via KaTeX at runtime
    syntaxHighlight: 'prism',
  },
}); 