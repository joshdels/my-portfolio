# SEO and Publishing

The site provides page-specific titles and descriptions, canonical URLs, Open Graph and Twitter previews, Person/WebSite/page structured data, `/sitemap.xml`, and `/robots.txt`.

## Before going live

1. Set the Wagtail Site hostname to the public domain and port to `443` for HTTPS. Avoid a localhost or internal hostname in production.
2. Confirm the homepage is the site root and publish the project index and project pages.
3. In Wagtail’s Promote tab, write an accurate SEO title and search description for each important page. Defaults use Joshua De Leon’s name and CAD-to-GIS, parcel mapping, and masterplan WebGIS focus; project descriptions supply project fallbacks.
4. Visit `/sitemap.xml` and inspect a page’s canonical URL. Both should use the public HTTPS domain.
5. Verify the domain in Google Search Console and submit the sitemap. Inspect the homepage and a project URL for indexing eligibility.
6. Check link previews, keyboard navigation, and mobile layouts. Measure deployed pages with PageSpeed Insights and monitor Search Console as field data becomes available.

## Project content freelance clients can assess

Lead with a clear problem and your contribution. Use the existing content field for sections covering source drawings or records, your role, coordinate and attribute checks, technical decisions, deliverables, outcome, and client handover. Add source-code or demo links using project links; these appear near the summary.

Describe the relevant sector and technologies naturally. Lead with CAD-to-GIS, land parcels, parcel and tax mapping, or masterplan drawings to interactive WebGIS only where the project supports that focus. Utility layers are a supporting topic where relevant. Do not relabel unrelated past projects as niche experience. Use measured results only when supported by evidence. Explain screenshots with captions and keep private client information out of public examples.

Use LinkedIn, GitHub, and your CV to link consistently to your portfolio and relevant case studies. Keep the CV sharing settings readable for visitors who are not signed in.

## Indexing policy

Public canonical pages are indexable by default. Filter/search variants are marked `noindex, follow` and point to the unfiltered canonical. The sitemap includes only live, public Wagtail pages and the contact page. Admin paths are disallowed in robots.txt; this is crawler guidance, not access control.

The first project image is used for its social preview. Other pages fall back to the portrait. All structured data reflects existing public profile or project content.

SEO implementation improves clarity and discovery eligibility; it does not guarantee rankings or client inquiries. Titles and descriptions may be rewritten by search engines.

## References

- [Google title links](https://developers.google.com/search/docs/appearance/title-link)
- [Google snippets](https://developers.google.com/search/docs/appearance/snippet)
- [Canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)

## Niche rollout

Homepage, contact, and project-index fallback copy emphasize freelance CAD-to-GIS conversion, parcel and tax mapping, and masterplan WebGIS handover. Existing CMS titles, descriptions, project narratives, and index intros retain editorial precedence: review them in Wagtail to remove outdated positioning without inventing project evidence.

Suggested homepage SEO title: `CAD-to-GIS & Masterplan WebGIS | Joshdels`. Describe actual inputs and deliverables in each project rather than repeating every service keyword. Parcel mapping does not imply surveying certification, valuation, or tax advice.

`/services/` is a coming-soon placeholder with a contact link. It uses `noindex, follow` and is intentionally absent from the sitemap. At launch, publish substantive service scope and verified evidence, remove its noindex policy in `portfolio_tags.py`, and add the route to the static sitemap. Do not add ratings, pricing, or service availability claims before they exist.

The standalone 500 page returns HTTP 500 and noindex metadata without structured data. It is an error handler, not a public service landing page. See [Google's HTTP status guidance](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes).

## Audience fit and measurement

The indexable homepage explains who the work is for, source materials, scoped outputs, and handover expectations. The services placeholder remains noindex until launch; it is not the organic-search landing page for this phase.

| Intended audience | Problem to describe | Evidence to publish when available |
| --- | --- | --- |
| Planning and engineering consultants | CAD-to-GIS conversion and drawing layer cleanup | Before/after layers, coordinate checks, delivered file structure |
| Property developers and land-record teams | Parcel boundaries linked to identifiers and tax records | Anonymized parcel joins, documented gaps, review workflow |
| Masterplan and planning teams | Drawings made accessible as interactive browser maps | Working map demo, feature inspection, handover documentation |

These are audience and search-intent hypotheses, not measured keyword demand or claims of past clients. No geographic service area, file compatibility guarantee, or client result should be added without confirmation.

After deployment, use Search Console to compare impressions, clicks, queries, and landing pages for CAD-to-GIS, parcel/tax mapping, and masterplan WebGIS searches. Review whether incoming inquiries describe those actual needs. Check CMS SEO overrides and published case studies if the site still attracts broad job-seeking or unrelated GIS queries. Rankings and audience reach have not been verified by this source-code review.

This approach follows [Google's people-first content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content): write for a defined audience and provide useful information about the work.
