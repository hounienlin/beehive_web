# beehive_web: 拼字蜂巢 BeeHive Spell website

Static marketing and support site for the iOS app **拼字蜂巢 BeeHive Spell**, hosted on GitHub Pages.

Pure HTML + one CSS file (`assets/css/style.css`). No JavaScript, no trackers, no analytics, no external fonts or CDNs.
The site itself loads nothing from a third party, which matches the app's kids-privacy promise. Keep it that way.

## Pages

| Page | 繁體中文 | English |
| --- | --- | --- |
| Landing | `/` (`index.html`) | `/en/` (`en/index.html`) |
| Free vs Pro | `/pro.html` | `/en/pro.html` |
| Support (App Store Connect "Support URL") | `/support.html` | `/en/support.html` |
| Privacy Policy (App Store Connect "Privacy Policy URL") | `/privacy.html` | `/en/privacy.html` |
| Not found | `404.html` (absolute `/beehive_web/...` paths, because GitHub Pages serves it at any depth) | |

GitHub Pages also answers the extensionless form (`/privacy` serves `privacy.html`), but use the `.html` URLs everywhere
(App Store Connect, the app's Parent Area links) so they also work on any other static host.

Final URLs after publishing:

- https://hounienlin.github.io/beehive_web/
- https://hounienlin.github.io/beehive_web/pro.html
- https://hounienlin.github.io/beehive_web/support.html
- https://hounienlin.github.io/beehive_web/privacy.html
- https://hounienlin.github.io/beehive_web/en/
- https://hounienlin.github.io/beehive_web/en/pro.html
- https://hounienlin.github.io/beehive_web/en/support.html
- https://hounienlin.github.io/beehive_web/en/privacy.html

## Publish (GitHub Pages)

1. On GitHub, create a **public** repository `hounienlin/beehive_web` (no README, no .gitignore, so the first push is clean).
2. From this folder:
   ```sh
   git remote add origin git@github.com:hounienlin/beehive_web.git   # or the https URL
   git branch -M main
   git push -u origin main
   ```
3. Repository > **Settings > Pages** > Build and deployment: Source **Deploy from a branch**, Branch **main**, folder **/ (root)**, Save.
4. Wait 1–3 minutes, then open the URLs above in a **private window (not signed in to GitHub)** and check every page.
5. App Store Connect:
   - App Information > Privacy Policy URL: zh-Hant `.../beehive_web/privacy.html`, English (U.S.) `.../beehive_web/en/privacy.html`
   - Version page > Support URL: zh-Hant `.../beehive_web/support.html`, English `.../beehive_web/en/support.html`
   - Marketing URL (optional): `.../beehive_web/` and `.../beehive_web/en/`
   - The app's Parent Area privacy link should open the page for the current app language.

`.nojekyll` is present so GitHub serves files as-is (no Jekyll build). `robots.txt` allows everything; note that crawlers
only read `robots.txt` at the domain root, so on a project site it is informational.

## Update screenshots, mascot art and icon

The images are copied and downscaled from the app repo (it is only read, never written):

```sh
python3 tools/sync_assets.py ../beehive                    # screenshots (600 px WebP), mascots (360 px WebP), icons
python3 tools/sync_assets.py ../beehive --icon icon-A2.png # use a different icon from docs/appstore/icon/
```

Sources: `docs/appstore/final/<zh-Hant|en-US>/iphone-6.9/*.png`, `ios/BeeHive/Resources/Assets.xcassets/Mascot/*/*@3x.png`,
`docs/appstore/icon/<icon>.png`. Needs Pillow. If the screenshot file names or order change, update the `<ul class="shots">`
lists and alt text in `index.html` and `en/index.html`.

## Check before every push

```sh
python3 tools/check_site.py          # internal links + #anchors, no third-party loads, banned words, only the approved email
python3 -m http.server 8000          # then open http://localhost:8000/
```

`404.html` uses `/beehive_web/...` paths, so it only looks right on GitHub Pages (or when served from a parent folder).

## Copy rules (from the app repo's docs/appstore/marketing-terms.md)

- The 7-letter game is **蜂巢挑戰 / Hive Challenge**. Never call anything "Spelling Bee".
- No contest, organizer, newspaper, publisher or exam brand names; no "official", 官方, 題庫, "official list".
- Grade-Level Contest Word Packs: list the published packs (K–2, 3–5, 6–8, 9–12); never claim complete grade coverage.
- No learning-outcome guarantees, superlatives, "AI", or pushy purchase words. No price until it is decided.
- Only claim what the shipped build does (no iCloud sync, no Family Sharing until decided).
- English mascot name: **Mimi** (matches the app's English UI; still a working name, see TODO.md).
