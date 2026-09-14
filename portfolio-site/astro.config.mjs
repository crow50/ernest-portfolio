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
    // Astro emits a <meta http-equiv="content-security-policy"> per page with
    // script-src/style-src hashes for its OWN bundled assets. Stable since
    // Astro 6 -- note it lives under `security`, not at the top level.
    //
    // public/_headers (Ernest, phase 4) carries what Astro cannot know about:
    // frame-ancestors, HSTS, Referrer-Policy, Permissions-Policy, X-Robots-Tag.
    // Both policies apply; the browser enforces the intersection.
    csp: {
      scriptDirective: {
        // REQUIRED for the phase 4 console breadcrumb. Astro does not cover
        // external scripts by default, so a plain /hello.js would be blocked
        // by Astro's own meta CSP even though _headers allows it. Adding
        // 'self' here is what makes the external-file approach work and keeps
        // us off the brittle inline-hash path.
        resources: ["'self'"],
      },
    },
  },

  build: {
    // LOAD-BEARING. Astro's default ('auto') inlines small stylesheets into
    // <style> tags. Keeping them external is what lets _headers ship a
    // style-src without 'unsafe-inline'. Changing this silently unstyles
    // the site under CSP.
    inlineStylesheets: 'never',
  },

  // Self-hosted at build time: no render-blocking request to Google, no
  // third-party origin in the CSP, and automatic fallback metrics for CLS.
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
