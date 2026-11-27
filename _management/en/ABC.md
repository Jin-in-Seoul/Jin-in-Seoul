# ABC — Jin-in-Seoul Site Operation and Maintenance Regulations

## 1. Purpose

These regulations aim to preserve the literary identity of Jin-in-Seoul, ensure the stable publication and preservation of works, maintain consistency in site operation, and secure technical stability.

## 2. Site Identity

Jin-in-Seoul is a personal literary website presenting novels, short stories, children's books, essays, haiku, music and tales from premodern Korea.

English-speaking readers are given priority. The usual multilingual display order is English · 日本語 · Français · 한국어. Existing conventions for individual collections, including haiku and music, follow their respective detailed regulations and editorial principles.

Jin-in-Seoul is the pen name used for the creation and publication of works. Public author information follows the approved pen name.

## 3. Operating Environment

- Official site: https://jin-in-seoul.com/
- Repository: Jin-in-Seoul/Jin-in-Seoul
- Production branch: main
- Publishing environment: GitHub Pages / Jekyll

Existing work URLs and publication structures are maintained on a continuing basis.

## 4. Management Regulations

These regulations establish the fundamental principles of site operation. Understanding the management system begins with this document and README. The following documents govern the individual areas.

| Document | Scope |
| --- | --- |
| [README.md](README.md) | Management system and document index |
| [CSS-MAINTENANCE.md](CSS-MAINTENANCE.md) | Design and CSS |
| [SEO-MAINTENANCE.md](SEO-MAINTENANCE.md) | Search engine optimisation and audits |
| [PUBLICATION-LOG-POLICY.md](PUBLICATION-LOG-POLICY.md) | Publication records |
| [ASSET-MAINTENANCE.md](ASSET-MAINTENANCE.md) | Digital assets |
| [PREMODERN-KOREAN-FICTION-TRANSLATION-GUIDE.md](PREMODERN-KOREAN-FICTION-TRANSLATION-GUIDE.md) | Shared translation principles and glossary for premodern Korean fiction |
| [JEON-UNCHI-TRANSLATION-GUIDE.md](JEON-UNCHI-TRANSLATION-GUIDE.md) | Work-specific translation guide for The Tale of Jeon Unchi |
| [MASTER-RABBIT-TRANSLATION-GUIDE.md](MASTER-RABBIT-TRANSLATION-GUIDE.md) | Work-specific translation guide for The Tale of Master Rabbit |

Both these regulations and the relevant detailed regulations apply to site management. Historical work records are distinguished from the current operating state, which is determined by the actual latest files on main. Conflicts between regulations require clarification and approval before changes are made.

## 5. Preservation and Editing of Works

Literary texts, titles, translations, paragraph structures and distinctive typography are respected and preserved as the results of creative and editorial work.

Literary and editorial changes are subject to the author's decisions. Technical maintenance is distinguished from literary editing. Existing content or publication formats are not changed merely to improve management efficiency.

Foreign-language translations follow the approved Korean source text. For premodern Korean fiction, the established modern Korean edition, its source edition and the applicable translation regulations are followed.

## 6. Design and Reader Experience

The site seeks simple and consistent literary typography.

Menus, links, buttons and other visual elements are used only when they have a clear function and are necessary.

Multilingual publication aims to provide works to readers in their own languages. Language selection is centred on work listings; additional language-switching functions within reading pages require separate approval.

Established typography and design appropriate to each work are maintained. In particular, the diary typography of Sweater and its related CSS are protected under the CSS maintenance regulations.

## 7. Technical Maintenance

Technical maintenance aims to improve the stability of the existing publishing system, accuracy of work and management efficiency.

New management functions are arranged independently of existing HTML, CSS and publication structures wherever possible. Work scope is established in advance, and changes outside the approved scope require separate review and approval. Requests for review or opinions are distinguished from approval to make changes.

## 8. Management Tools

Management tools are stored separately in the _maintenance/ directory.

| Tool | Function |
| --- | --- |
| [plan_release.py](../../_maintenance/plan_release.py) | Generate new publication plans and proposed changes by collection |
| [plan_gray_note_release.py](../../_maintenance/plan_gray_note_release.py) | Generate new Gray Note publication plans |
| [check_change_scope.py](../../_maintenance/check_change_scope.py) | Verify the scope of changes |
| [report_site_status.py](../../_maintenance/report_site_status.py) | Check deployment and technical audit status |

Publication planning tools output proposed changes for review; they do not directly modify existing files or publish works. The shared tool was written to support new publication plans for A Dictionary of Galactic Extinction, Scarecrow Distance, Sweater, short stories, children's books, Tales from Premodern Korea, Gray Note, Haiku and Music. Adding translations of existing works, uploading assets and special publication formats require separate review.

As of 26 November 2026, the management tools had been registered and their sources retrieved for verification, but execution tests had not been completed. Unverified functions are not used for actual publication. The execution requirements and input formats of each tool follow the descriptions in its source.

Management tools and the public site are functionally separate. Introducing or changing tools must not affect existing works or the reader experience.

## 9. Publication of Works

New works and translations require the following checks as applicable:

- Work text and title
- Work listings and relevant homepage entries
- Sitemap and internal search index
- Canonical and hreflang
- Search and sharing metadata
- JSON-LD structured data
- Publication Log

Publication records and search information reflect works and language editions actually published. Publication dates, language order and preservation of existing records follow the Publication Log policy.

Decisions concerning digital assets, including the suspension of PDF and EPUB publication, follow the asset maintenance regulations.

## 10. Change Control and Verification

All changes are based on the latest production branch. Before a change, the baseline commit and latest state of the target files are checked; changed files are retrieved afterwards.

The complete file state before and after the change is compared to verify compliance with the approved scope. GitHub source changes, automated audits, GitHub Pages deployment and the public site's condition are treated as separate verification items.

Audit success and the actual number of errors are distinguished. Unverified matters are not recorded as verified.

## 11. Recovery and History Preservation

When technical errors occur, their scope and cause are identified and the previous working state is restored to the extent necessary.

Unrelated work and existing publication records are preserved during recovery. Change and recovery history remains traceable through Git commits, and recovery results are verified against the baseline state.

## 12. Maintenance and Revision of Regulations

These regulations and the detailed regulations for individual areas may be revised according to the site's operating environment and publishing system.

Revisions require the author's approval and maintain consistency with existing regulations.
