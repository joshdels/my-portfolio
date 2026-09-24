# SEO and Publishing

The site provides page-specific titles and descriptions, canonical URLs, Open Graph and Twitter previews, Person/WebSite/page structured data, `/sitemap.xml`, and `/robots.txt`.

## Before going live

1. Set the Wagtail Site hostname to the public domain and port to `443` for HTTPS. Avoid a localhost or internal hostname in production.
2. Confirm the homepage is the site root and publish the project index and project pages.
3. In Wagtail’s Promote tab, write an accurate SEO title and search description for each important page. Defaults use Joshua De Leon’s name and geospatial specialization; project descriptions supply project fallbacks.
4. Visit `/sitemap.xml` and inspect a page’s canonical URL. Both should use the public HTTPS domain.
5. Verify the domain in Google Search Console and submit the sitemap. Inspect the homepage and a project URL for indexing eligibility.
6. Check link previews, keyboard navigation, and mobile layouts. Measure deployed pages with PageSpeed Insights and monitor Search Console as field data becomes available.

## Project content employers can assess

Lead with a clear problem and your contribution. Use the existing content field for sections covering your role, approach, technical decisions, outcome, and lessons. Add source-code or demo links using project links; these appear near the summary.

Describe the relevant sector and technologies naturally. Do not claim energy, land, or infrastructure experience that a project does not demonstrate. Use measured results only when supported by evidence. Explain screenshots with captions and keep private client information out of public examples.

Use LinkedIn, GitHub, and your CV to link consistently to your portfolio and relevant case studies. Keep the CV sharing settings readable for visitors who are not signed in.

## Indexing policy

Public canonical pages are indexable by default. Filter/search variants are marked `noindex, follow` and point to the unfiltered canonical. The sitemap includes only live, public Wagtail pages and the contact page. Admin paths are disallowed in robots.txt; this is crawler guidance, not access control.

The first project image is used for its social preview. Other pages fall back to the portrait. All structured data reflects existing public profile or project content.

SEO implementation improves clarity and discovery eligibility; it does not guarantee rankings or employer inquiries. Titles and descriptions may be rewritten by search engines.

## References

- [Google title links](https://developers.google.com/search/docs/appearance/title-link)
- [Google snippets](https://developers.google.com/search/docs/appearance/snippet)
- [Canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
