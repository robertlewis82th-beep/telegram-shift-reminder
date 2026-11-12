# Telegram Shift Reminder

Six daily messages to one Telegram group, based on Tashkent (UTC+5) time.

## Setup
1. Create a GitHub repository and upload `bot.py` and `.github/workflows/notify.yml` preserving paths.
2. In repository Settings > Secrets and variables > Actions, create repository secrets `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
3. Open Actions > Telegram shift notifications > Run workflow to send a test message.
4. GitHub runs scheduled workflows on the default branch automatically.

## Chat ID
Send `/start` in the group, then use `https://api.telegram.org/bot<TOKEN>/getUpdates` privately to locate the group `chat.id`. Never share the token or commit it to GitHub.

## Timing
GitHub Actions scheduled workflows may be delayed or dropped under load. This solution is best-effort, not guaranteed exact-minute delivery. A missed scheduled job will not automatically be replayed. The workflow uses fixed UTC times because Tashkent does not observe DST.
