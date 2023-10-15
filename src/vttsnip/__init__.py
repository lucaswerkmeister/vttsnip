import datetime
import re
import sys

def timestamp_to_timedelta(webvtt_timestamp: str) -> datetime.timedelta:
    hours, minutes, seconds, frac = re.match(r'(?:([0-9]{2,}):)?([0-9]{2}):([0-9]{2}).([0-9]{3})', webvtt_timestamp).groups()
    return datetime.timedelta(
        hours=int(hours or '0'),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(frac),
    )

def timedelta_to_timestamp(timedelta: datetime.timedelta) -> str:
    hours = timedelta.seconds // 3600
    minutes = timedelta.seconds % 3600 // 60
    seconds = timedelta.seconds % 60
    milliseconds = timedelta.microseconds // 1000
    return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}'

adjustments_ = [
    ('14:50.000', 5000),
    ('27:02.000', 8800 - 5000),
]
adjustments = [
    (timestamp_to_timedelta(ts), datetime.timedelta(milliseconds=ms))
    for ts, ms in adjustments_
]
adjustments.sort(reverse=True)

def main() -> None:
    for line in sys.stdin:
        if '-->' not in line:
            print(line, end='')
            continue
        ts_from, ws1, arrow, ws2, ts_to, rest = re.match(r'([^ \t]+)([ \t]+)(-->)([ \t]+)([^ \t]+)(.*)', line, re.DOTALL).groups()
        td_from = timestamp_to_timedelta(ts_from)
        td_to = timestamp_to_timedelta(ts_to)
        for adj_td_from, adj_td_add in adjustments:
            if td_from >= adj_td_from:
                td_from += adj_td_add
                td_to += adj_td_add
        ts_from = timedelta_to_timestamp(td_from)
        ts_to = timedelta_to_timestamp(td_to)
        print(ts_from + ws1 + arrow + ws2 + ts_to + rest, end='')