# Asset maintenance — Jin-in-Seoul

Repository: `Jin-in-Seoul/Jin-in-Seoul` (`main`). Public site: https://jin-in-seoul.com/.

## 1. Purpose

This document defines the management principles for images, audio files, PDF editions, and EPUB editions published on Jin-in-Seoul.com.

Objectives:

- Preserve the existing repository structure and stable published URLs.
- Control storage use and page loading performance.
- Prevent accidental replacement or deletion of published assets.
- Keep original materials separate from web-ready files.
- Establish consistent procedures for future additions.

**Existing published assets must not be reorganized or modified solely for consistency.** Changes to published assets require a specific reason and the author's authorization.

This is a technical management document. The author determines which photographs appear in an essay, how many are used, and where they are placed. Technical guidelines do not override literary or editorial decisions.

## 2. Current Repository Structure

Current asset locations:

```text
assets/
├── images/
│   ├── gray-note/
│   │   ├── 003-black-hole-four-views.webp
│   │   └── 2026-10-01-spring-to-summer-seoul/
│   ├── footer/
│   ├── originals/
│   └── [shared site images]
├── audio/
│   └── music/
│       └── [published MP3 files]
└── downloads/
    ├── a-dictionary-of-galactic-extinction/
    ├── sweater/
    └── adjunct-lecturer-k-007-briefcase/
```

Published pages are maintained separately from media:

- `gray-note/002/` — photo essay page; `assets/images/gray-note/` — its images.
- `music/` — music pages; `assets/audio/music/` — MP3 recordings.
- `downloads/` — digital-edition listing; `assets/downloads/` — PDF and EPUB files.

This separation is intentional and must be preserved.

## 3. Image Management

### 3.1 Storage location

Store new Gray Note images under `/assets/images/gray-note/`. For a new photo essay, use a descriptive subdirectory such as:

```text
assets/images/gray-note/
└── venice-to-athens/
    ├── 01-venice-port.webp
    ├── 02-ferry-deck.webp
    └── 03-mediterranean-sea.webp
```

These filenames are examples, not required names. Existing image paths must remain unchanged.

### 3.2 Image optimization

Optimize new photographs before upload. Proposed defaults:

| Property | Recommended guideline |
| --- | --- |
| Preferred format | WebP |
| Alternative format | JPEG |
| Maximum long edge | 1600 pixels |
| Typical file-size target | 150–300 KB |
| Detailed photographs | Approximately 500 KB when necessary |
| Color profile | sRGB |
| Metadata | Remove unnecessary location and device metadata from web copies |

These are guidelines, not absolute limits. Inspect quality visually, especially for text, architecture, and fine detail. Do not enlarge images already smaller than the recommended dimensions.

### 3.3 Historical authenticity and original photographs

Historical travel photographs are records of the time and place in which they were made. Preserve their original appearance. Preparation for web publication should ordinarily be limited to resizing, compression, format conversion, and necessary technical corrections.

Do not alter colors, composition, or depicted content merely to make the photograph more visually appealing. Do not remove, replace, or generate elements of historical photographs as routine optimization. Any substantive visual edit requires the author's explicit decision.

Preserve original files in personal storage outside GitHub, and create separate optimized web copies. Never overwrite originals during conversion. Keep an independent backup of original photographs.

The existing `/assets/images/originals/` directory may contain legacy originals; review individual files before any change. Do not delete or relocate them merely to standardize storage.

### 3.4 Photo essays

Photographs should serve the author's narrative. There is no fixed number of images per essay.

Use meaningful filenames and descriptive `alt` attributes. Where appropriate, specify image dimensions and lazy-load images below the initial viewport.

**The author decides photograph selection, count, order, and placement.** Do not rearrange photographs, paragraphs, or captions without approval.

## 4. Audio Management

### 4.1 Storage location

Keep published audio under `/assets/audio/music/` and music pages under `/music/`. Do not move published files solely for consistency.

### 4.2 Audio format and naming

MP3 is the existing publication format and remains the default unless a change is approved. Avoid duplicate copies of identical recordings. Preserve established filename conventions and language suffixes such as `-ja`.

For new files, use descriptive lowercase filenames with hyphens.

### 4.3 Audio updates

Before adding or replacing audio:

1. Confirm the work, version, and language.
2. Check playback, duration, start and ending, and obvious sound defects.
3. Verify that the correct audio file is linked from the music page.
4. Check the music index and associated navigation.
5. Consider browser caches and direct links if an authorized replacement changes a published recording.

