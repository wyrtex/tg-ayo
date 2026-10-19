# tg-ayo

Telegram-iOS fork-by-patches with AyuGram-style features.

The repo stores only patches (`patches/*.patch`) and a pinned upstream commit
(`UPSTREAM_COMMIT`). GitHub Actions fetches upstream, applies the patches and
builds an unsigned IPA (Actions → Build IPA → Artifacts). Sign it with ESign.

The app is branded as **AyoGram** (`branding/`: name, ghost icon) and uses its own
bundle id `org.ayogram.ios`, so it installs next to the official Telegram.
Sideloaded builds lose the app group entitlement; patch 0002 makes the app keep
its data in its own container instead of hanging on a black screen.

Secrets required: `TG_API_ID`, `TG_API_HASH`.

## Features
All toggles: Settings → Ayo настройки.
- [x] Ghost mode (no read receipts, no typing, no online)
- [x] Keep deleted messages (marked 🗑 in the time label)
- [x] Edit history (message context menu → «История правок»)
- [x] Bypass copy protection (copy / save in protected chats)
- [x] Allow screenshots, no screenshot notifications
- [x] Unlimited accounts
- [ ] Forward from protected chats (server rejects plain forwards; needs re-upload)
- [ ] Save self-destructing media
- [ ] UI customization
