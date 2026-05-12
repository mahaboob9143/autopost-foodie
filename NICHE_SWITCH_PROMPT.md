# 🔄 Niche Switch Prompt & Guide

Use this guide whenever you want to pivot this bot to a new Instagram niche, source account, or publishing profile.

---

## 🤖 The "One-Shot" Prompt
Copy and paste this into your AI assistant (e.g., Antigravity) at the start of a conversation to perform the switch automatically:

```text
Hey! I want to switch the niche of my InstaAgent bot.

**Project location:** p:\Projects\InstaAgent+YT Foodie  
**New source account:** [URL_OR_USERNAME]
**New publishing account:** [ACCOUNT_NAME_FROM_META_DUMP]

Please perform the following steps:
1. Update 'source_accounts' and 'fallback_templates' in config.yaml.
2. Update YouTube 'category_id' (e.g., 19 for Travel, 24 for Entertainment) and 'tags' in config.yaml.
3. Completely rewrite 'core/caption_engine.py' keyword banks, hooks, and hashtags for the new niche.
4. Update SHEET_CSV_URL in 'core/sheets_reader.py' to point to the new Google Sheet.
5. Update CLOUDINARY_FOLDER in .env to [account_name]/reposts.
6. Update README.md and REPOST_AGENT docstrings with new niche details.
7. Clear 'data/tracker.xlsx' to reset the deduplication history.

After local updates, help me test with 'python main.py --repost' and then push to a new GitHub repo.
```

---

## 📋 Niche Switch Checklist

| File | Changes Required |
|---|---|
| **`config.yaml`** | `source_accounts`, YT `category_id`, `tags`, `fallback_templates`. |
| **`core/caption_engine.py`** | Key scoring categories, `_HOOKS`, `_PRE_HOOKS`, `_HASHTAGS`. |
| **`core/sheets_reader.py`** | `SHEET_CSV_URL` (Export link from Google Sheets). |
| **`.env`** | `IG_ACCOUNT_ID`, `FB_PAGE_ID`, `FB_PAGE_ACCESS_TOKEN`, `CLOUDINARY_FOLDER`. |
| **`README.md`** | Update niche description and source account link. |
| **`data/tracker.xlsx`** | Delete all rows (except header) to start fresh. |

---

## 🛠️ Essential Tools

### 1. Secrets Migration
To quickly set up your new GitHub repository with all your local secrets:
```bash
python tools/migrate_secrets.py [your-github-username]/[repo-name]
```
*(Requires GitHub CLI installed and authenticated)*

### 2. YouTube Authentication
If you are moving to a **new YouTube channel**, you must generate a new refresh token:
1. Ensure your OAuth2 Desktop Client credentials are in `.env`.
2. Run: `python tools/yt_auth.py`
3. Paste the generated token into `.env` and GitHub Secrets.

---

## ⚠️ Important Constraints
- **Caption Limit**: The code automatically truncates captions at 2,100 characters to prevent Meta API errors. Do not remove this logic from `core/caption_engine.py`.
- **Cloudinary Folders**: Always use the `CLOUDINARY_FOLDER` env var to keep different niches separated in your Cloudinary media library.
- **Deduplication**: The bot uses `data/tracker.xlsx`. If you don't clear this when switching niches, it might skip content that has a similar ID to old niche posts.