Existing audio files must not be replaced or renamed without approval.

## 5. PDF and EPUB Management

### 5.1 Storage location

Keep digital editions under `/assets/downloads/`, organized by work and language, with part directories where appropriate.

```text
assets/downloads/
└── a-dictionary-of-galactic-extinction/
    └── part-01/
        ├── en/
        ├── ja/
        └── ko/
```

Keep the download listing separately under `/downloads/`.

### 5.2 Publication suspension

**The publication notice dated November 2, 2026 remains in effect.**

Uploads and updates of downloadable PDF and EPUB editions are suspended until a reliable production and verification process is established. Existing errors in those editions are not to be corrected during this suspension.

The most current literary texts are available in the site's HTML pages.

### 5.3 If publication resumes

A newly authorized release should be verified for:

- Complete text, correct chapter order, and paragraph formatting.
- Language-specific fonts, typography, and rendering.
- Table of contents and internal navigation.
- File opening on representative readers.
- Filename, version, and download-link accuracy.

Do not silently overwrite existing versioned downloads.

## 6. File Naming

For newly published media, prefer:

- Lowercase Latin letters and digits.
- Hyphens between words.
- Descriptive names identifying the work or scene.
- Language suffixes where appropriate.
- Dates and version numbers for downloadable editions when required by existing conventions.

Examples:

- `01-venice-port.webp`
- `autumn-rain-blue-night-ja.mp3`
- `sweater-en-20260930-ver-001.pdf`

Do not rename published files merely to enforce these conventions.

**Preserving existing URLs takes priority over naming uniformity.**

## 7. Storage and Performance

Assets stored in the repository contribute to repository size and, when published, may contribute to GitHub Pages site size and bandwidth. Repository size and published-site size are different measurements.

Before publishing a photo essay or substantial new media collection:

1. Estimate the total size of all new files.
2. Confirm that individual images have been optimized.
3. **Calculate the combined size of all images used by the essay**, not only the size of each photograph.
4. Review the likely page-loading impact on mobile connections, including the initial images and images loaded later.
5. Check relevant repository and GitHub Pages storage constraints.
6. Avoid redundant copies and upload additions incrementally when useful.

**Do not impose an automatic image-count limit or a universal per-essay size cap.** Total size is a review signal, and the author decides the final composition. Improve compression or loading behavior first if a page is unusually heavy.

Audio and downloadable editions may use more storage than optimized photographs. Review storage growth periodically.

External hosting is not the default policy. Consider it only when actual storage, bandwidth, or operational requirements justify additional complexity.

## 8. Publication Checklist

Before publishing a new asset:

- [ ] Confirm the intended final version and authorized publication.
- [ ] Verify the designated directory, filename, format, and size.
- [ ] For photographs, use a web copy and preserve the original separately.
- [ ] For photo essays, review the **combined image size** and mobile loading behavior.
- [ ] Confirm that no existing file is overwritten unintentionally.
- [ ] Add or verify the relevant page reference.
- [ ] Check image display, playback, or download on desktop and mobile.
- [ ] Verify file URLs, image `alt` attributes, and relevant accessibility details.
- [ ] Check navigation, search inclusion, and SEO metadata when adding a new page.
- [ ] Update the publication log when a new work or edition is formally released.

Follow `SEO-MAINTENANCE.md` for new pages and `CSS-MAINTENANCE.md` for stylesheet changes.

An asset-only addition does not automatically require a publication-log entry.

## 9. Preservation and Change Control

The existing published website is the reference state.

Do not:

- Move existing asset directories or rename published files without approval.
- Replace originals with compressed derivatives.
- Recompress, restyle, or otherwise edit published media automatically.
- Delete apparently unused files without checking all references.
- Modify literary text or paragraph boundaries during asset maintenance.
- Change photo selection or layout without the author's decision.
- Resume PDF/EPUB publication without authorization.

Before an approved change, identify affected file references, public URLs, and cache or indexing consequences. Fetch the latest GitHub `main` and file SHA before writing. Re-fetch every changed file afterward and check Pages deployment separately when feasible.

## 10. Documentation Maintenance

Link this document from the repository `README.md` alongside `CSS-MAINTENANCE.md` and `SEO-MAINTENANCE.md`.

Update these guidelines when a new file type, storage method, or publication workflow genuinely requires a new policy. Do not revise established policies merely for stylistic consistency.

**The author retains final editorial authority. Technical asset policies do not determine the composition of literary works.**
