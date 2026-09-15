import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = (await getCollection('posts')).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );
  return rss({
    title: 'Shopping Gems — Best Online Shopping Blogs, Coupons & Deals',
    description: 'Sale calendars, coupons and honest shopping guides from Shopping Gems.',
    site: context.site ?? 'http://localhost:4321',
    items: posts.map((p) => ({
      title: p.data.title,
      description: p.data.description,
      pubDate: p.data.pubDate,
      link: `/posts/${p.slug}/`,
      categories: [p.data.category, ...p.data.tags],
    })),
    customData: '<language>en</language>',
  });
}
