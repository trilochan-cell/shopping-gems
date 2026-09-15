import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    category: z.string().default('Online Shopping'),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    views: z.number().default(0),
    featured: z.boolean().default(false),
    dealUrl: z.string().optional(),
  }),
});

export const collections = { posts };
