## Broad migration to React + Astro (branch-only)

The initial pilot's eight routes were extended to the existing v2 content inventory. Running
\`npm run sync\` now derives **both** the event catalog and the source-preserving
React-rendered legacy article pages from the original HTML. The source is authoritative;
do **not** edit \`src/data/legacy-pages.json\` directly.

The source retains the existing 129 HTML documents (128 public routes and ancillary content)
and excludes generated review/comparison snapshots. A build-time path audit fails when pages
disappear or duplicate. The 8 custom React routes take precedence; the other existing
route types are rendered with a React server component in Astro's catch-all static route.
The original body fragments, factual statements, attribution and links are retained.
Internal navigation is remapped to the pilot's routes and original media are referenced from
the published v2 site. The original site remains unchanged, and no deployment happens from CI.

**Hybrid migration warning:** The remaining routes are React SSR wrappers around the
existing source markup rather than bespoke rewrites into JSX components. Original v2 JS
is provided for legacy interactions on migrated pages; critical user flows still require
browser verification, especially notebook/haiku, document downloads, keyboard accessibility
and mobile focus. The conversion is a useful complete-content, shared-shell milestone,
**not** evidence of full functional parity or readiness to replace the root.

Browser comparison: \`.github/workflows/react-astryx-visual.yml\` captures the original v2
and React outputs in Chromium at desktop (1440px), mobile (390px) and narrow (320px), with
basic interaction checks and a JSON report uploaded as an artifact. Review screenshots and
identified issues before a release.
