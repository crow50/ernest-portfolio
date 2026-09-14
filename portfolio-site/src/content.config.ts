import { defineCollection, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

/**
 * YAML distinguishes "key absent" (undefined) from "key present but empty" (null).
 * A bare z.string().url().optional() accepts the first and throws on the second
 * with `Expected string, received null`, so an empty `url:` would fail the build.
 */
const optionalUrl = z.preprocess(
  (v) => (v === '' || v === null ? undefined : v),
  z.string().url().optional(),
);

/** Markdown-bearing: the `.md` body is the content, rendered via render(). */
const experience = defineCollection({
  loader: glob({ base: './src/content/experience', pattern: '**/*.md' }),
  schema: z.object({
    company: z.string(),
    position: z.string(),
    duration: z.string(), // display string, e.g. "November 2021 to Present"
    order: z.number().int().positive(), // 1 = most recent; explicit, no date parsing
  }),
});

const education = defineCollection({
  loader: glob({ base: './src/content/education', pattern: '**/*.md' }),
  schema: z.object({
    degree: z.string(),
    uni: z.string(),
    year: z.string(), // "May, 2027" is not a parseable date
    order: z.number().int().positive(),
    awards: z.array(z.string()).default([]),
  }),
});

/** Plain text. Rendered as bare expressions, never markdown-parsed. */
const projects = defineCollection({
  loader: file('./src/content/projects.yml'),
  schema: z.object({
    project: z.string(),
    role: z.string(),
    duration: z.string(),
    url: optionalUrl,
    description: z.string(),
  }),
});

const skills = defineCollection({
  loader: file('./src/content/skills.yml'),
  schema: z.object({
    skill: z.string(),
    description: z.string(),
  }),
});

const associations = defineCollection({
  loader: file('./src/content/associations.yml'),
  schema: z.object({
    organization: z.string(),
    role: z.string(),
    year: z.string(),
    url: optionalUrl,
    summary: z.string(),
  }),
});

/** Terminal-only. Never queried by index.astro. */
const notes = defineCollection({
  loader: glob({ base: './src/content/notes', pattern: '**/*.md' }),
  schema: z.object({
    path: z.string().startsWith('/home/ernest/'),
    title: z.string(),
  }),
});

export const collections = { experience, education, projects, skills, associations, notes };
