import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    category: z.string().default('Online Shopping'),
    tags: z.array(z.string()).default([]),
    faq: z.array(z.object({ question: z.string(), answer: z.string() })).default([]),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    views: z.number().default(0),
    featured: z.boolean().default(false),
    dealUrl: z.string().optional(),
  }),
});

const brands = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    tagline: z.string(),
    description: z.string(),
    website: z.string().url(),
    category: z.string().default('Shopping'),
    rating: z.number().min(0).max(5).default(4.5),
    reviews: z.number().default(0),
    maxDiscount: z.string().default('20%'),
    faq: z.array(z.object({ question: z.string(), answer: z.string() })).default([]),
  }),
});

const coupons = defineCollection({
  type: 'content',
  schema: z.object({
    brand: z.string(),
    title: z.string(),
    description: z.string(),
    type: z.enum(['code', 'deal']).default('code'),
    badge: z.string(),
    code: z.string().optional(),
    expiry: z.coerce.date(),
    verified: z.coerce.date().optional(),
    uses: z.number().default(0),
    terms: z.array(z.string()).default([]),
    labels: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
  }),
});

export const collections = { posts, brands, coupons };
