---
name: smart-time-planner
description: Find task-appropriate calendar gaps using duration, working hours, buffers and explicit preferences.
version: 0.1.0
---

1. Establish the task's date and duration. Ask if either is ambiguous.
2. In the A3 assistant, call a3_find_time(date, minutes). Respect the returned working hours,
   buffers and current-time boundary. Do not invent availability.
3. Recommend one or two returned slots with a reason; keep calendar changes separate for review.
4. Outside the A3 app, the included Python helper computes slots from supplied JSON using only
   the standard library. Read references/input-example.json for the schema. Pass the input on
   stdin to scripts/find_slots.py. It does not authenticate to a calendar or change any events.

The calendar adapter must expand recurring events first and exclude cancelled/transparent
busy time appropriately. A scheduling suggestion is not a completed task.

Install this bundle through a Hermes GitHub skill tap. See the repository README for installation and the standalone input format.
