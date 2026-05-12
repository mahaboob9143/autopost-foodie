# 🔄 Niche Switch Prompt (Reusable)

Use this prompt whenever you want to switch this bot to a new Instagram niche and source account.
Copy and paste it to your AI assistant (Antigravity / Claude / etc.) at the start of a conversation.

---

## Prompt Template

```
Hey! I want to switch the niche of my InstaAgent repost bot to a new one.

**Project location:** p:\Projects\InstaAgent+YT Foodie  
**Current source account scraping from:** [CURRENT_SOURCE_ACCOUNT]  
**New source account to scrape from:** [NEW_SOURCE_ACCOUNT_URL]

Here's what I need:
1. Change the source account in `config.yaml` → `repost.source_accounts`
2. Update YouTube category ID and tags in `config.yaml` to match the new niche
3. Update the caption engine categories, hooks, pre-hooks, and hashtags in `core/caption_engine.py`
4. Update the caption `fallback_templates` in `config.yaml`
5. Update the publishing Instagram account credentials in `.env`:
   - `IG_ACCOUNT_ID` → [NEW_IG_ACCOUNT_ID from meta_accounts_dump.json]
   - `FB_PAGE_ID` → [NEW_FB_PAGE_ID]
   - `FB_PAGE_ACCESS_TOKEN` → [NEW_FB_PAGE_ACCESS_TOKEN]
   - `CLOUDINARY_FOLDER` → [NEW_FOLDER_NAME] (e.g. account_name/reposts)
   - `META_ACCESS_TOKEN` → [NEW_META_ACCESS_TOKEN — long-lived]
6. Update Google Sheets URL in `core/sheets_reader.py` → SHEET_CSV_URL
   New sheet: [NEW_GOOGLE_SHEET_URL]
7. Update `README.md` with the new source account and niche description
8. Update docstrings and hardcoded fallback account in `agents/repost_agent.py`
9. Clear `data/tracker.xlsx` (reset dedup tracker for new niche)
10. Deploy to a new GitHub repo: [NEW_GITHUB_REPO_URL]
    - For YouTube: new channel → run `python tools/yt_auth.py` to generate new refresh token
    - OR reuse existing YT channel credentials

Please:
- First tell me the plan and all required changes — NO code changes until I say go
- Ask me if anything is unclear
- After I approve, make all local changes first so I can test with `python main.py --repost`
- No git/GitHub changes until local test passes

**Answers to standard questions:**
- Publishing Instagram account: [ACCOUNT_NAME from meta_accounts_dump.json]
- YouTube channel: [new / same]
- Google Sheets: [NEW / SAME — URL: ]
- New GitHub repo name: [REPO_URL]
```

---

## Checklist of Files That Change Every Niche Switch

| File | What Changes |
|---|---|
| `config.yaml` | `source_accounts`, YT `category_id`, `tags`, caption `fallback_templates`, `facebook.page_name` |
| `core/caption_engine.py` | `_KEYWORDS`, `_PRE_HOOKS`, `_HOOKS`, `_HASHTAGS` — all niche-specific content |
| `core/sheets_reader.py` | `SHEET_CSV_URL` — point to new Google Sheet |
| `agents/repost_agent.py` | Docstring (line 47) + hardcoded fallback account (line 70) |
| `README.md` | Source account, niche description, project title |
| `.env` | `IG_ACCOUNT_ID`, `FB_PAGE_ID`, `FB_PAGE_ACCESS_TOKEN`, `META_ACCESS_TOKEN`, `CLOUDINARY_FOLDER`, YT tokens if new channel |
| `.env.template` | Comment updates to reflect new niche |
| `data/tracker.xlsx` | Clear/reset — old post IDs irrelevant for new niche |
| `.git/` | Delete + reinit → new GitHub repo + add all Secrets |

---

## GitHub Secrets Migration

To copy all secrets from your local `.env` to the new GitHub repository quickly:
```bash
python tools/migrate_secrets.py mahaboob9143/new-repo-name
```
(Requires [GitHub CLI](https://cli.github.com/) installed and authenticated)

## YouTube Auth (if new channel)

Run once locally after setting up Google Cloud credentials:
```bash
python tools/yt_auth.py
```
Copy the generated `YT_REFRESH_TOKEN` into `.env` and GitHub Secrets.

## Meta Long-Lived Token (always needed)

1. Go to [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Generate User Token with scopes: `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`
3. Exchange for long-lived token:
```
GET https://graph.facebook.com/v21.0/oauth/access_token
    ?grant_type=fb_exchange_token
    &client_id=YOUR_APP_ID
    &client_secret=YOUR_APP_SECRET
    &fb_exchange_token=SHORT_LIVED_TOKEN
```
4. Get IG Account ID:
```
GET https://graph.facebook.com/v21.0/{FB_PAGE_ID}?fields=instagram_business_account&access_token={LONG_LIVED_TOKEN}
```
