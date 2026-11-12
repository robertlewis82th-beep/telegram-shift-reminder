import os
import sys
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=5))  # Tashkent has no daylight saving time
SCHEDULE = {
    '17:00': 'Robert 5-8pm',
    '20:00': 'Samuel 8-11pm',
    '23:00': 'Frank 11pm-1am',
    '01:00': 'Daniel 1-3am',
    '03:00': 'Andrey 3-5am',
    '05:00': 'Adam 5-7am',
}

def send(text):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        raise RuntimeError('Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID as GitHub Actions secrets')
    data = urllib.parse.urlencode({'chat_id': chat_id, 'text': text}).encode()
    request = urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage', data=data, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.load(response)
    except Exception as exc:
        raise RuntimeError(f'Telegram request failed: {exc}') from exc
    if not result.get('ok'):
        raise RuntimeError('Telegram API did not confirm delivery')
    print('Telegram message sent:', text)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--test':
        send('Test notification - bot connected')
    else:
        # GitHub cron can start late. Each cron entry specifies the intended
        # slot in UTC, avoiding missed sends caused by minute-level delays.
        slot = os.environ.get('SHIFT_SLOT', '')
        if slot not in SCHEDULE:
            raise RuntimeError('SHIFT_SLOT must match a scheduled Tashkent HH:MM time')
        send(SCHEDULE[slot])
