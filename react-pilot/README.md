# React 19 + Astro + Meta Astryx migration pilot

This is a **non-destructive, opt-in migration** of the 2028 Ehime culture festival design PoC. It does not replace any existing v1/v2 route. The original Pages site remains published at the root.

## Included

- React home-page experience at the pilot root
- React event search with keyword, city, genre and verified/sample filters
- Six statically generated React event detail pages (one original verified event and five clearly labelled fictitious examples)
- Shared accessible Astro header and footer; Meta Astryx v0.7.11 Stone theme and real Astryx Button component
- Original festival imagery referenced from the published v2 site without copying or relicensing the assets
- Automatic event synchronization from original v2 data, with build-time guards

## Run

Requires Node.js 22+ and internet access for dependency installation.

    cd react-pilot
    npm install
    npm run test
    npm run check
    npm run build
    npm run dev

Visit the local URL printed by Astro. Production build is set to /ehime-kokubunsai-hp-poc/react-pilot/, for eventual isolated GitHub Pages publication.

The event JSON is generated (and git-ignored). Do not edit it. Adjust the source of truth, design-lab/experience-data.js, then rerun npm run sync. If the existing source changes in an unexpected way, the build stops instead of silently fabricating data.

## Review and publishing

The CI workflow builds this directory and uploads the static dist artifact. It **does not deploy the pilot**, change GitHub Pages settings, change the root site, merge a PR, or modify v1-frozen. An explicit deployment decision is required to make the trial version public.

Some navigation links intentionally return to the current site while only the first three page archetypes have been migrated. Additional functionality including cultural notebook and literary interactions stays on v2 until separately migrated and tested.

Items remaining before replacing v2: full page inventory and URL parity, preservation audit, keyboard/screen-reader tests, 200% zoom, responsive device checks, performance and legal/asset review. Astryx is beta; dependency version is pinned.
