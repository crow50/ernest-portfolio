/**
 * Values that were scattered across Jekyll's _config.yml as theme "knobs".
 * Most of those knobs were the theme's on/off switches and disappeared with it;
 * what survives here is actual data.
 */
export const site = {
  name: 'Ernest L. Baker',
  title: 'DevSecOps Engineer',

  // Used for <title> and the meta description. The old description
  // ("A vain attempt to document my professional life") was the text Google
  // showed under the site name in search results.
  siteTitle: 'Ernest Baker | DevSecOps Engineer',
  description:
    'DevSecOps engineer and U.S. Army veteran building automated infrastructure and CI/CD pipelines with security built in from the start.',

  /**
   * Plain text, not HTML. The Jekyll value was an HTML string containing a <p>
   * tag; the component does the wrapping now.
   */
  intro:
    "I'm a Senior Systems Analyst transitioning into DevSecOps Engineering, with 10+ years in systems analysis, network administration, and process automation. I build automated infrastructure and CI/CD pipelines with security built in from the start: secrets scanning, container hardening, and software supply-chain analysis. Army veteran with a disciplined, mission-focused approach to solving infrastructure and security challenges.",

  contact: {
    email: 'ernestleroybaker@gmail.com',
    location: 'DeLand, FL',
    /**
     * PRINT ONLY. Deliberately excluded from the rendered web page and from
     * the JSON-LD block. The old site emitted this in a schema.org
     * <meta itemprop="telephone"> on every page load even though the visible
     * contact block was switched off -- so it was scrapeable while appearing hidden.
     * Consumed only by components/PrintContact.astro.
     */
    phone: '719.229.7102',
  },

  lookingForWork: true,

  social: {
    github: 'https://github.com/crow50',
    linkedin: 'https://www.linkedin.com/in/ernestlbaker',
    website: 'https://ernestbaker.me',
  },
} as const;

/** Where the shell lives. Referenced by robots.txt, _headers, and hello.js. */
export const SHELL_PATH = '/dev';
