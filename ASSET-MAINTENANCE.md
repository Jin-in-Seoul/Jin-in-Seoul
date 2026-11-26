# Asset maintenance — Jin-in-Seoul

Repository: `Jin-in-Seoul/Jin-in-Seoul` (`main`). Public site: https://jin-in-seoul.com/.

## 1. Purpose

This document defines the management principles for images, audio files, PDF editions, and EPUB editions published on Jin-in-Seoul.com.

Objectives:

- Preservation of the existing repository structure and stable published URLs.
- Control of storage use and page loading performance.
- Prevention of accidental replacement or deletion of published assets.
- Separation of original materials from web-ready files.
- Consistent procedures for future additions.

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

New Gray Note images are stored under `/assets/images/gray-note/`. New photo essays use descriptive subdirectories such as:

```text
assets/images/gray-note/
└── venice-to-athens/
    ├── 01-venice-port.webp
    ├── 02-ferry-deck.webp
    └── 03-mediterranean-sea.webp
```

These filenames are examples, not required names. Existing image paths must remain unchanged.

### 3.2 Image optimization

New photographs are optimized before upload. Proposed defaults:

| Property | Recommended guideline |
| --- | --- |
| Preferred format | WebP |
| Alternative format | JPEG |
| Maximum long edge | 1600 pixels |
| Typical file-size target | 150–300 KB |
| Detailed photographs | Approximately 500 KB when necessary |
| Color profile | sRGB |
| Metadata | Remove unnecessary location and device metadata from web copies |

These are guidelines, not absolute limits. Visual quality review is required, especially for text, architecture and fine detail. Images already smaller than the recommended dimensions are not enlarged.

### 3.3 Historical authenticity and original photographs

Historical travel photographs are records of the time and place in which they were made. Their original appearance is preserved. Preparation for web publication should ordinarily be limited to resizing, compression, format conversion, and necessary technical corrections.

Visual appeal alone does not justify changes to colors, composition or depicted content. Routine optimization excludes removal, replacement or generation of elements in historical photographs. Any substantive visual edit requires the author's explicit decision.

Original files are preserved in personal storage outside GitHub, with separate optimized web copies and an independent backup. Originals are not overwritten during conversion.

The existing `/assets/images/originals/` directory may contain legacy originals; changes require individual file review. Storage standardization alone does not justify deletion or relocation.

### 3.4 Photo essays

Photographs should serve the author's narrative. There is no fixed number of images per essay.

Meaningful filenames and descriptive `alt` attributes are used. Where appropriate, image dimensions are specified and images below the initial viewport are lazy-loaded.

**The author decides photograph selection, count, order, and placement.** Rearrangement of photographs, paragraphs or captions requires approval.

## 4. Audio Management

### 4.1 Storage location

Published audio remains under `/assets/audio/music/` and music pages under `/music/`. Consistency alone does not justify moving published files.

### 4.2 Audio format and naming

MP3 is the existing publication format and remains the default unless a change is approved. Duplicate copies of identical recordings are avoided. Established filename conventions and language suffixes such as `-ja` are preserved.

New files use descriptive lowercase filenames with hyphens.

### 4.3 Audio updates

Before adding or replacing audio:

1. Confirmation of the work, version and language.
2. Verification of playback, duration, start and ending, and obvious sound defects.
3. Verification of the correct audio link on the music page.
4. Verification of the music index and associated navigation.
5. Review of browser caches and direct links when an authorized replacement changes a published recording.

Existing audio files must not be replaced or renamed without approval.

## 5. PDF and EPUB Management

### 5.1 Storage location

Digital editions are stored under `/assets/downloads/`, organized by work and language, with part directories where appropriate.

```text
assets/downloads/
└── a-dictionary-of-galactic-extinction/
    └── part-01/
        ├── en/
        ├── ja/
        └── ko/
```

The download listing remains separately under `/downloads/`.

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

Existing versioned downloads are not silently overwritten.

## 6. File Naming

Preferred naming conventions for newly published media:

- Lowercase Latin letters and digits.
- Hyphens between words.
- Descriptive names identifying the work or scene.
- Language suffixes where appropriate.
- Dates and version numbers for downloadable editions when required by existing conventions.

Examples:

- `01-venice-port.webp`
- `autumn-rain-blue-night-ja.mp3`
- `sweater-en-20260930-ver-001.pdf`

Naming conventions alone do not justify renaming published files.

**Preserving existing URLs takes priority over naming uniformity.**

## 7. Storage and Performance

Assets stored in the repository contribute to repository size and, when published, may contribute to GitHub Pages site size and bandwidth. Repository size and published-site size are different measurements.

Before publishing a photo essay or substantial new media collection:

1. Estimation of the total size of all new files.
2. Confirmation of individual image optimization.
3. **Calculation of the combined size of all images used by the essay**, in addition to individual photograph sizes.
4. Review of likely page-loading impact on mobile connections, including initial images and those loaded later.
5. Review of relevant repository and GitHub Pages storage constraints.
6. Avoidance of redundant copies and incremental uploads where useful.

**No automatic image-count limit or universal per-essay size cap applies.** Total size is a review signal, and the author decides the final composition. Improve compression or loading behavior first if a page is unusually heavy.

Audio and downloadable editions may use more storage than optimized photographs. Storage growth is reviewed periodically.

External hosting is not the default policy. Its adoption requires actual storage, bandwidth or operational needs that justify additional complexity.

## 8. Publication Checklist

Before publishing a new asset:

- [ ] Confirmation of the intended final version and authorized publication.
- [ ] Verification of the designated directory, filename, format, and size.
- [ ] Use of web copies and separate preservation of photographic originals.
- [ ] Review of the **combined image size** and mobile loading behavior for photo essays.
- [ ] Confirmation that no existing file is overwritten unintentionally.
- [ ] Addition or verification of the relevant page reference.
- [ ] Verification of image display, playback, or download on desktop and mobile.
- [ ] Verification of file URLs, image `alt` attributes, and relevant accessibility details.
- [ ] Verification of navigation, search inclusion, and SEO metadata when adding a new page.
- [ ] Updating the publication log when a new work or edition is formally released.

New pages are governed by `SEO-MAINTENANCE.md` and stylesheet changes by `CSS-MAINTENANCE.md`.

An asset-only addition does not automatically require a publication-log entry.

## 9. Preservation and Change Control

The existing published website is the reference state.

The following practices are excluded:

- Moving existing asset directories or renaming published files without approval.
- Replacing originals with compressed derivatives.
- Automatic recompression, restyling or other editing of published media.
- Deletion of apparently unused files without checking all references.
- Modification of literary text or paragraph boundaries during asset maintenance.
- Changes to photo selection or layout without the author's decision.
- Resumption of PDF/EPUB publication without authorization.

Approved changes require prior identification of affected file references, public URLs and cache or indexing consequences, together with confirmation of the latest GitHub `main` and file SHA. Subsequent verification includes retrieval of every changed file and separate confirmation of Pages deployment when feasible.

## 10. Documentation Maintenance

This document is linked from the repository `README.md` alongside `CSS-MAINTENANCE.md` and `SEO-MAINTENANCE.md`.

These guidelines are updated when a new file type, storage method or publication workflow genuinely requires a new policy. Stylistic consistency alone does not justify revision of established policies.

**The author retains final editorial authority. Technical asset policies do not determine the composition of literary works.**
