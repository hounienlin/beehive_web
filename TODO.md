# TODO before / after launch

Search the HTML for `TODO` to find each spot.

## Filled (done)

- Developer name: `Hounien Lin` (footers, privacy policy).
- Contact email: `hounienlin@gmail.com` (support, privacy, pro pages). This is the only email allowed on the site;
  `tools/check_site.py` fails on any other address.

## Must do

- [ ] **App Store link and badge** (`index.html`, `en/index.html`, hero button `href="#"`): after the app is live, set
      `https://apps.apple.com/app/id<APP_ID>` and swap the "即將上架 / Coming soon" button for the "Download on the App Store"
      badge downloaded from Apple's marketing resources into `assets/img/` (do not hot-link it from Apple's servers).
- [ ] **Screenshots**: the current set is from 2026-10-28; a new set is being generated. When it lands, run
      `python3 tools/sync_assets.py ../beehive` and re-check the alt text in both landing pages.
- [ ] **App icon**: favicon / apple-touch-icon / og image use `icon-C2.png` for now. Re-run sync with `--icon <file>` when final.

## Waiting for a product decision (do not publish a promise before it is decided)

- [ ] **Pro price** (`pro.html`, `en/pro.html`, comment in the "Cost" row): no amount anywhere until set.
- [ ] **Family Sharing** (`support.html`, `en/support.html`, `pro.html`, `en/pro.html`, comments): `Products.storekit` has
      `familyShareable = false`; the PRD says on. If it is turned on, add the prepared FAQ text from the comment.
- [ ] **Grade-Level Contest Word Packs pricing** (comment in `pro.html` / `en/pro.html`): free, included in Pro, or sold
      separately is undecided. The site only describes the packs.
- [ ] **Practice after 300 words**: the site follows release-readiness 8.1 ("every practice start shows the Pro screen").
      An in-app string still says learned words can be reviewed. If the rule changes, update `pro.html` section 03,
      `support.html` section 04 and the English pages.
- [ ] **English mascot name "Mimi"**: still a working name. If it changes, replace `Mimi` in `en/*.html` and the 404 alt text.
- [ ] **iCloud sync**: if it ships, update "progress stays on this device" in privacy, support, pro and landing pages,
      and update the privacy policy date first.
