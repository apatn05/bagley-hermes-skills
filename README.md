# Bagley Smart Time Planner — Hermes skill tap

A reusable skill for finding task-sized gaps around calendar events. It respects
working hours, buffers and time zones, and distinguishes a complete free window
from the smaller proposed session inside it. It never changes calendar events.

The portable Python helper uses only the standard library; no credentials,
accounts or network access are needed. An assistant may explain the computed
slots, but should not invent availability. Recurring events must be expanded by
the calendar adapter before supplying them. Inputs and examples are fictional.

## Install with Hermes

```sh
hermes skills tap add apatn05/bagley-hermes-skills
hermes skills install apatn05/bagley-hermes-skills/skills/smart-time-planner
```

Use the Hermes skill-tap installer, not a direct SKILL.md URL. A fresh-install
transcript, resolved commit and bundle verification are recorded separately with
the assignment after publication. This repository contains only the reusable
skill, not account credentials or the complete assignment application.

## Run the portable helper

From the installed smart-time-planner directory:

```sh
python3 scripts/find_slots.py < references/input-example.json
```

Input fields: date (YYYY-MM-DD), IANA timezone, minutes (1–840), working_start and
working_end (whole hours), buffer_minutes (0–120), and events with id, title,
start/end ISO timestamps containing offsets, and optional busy boolean. Output
contains each free window's start/end and available_minutes, plus a task-sized
suggested_start/suggested_end and suggested_duration_minutes. Invalid durations,
work hours or event ranges fail rather than producing invented slots.

Example expected result: for a 09:00–10:00 fictional meeting, 15-minute buffers,
08:00–18:00 work hours and a 90-minute task, the usable window starts at 10:15 and
the first suggested session ends at 11:45.

## Development and attribution

Developed for CSCI 599 Assignment 3 with AI-assisted scaffolding and human review.
Calendar calculations use Python datetime/zoneinfo and explicit UTC comparisons.
The tap layout follows the official Hermes Skills System documentation:
https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
The skill's Python helper was extracted from Bagley's calendar planner so it can
run without the assistant, Google integration or Hermes tool registration.

Run `python3 -m unittest discover -s tests -v` for offline tests.
