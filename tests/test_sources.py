"""读取合成业务交接资料并核对表间关联。"""
import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "samples"

HEADERS = {'shows.csv': ['show', 'title', 'room', 'start', 'capacity', 'access_seats', 'round', 'state'], 'releases.csv': ['release', 'show', 'at', 'supply', 'taken', 'state'], 'groups.csv': ['group', 'size', 'access', 'indivisible', 'preferred', 'received'], 'tickets.csv': ['receipt', 'group', 'show', 'kind', 'event_at', 'received', 'hold_until'], 'copies.csv': ['copy', 'title', 'format', 'feature', 'valid_from', 'valid_to', 'currently_at'], 'room_paths.csv': ['origin', 'destination', 'travel_minutes', 'formats', 'access_features'], 'changes.csv': ['change', 'show', 'reported', 'effective', 'kind']}
REFERENCES = [('releases.csv', 'show', 'shows.csv', 'show'), ('tickets.csv', 'show', 'shows.csv', 'show'), ('tickets.csv', 'group', 'groups.csv', 'group'), ('changes.csv', 'show', 'shows.csv', 'show'), ('copies.csv', 'title', 'shows.csv', 'title')]
OBSERVED_VALUES = [('releases.csv', 'show', 'S1', 2), ('tickets.csv', 'receipt', 'T4', 1), ('groups.csv', 'group', 'G2', 1)]

class SampleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {}
        for name in HEADERS:
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source, strict=True)
                if reader.fieldnames != HEADERS[name]:
                    raise ValueError(f"字段不一致：{name}")
                cls.sources[name] = list(reader)

    def test_tabular_structure(self):
        for name, rows in self.sources.items():
            with self.subTest(source=name):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_keys(self):
        for left, column, right, target in REFERENCES:
            with self.subTest(source=left, field=column):
                actual = {row[column] for row in self.sources[left] if row[column]}
                allowed = {row[target] for row in self.sources[right] if row[target]}
                self.assertTrue(actual)
                self.assertEqual(actual - allowed, set())

    def test_shared_or_revised_facts_have_source_rows(self):
        for name, column, value, minimum in OBSERVED_VALUES:
            with self.subTest(source=name, field=column, value=value):
                self.assertGreaterEqual(sum(row[column] == value for row in self.sources[name]), minimum)
