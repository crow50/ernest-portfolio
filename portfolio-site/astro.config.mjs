// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://ernestbaker.me',

  integrations: [
    // The terminal is discoverable on purpose, not by search.
    sitemap({ filter: (page) => !page.includes('/dev') }),
  ],

  security: {
    // Emits a <meta http-equiv="content-security-policy"> per page, hashing
    // Astro's own bundled scripts and styles. The key lives under `security`,
    // not at the top level. public/_headers carries the rest; where both set a
    // directive the browser enforces the intersection.
    csp: {
      scriptDirective: {
        // Astro's meta CSP does not cover external scripts by default, so
        // without this /hello.js is blocked even when _headers allows it.
        resources: ["'self'"],
      },
    },
  },

  build: {
    // Keeps stylesheets external so style-src needs no 'unsafe-inline'.
    // Setting this back to 'auto' renders the site unstyled under CSP.
    inlineStylesheets: 'never',
  },

  // Downloaded and self-hosted at build time, so font-src stays 'self'.
  fonts: [
    {
      provider: fontProviders.google(),
      name: 'Lora',
      cssVariable: '--font-lora',
      weights: [400, 700],
      styles: ['normal', 'italic'],
      subsets: ['latin'],
    },
    {
      provider: fontProviders.google(),
      name: 'Open Sans',
      cssVariable: '--font-open-sans',
      weights: [300, 400, 700, 800],
      subsets: ['latin'],
    },
  ],

  vite: { plugins: [tailwindcss()] },
});
