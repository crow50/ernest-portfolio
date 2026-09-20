export const site = {
  name: 'Ernest L. Baker',
  title: 'DevSecOps Engineer',

  siteTitle: 'Ernest Baker | DevSecOps Engineer',
  description:
    'Senior Systems Analyst turned DevSecOps Engineer. Container scanning, SBOMs, secrets detection, and ten years automating utility infrastructure. Army veteran.',

  intro:
    "I'm a DevSecOps Engineer, with ten years in systems analysis, network administration, and process automation. I work on secrets scanning, container hardening, and software supply-chain analysis for the pipelines I build. I'm an Army veteran, and I'm finishing a cyber security degree at Stetson.",

  contact: {
    email: 'ernestleroybaker@gmail.com',
    location: 'DeLand, FL',
    /** Also hardcoded in the .print-phone rule in styles/global.css. Change both. */
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
