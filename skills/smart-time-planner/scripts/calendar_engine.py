"""Calendar arithmetic is deterministic; models explain results, not invent availability."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Event:
    id: str
    title: str
    start: datetime
    end: datetime
    description: str = ""
    busy: bool = True

    def __post_init__(self):
        if self.start.tzinfo is None or self.end.tzinfo is None:
            raise ValueError("Events must have timezone-aware timestamps.")
        if self.end.astimezone(timezone.utc) <= self.start.astimezone(timezone.utc):
            raise ValueError("Event end must follow its start.")

    def to_dict(self):
        return {**asdict(self), "start": self.start.isoformat(), "end": self.end.isoformat()}


def from_google(item: dict, default_zone: str) -> Event | None:
    if item.get("status") == "cancelled":
        return None
    zone = ZoneInfo(default_zone)

    def stamp(value):
        if "dateTime" in value:
            parsed = datetime.fromisoformat(value["dateTime"].replace("Z", "+00:00"))
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=ZoneInfo(value.get("timeZone", default_zone)))
        # Google all-day end dates are exclusive, including across DST boundaries.
        return datetime.combine(date.fromisoformat(value["date"]), time(), zone)

    return Event(str(item["id"]), item.get("summary", "Untitled event"), stamp(item["start"]),
                 stamp(item["end"]), item.get("description", ""), item.get("transparency") != "transparent")


def conflicts(events: list[Event]) -> list[dict]:
    busy = sorted((e for e in events if e.busy), key=lambda e: e.start.astimezone(timezone.utc))
    found = []
    for i, first in enumerate(busy):
        first_start, first_end = first.start.astimezone(timezone.utc), first.end.astimezone(timezone.utc)
        for second in busy[i + 1:]:
            second_start, second_end = second.start.astimezone(timezone.utc), second.end.astimezone(timezone.utc)
            if second_start >= first_end:
                break
            found.append({"event_ids": [first.id, second.id], "titles": [first.title, second.title],
                          "start": max(first_start, second_start).astimezone(first.start.tzinfo).isoformat(),
                          "end": min(first_end, second_end).astimezone(first.start.tzinfo).isoformat()})
    return found


def slots(events: list[Event], day: date, zone: ZoneInfo, duration: int = 60,
          start_hour: int = 8, end_hour: int = 22, buffer: int = 15,
          not_before: datetime | None = None) -> list[dict]:
    if not 1 <= duration <= 840 or not 0 <= buffer <= 120 or not 0 <= start_hour < end_hour <= 23:
        raise ValueError("Invalid duration, work hours, or buffer.")
    start = datetime.combine(day, time(start_hour), zone).astimezone(timezone.utc)
    end = datetime.combine(day, time(end_hour), zone).astimezone(timezone.utc)
    cursor = max(start, not_before.astimezone(timezone.utc)) if not_before else start
    if cursor >= end:
        return []
    intervals = sorted((max(start, e.start.astimezone(timezone.utc) - timedelta(minutes=buffer)),
                        min(end, e.end.astimezone(timezone.utc) + timedelta(minutes=buffer)))
                       for e in events if e.busy and e.end.astimezone(timezone.utc) > start
                       and e.start.astimezone(timezone.utc) < end)
    gaps = []
    for left, right in intervals + [(end, end)]:
        if left - cursor >= timedelta(minutes=duration):
            gaps.append({"start": cursor.astimezone(zone).isoformat(), "end": left.astimezone(zone).isoformat(),
                         "available_minutes": int((left - cursor).total_seconds() // 60),
                         "suggested_start": cursor.astimezone(zone).isoformat(),
                         "suggested_duration_minutes": duration,
                         "suggested_end": (cursor + timedelta(minutes=duration)).astimezone(zone).isoformat()})
        cursor = max(cursor, right)
    return gaps
