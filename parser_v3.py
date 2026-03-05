#!/usr/bin/env python3
from __future__ import annotations
import re, csv, json
from pathlib import Path
from datetime import datetime

HEADERS = [
    'PrimaryKey','Date','ChemSystem','SampleModel','ParallelCount','SampleSerial','TestItem',
    'TestCondition','TempCondition','RunVersion','EquipmentFixture','TestResultLevel',
    'FormulaAdditive','Note','Confidence'
]

TEMP_MAP = {
    'RT':'RT','室溫':'RT','25C':'RT','25℃':'RT',
    '45C':'45℃','45℃':'45℃','45°C':'45℃',
    '60C':'60℃','60℃':'60℃','60°C':'60℃',
}

LEVEL_RE = re.compile(r'\b(?:HSL|LV|L)\s*([1-7])\b', re.I)
DATE_RE = re.compile(r'(20\d{6})')
MODEL_RE = re.compile(r'\\(\d{6})\\')
CHEM_RE = re.compile(r'\b(AP\d{2}|SN\d{2}(?:\.\d+)?(?:\+\+)?(?:\.\d+)?\'?)\b')
PARA_RE = re.compile(r'\b(\d+(?:\+\d+)?P)\b', re.I)
SERIAL_RE = re.compile(r'(?:45-)?(?:5S|5T)\d{9,}-\d{3,4}', re.I)
RUN_RE = re.compile(r'(run\d+|#\d+R\d+|#\d+|R\d+)\b', re.I)
VOL_RE = re.compile(r'\b(4\.\d{1,3}V|4\.35V|4\.2V|4\.0V|4\.05V)\b', re.I)
COND_RE = re.compile(r'\b(\d+(?:\.\d+)?mm|\d+(?:\.\d+)?mms|\d+%|CW\d+)\b', re.I)


def norm_date(raw: str) -> str:
    m = DATE_RE.search(raw)
    if not m: return ''
    d = m.group(1)
    return f'{d[:4]}-{d[4:6]}-{d[6:8]}'


def pick_best(cands):
    if not cands: return ''
    return sorted(cands, key=lambda x: (-len(x), x))[0]


def parse_line(line: str) -> dict:
    s = line.strip()
    row = {k:'' for k in HEADERS}
    if not s:
        row['Confidence'] = 'Low'; return row
    row['Date'] = norm_date(s)
    mm = MODEL_RE.search(s)
    row['SampleModel'] = mm.group(1) if mm else ''
    cm = CHEM_RE.search(s)
    row['ChemSystem'] = cm.group(1) if cm else ''
    pm = PARA_RE.search(s)
    row['ParallelCount'] = pm.group(1).upper() if pm else ''
    serials = SERIAL_RE.findall(s)
    row['SampleSerial'] = pick_best(serials)

    row['TestItem'] = '穿刺' if ('穿刺' in s or '穿刺影片' in s) else ''

    temps = [k for k in TEMP_MAP if k in s]
    row['TempCondition'] = TEMP_MAP[temps[0]] if temps else ''

    rv = RUN_RE.findall(s)
    row['RunVersion'] = (rv[0].lower() if rv else '')

    lv = [f'HSL{m.group(1)}' for m in LEVEL_RE.finditer(s)]
    row['TestResultLevel'] = ','.join(dict.fromkeys(lv))

    conds = COND_RE.findall(s) + VOL_RE.findall(s)
    row['TestCondition'] = ','.join(dict.fromkeys([c for c in conds if c]))

    if row['Date'] and row['SampleModel'] and row['RunVersion']:
        row['PrimaryKey'] = f"{row['Date'].replace('-','')}-{row['SampleModel']}-{row['RunVersion']}"

    core_ok = sum(bool(row[k]) for k in ['Date','ChemSystem','SampleModel','TestItem','TempCondition'])
    row['Confidence'] = 'High' if core_ok >= 5 else ('Med' if core_ok >= 3 else 'Low')

    if not row['ChemSystem'] or not row['SampleSerial']:
        row['Note'] = 'needs-dictionary-alignment'
    return row


def load_lines(path: Path):
    if path.suffix.lower() == '.txt':
        return [x.strip() for x in path.read_text(encoding='utf-8', errors='ignore').splitlines() if x.strip()]
    if path.suffix.lower() == '.csv':
        out=[]
        with path.open(encoding='utf-8', errors='ignore') as f:
            r=csv.reader(f)
            for row in r:
                if not row: continue
                out.append(' '.join(row).strip())
        return out
    raise ValueError('only txt/csv supported')


def main(inp: str, out_csv: str):
    lines = load_lines(Path(inp))
    rows = [parse_line(x) for x in lines]
    p = Path(out_csv)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader(); w.writerows(rows)
    print(f'parsed={len(rows)} -> {p}')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('usage: parser_v3.py <input.txt|input.csv> <output.csv>')
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2])
