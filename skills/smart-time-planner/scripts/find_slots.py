#!/usr/bin/env python3
"""Portable skill helper; no accounts, network access, or writes."""
import json
import sys
from datetime import date, datetime
from zoneinfo import ZoneInfo

from calendar_engine import Event, slots


def main():
    data = json.load(sys.stdin)
    events = [Event(str(item["id"]), item.get("title", "Busy"),
                    datetime.fromisoformat(item["start"]), datetime.fromisoformat(item["end"]),
                    busy=item.get("busy", True)) for item in data["events"]]
    result = slots(events, date.fromisoformat(data["date"]), ZoneInfo(data["timezone"]),
                   data["minutes"], data.get("working_start", 8), data.get("working_end", 22),
                   data.get("buffer_minutes", 15))
    print(json.dumps({"slots": result}, indent=2))


if __name__ == "__main__":
    main()
