# InstaAgent — Cloud Repost Pipeline

A fully autonomous Instagram repost agent that scrapes content from travel creators, rewrites captions using a rule-based engagement engine, and publishes automatically via the official Meta Graph API.

**Source Account:** [@karadenizli.maceraci](https://www.instagram.com/karadenizli.maceraci/)
**Publishing Account:** [@food.timeez](https://www.instagram.com/food.timeez/)
**Niche:** Travel / Adventure / Nature / Black Sea (Turkey)

## 🌟 Key Features
- **3-Tier Fallback Architecture**: 
  1. **Auto-Scrape**: Scrapes public creator content using `instaloader`.
  2. **Manual Queue (Google Sheets)**: Automatically fetches specific unposted URLs from your private sheet.
  3. **Duplicate Safeguard**: Automatically re-uses high-performing old content if the queue is empty.
- **Rule-based Caption Engine**: Dynamically builds captions with:
  - **Travel Categories**: Scenic, Adventure, Cultural, Motivation.
  - **Auto-Hooks**: Weaves engaging travel-specific hooks & CTAs.
  - **Length Safety**: Automatically truncates captions to 2,200 chars to avoid Instagram API errors.
- **Advanced Asset Hosting**: 
  - **Cloudinary Integration**: Handles large video uploads for Meta API.
  - **Custom Folder Mapping**: Uses `CLOUDINARY_FOLDER` to organize assets per account.
- **YouTube Shorts Sync**: Simultaneously publishes reels to YouTube (Travel & Events category).
- **GitHub Actions Native**: Designed for 100% headless execution with automatic state tracking.

## 🚀 Setup & Deployment

1. **Local Credentials**: Copy `.env.template` to `.env` and fill in:
   - `IG_ACCOUNT_ID` & `META_ACCESS_TOKEN`
   - `CLOUDINARY_*` credentials
   - `YT_*` OAuth2 tokens
2. **Secrets Migration**: Use the included tool to push local secrets to GitHub:
   ```bash
   python tools/migrate_secrets.py mahaboob9143/your-repo-name
   ```
3. **Run Locally**:
   ```bash
   python main.py --repost
   ```

## 🔄 Niche Switch
This bot is designed to be pivoted to any niche in minutes. 
See [NICHE_SWITCH_PROMPT.md](NICHE_SWITCH_PROMPT.md) for the "one-shot" AI prompt and checklist.

## 📁 Directory Structure
- `agents/`: Core logic (RepostAgent, PosterAgent, YouTubePoster).
- `core/`: Utilities (Caption Engine, Cloudinary Uploader, Sheets Reader).
- `data/`: Excel-based repost tracker.
- `tools/`: Auth and secret migration utilities.
- `.github/workflows/`: Automation scheduling.
