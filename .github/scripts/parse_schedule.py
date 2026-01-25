#!/usr/bin/env python3
import os
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def write_output(key: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"{key}={value}\n")


def fail(message: str) -> None:
    write_output("valid", "false")
    write_output("error", message)


raw = os.environ.get("RAW", "").strip()
if not raw:
    fail("Missing schedule time.")
    raise SystemExit(0)

normalized = re.sub(r"\s+", " ", raw).strip()
match = re.match(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{1,2}(:\d{2})?\s*(am|pm)?)\s*(?P<tz>ct|cst|cdt)?$",
    normalized,
    re.IGNORECASE,
)

if not match:
    fail(
        "Invalid time format. Use `/schedule-merge YYYY-MM-DD HH:MM CT` or `/schedule-merge YYYY-MM-DD 9am CT`."
    )
    raise SystemExit(0)

date_part = match.group("date")
time_part = match.group("time").strip().lower()

hour = None
minute = 0

ampm_match = re.match(r"^(?P<h>\d{1,2})(:(?P<m>\d{2}))?(?P<ampm>am|pm)$", time_part.replace(" ", ""))
if ampm_match:
    hour = int(ampm_match.group("h"))
    minute = int(ampm_match.group("m") or 0)
    ampm = ampm_match.group("ampm")
    if hour < 1 or hour > 12 or minute > 59:
        fail("Invalid time value.")
        raise SystemExit(0)
    if ampm == "pm" and hour != 12:
        hour += 12
    if ampm == "am" and hour == 12:
        hour = 0
else:
    hm_match = re.match(r"^(?P<h>\d{1,2})(:(?P<m>\d{2}))?$", time_part)
    if not hm_match:
        fail("Invalid time value.")
        raise SystemExit(0)
    hour = int(hm_match.group("h"))
    minute = int(hm_match.group("m") or 0)
    if hour > 23 or minute > 59:
        fail("Invalid time value.")
        raise SystemExit(0)

year, month, day = [int(part) for part in date_part.split("-")]
local_tz = ZoneInfo("America/Chicago")
try:
    local_dt = datetime(year, month, day, hour, minute, tzinfo=local_tz)
except ValueError:
    fail("Invalid calendar date.")
    raise SystemExit(0)
utc_dt = local_dt.astimezone(timezone.utc)

now_utc = datetime.now(timezone.utc)
if utc_dt <= now_utc:
    fail("Scheduled time must be in the future.")
    raise SystemExit(0)

utc_iso = utc_dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")
local_iso = local_dt.replace(microsecond=0).isoformat()

write_output("valid", "true")
write_output("utc", utc_iso)
write_output("local", local_iso)
write_output("display", local_dt.strftime("%Y-%m-%d %I:%M %p CT"))
