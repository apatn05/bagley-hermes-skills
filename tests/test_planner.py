import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/smart-time-planner'

class PlannerTests(unittest.TestCase):
    def test_portable_example_and_task_duration(self):
        data = (SKILL/'references/input-example.json').read_bytes()
        result = subprocess.run([sys.executable,str(SKILL/'scripts/find_slots.py')],input=data,capture_output=True,check=True)
        slots = json.loads(result.stdout)['slots']
        self.assertEqual(slots[0]['suggested_start'],'2026-11-12T10:15:00-08:00')
        self.assertEqual(slots[0]['suggested_end'],'2026-11-12T11:45:00-08:00')
        self.assertEqual(slots[0]['suggested_duration_minutes'],90)
        self.assertGreater(slots[0]['available_minutes'],90)

    def test_invalid_duration_produces_no_successful_output(self):
        data = json.loads((SKILL/'references/input-example.json').read_text())
        data['minutes'] = 0
        result = subprocess.run([sys.executable,str(SKILL/'scripts/find_slots.py')],input=json.dumps(data).encode(),capture_output=True)
        self.assertNotEqual(result.returncode,0)
        self.assertFalse(result.stdout)
