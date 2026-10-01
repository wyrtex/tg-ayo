# tg-ayo

Telegram-iOS fork-by-patches with AyuGram-style features.

The repo stores only patches (`patches/*.patch`) and a pinned upstream commit
(`UPSTREAM_COMMIT`). GitHub Actions fetches upstream, applies the patches and
builds an unsigned IPA (Actions → Build IPA → Artifacts). Sign it with ESign.

Secrets required: `TG_API_ID`, `TG_API_HASH`.

## Features
- [x] Ghost mode (no read receipts, no typing, no online) — Settings → Ayo настройки
- [ ] Keep deleted messages
- [ ] Save self-destructing media
- [ ] Bypass forward/save restrictions
- [ ] UI customization
