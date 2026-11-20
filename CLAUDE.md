# Xedine Social Autopilot: notes for Claude

Posts the Xedine brand's content to its own four accounts, by itself, from GitHub Actions. A copy of the
Xegency bot (`E:\social-manager\social-media`), with its own accounts, queue, secrets and state.
Do NOT put Xegency's tokens here and do NOT put Xedine's tokens in the Xegency repo.

## Accounts
| Platform | Account | How it posts |
|---|---|---|
| Facebook | Page "Xedine" (facebook.com/xedine) | Meta Graph API, Page token |
| Instagram | @xedine.ai | Meta Graph API |
| TikTok | @xedine.ai (xestore777@gmail.com via Google) | Buffer free plan |
| YouTube | @xedineai (rifatcore1@gmail.com, Chrome Profile 3) | Buffer free plan (Google's API only allows private uploads until audited) |

## Hard rules
- Zero budget: free tools only. Repo stays public (free Actions cron and GitHub Pages).
- Never commit `.env` or any token. Secrets live in GitHub Secrets (`python -m bot secrets`).
- Public text: the founder's rules in `E:\xedine.org` memory: chef logo, example numbers are labelled "উদাহরণ",
  no invented results, hashtags in English only (the bot strips Bangla vowel signs from hashtags).
- The 14 launch videos (Bangla, 15-19 s) are in `content/media/`, made in `E:\Editing\projects\_xedine-batch`.
  `tools_make_posts.py` regenerates `content/posts/*.md` from them (2 a day, 12:00 and 21:00 Asia/Dhaka).

## Run
`E:\social-manager\social-media\.venv\Scripts\python.exe -m bot <validate|plan|health|auth ...>` from this folder
(that venv works here; C: is nearly full, do not create a new one). Tests: `python -m pytest -q`.
