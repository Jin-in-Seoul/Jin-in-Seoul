# Jin-in-Seoul

## A Dictionary of Galactic Extinction

*A Dictionary of Galactic Extinction* began with two images.

One came from *Men in Black*: a tiny galaxy contained inside a bead hanging from a cat’s collar. The other came much later, from a simple question: what would happen if a candle burned inside a perfectly mirrored room and its light could never escape?

Those two images gradually became questions about light, energy, civilization, and extinction. What interested me was not a story in which evil destroys civilization, but a more difficult problem: what happens when rational and well-intentioned people keep solving problems, and the accumulated consequences of those solutions eventually become catastrophic?

The form of the novel grew from the same concern. Rather than tell the history of a vast civilization through a single protagonist and a single plot, I wanted the world to emerge through fragments of physics, history, people, words, records, and different kinds of documents.

At first, I wanted to write a story about placing a galaxy inside a small object. In the end, it became something entirely different. I wanted to place human goodwill, desire, fear, language, and reason inside a galaxy, and see where they would lead if allowed to operate to their logical end.

## Serial Publication

*A Dictionary of Galactic Extinction* is currently being published online in serialized form in **English and French**.

[Read the archive](https://jin-in-seoul.com)

## Shared site chrome

The site-wide header and footer are maintained as Jekyll includes:

- `_includes/header.html`
- `_includes/footer.html`

Reader-facing HTML pages use `{% include header.html %}` and `{% include footer.html %}`.
GitHub Pages expands these includes when the site is published, so future site-wide header/footer changes require editing only the corresponding include file.

## Shared navigation (v046)
- `_includes/header.html` is the single site-wide home/publication/download header.
- `_includes/footer.html` is the single site-wide footer.
- Reader/body pages use one localized Contents link only: `Contents`, `Sommaire`, `目次`, or `목차`.
- Redundant page-local Home, language/month navigation, and Sweater previous/next chapter navigation were removed.



## 049
- Added public Translation Principles pages for A Dictionary of Galactic Extinction in English, Japanese, and French.
- Added homepage links beneath Short Stories.
- Added the three pages to sitemap.xml.


## Download tracking
Free Digital Editions links emit the GA4 event `digital_edition_download` with work, part, language, format, version, file name, and URL metadata. GA4 Enhanced Measurement may also record its standard `file_download` event.


## 053
- Added English A Dictionary of Galactic Extinction, Part II, Chapters 7–9.
- Activated the new chapter links in the English contents page.
- Updated sitemap.xml and Publication Log for September 30, 2026.

## 055 — 회색노트 self-publishing
- Added `/gray-note/` as a Jekyll-managed essay/notes section.
- New posts are created by adding one Markdown file to `_posts/`; the list page updates automatically in reverse chronological order.
- Post URLs are generated automatically as `/gray-note/YYYY/MM/DD/slug/`.
- `sitemap.xml` now automatically includes future Gray Note posts.
- Gray Note posts use `_layouts/gray-note-post.html`, the shared site header/footer, GA4, and the site's Korean serif typography.

### How to publish a new 회색노트 post without rebuilding the site
In GitHub, create a new file inside `_posts/` with a filename like:

`2026-09-30-my-note.md`

Paste this at the top:

```yaml
---
layout: gray-note-post
title: "글 제목"
date: 2026-09-30
---
```

Then write the body below the closing `---` in ordinary Markdown and commit the file.
The `/gray-note/` index and sitemap update automatically when GitHub Pages rebuilds the site.
