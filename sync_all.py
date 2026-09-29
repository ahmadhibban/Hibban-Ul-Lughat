#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_all.py
Synchronizes urdu_bangla.json to data.js, index.html, and urdu_bangla.db.
Works cross-platform in pure Python 3 without requiring Windows DLLs.
"""

import json
import sqlite3
import os
import sys

def sync():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "urdu_bangla.json")
    data_js_path = os.path.join(base_dir, "data.js")
    html_path = os.path.join(base_dir, "index.html")
    db_path = os.path.join(base_dir, "urdu_bangla.db")

    print(f"Reading {json_path}...")
    with open(json_path, "r", encoding="utf-8-sig") as f:
        entries = json.load(f)

    print(f"Total entries loaded: {len(entries)}")

    # Check validity
    empty_bengali = [e['urdu'] for e in entries if not e.get('bengali') or not e['bengali'].strip()]
    if empty_bengali:
        print(f"WARNING: {len(empty_bengali)} entries have empty Bengali translations: {empty_bengali[:5]}")
    else:
        print("All entries have non-empty Bengali translations!")

    # 1. Ensure urdu_bangla.json is cleanly formatted
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print("urdu_bangla.json saved.")

    # 2. Build data.js
    print("Generating data.js...")
    dict_map = {}
    word_list = []
    raw_words = []

    for item in entries:
        u = item["urdu"]
        b = item["bengali"]
        dict_map[u] = b
        word_list.append({"ur": u, "bn": b})
        raw_words.append([u, b])

    dict_json = json.dumps(dict_map, ensure_ascii=False)
    words_json = json.dumps(word_list, ensure_ascii=False)

    data_js_content = f"window.OFFLINE_DICT = {dict_json};\r\nwindow.OFFLINE_WORDS = {words_json};"
    with open(data_js_path, "w", encoding="utf-8") as f:
        f.write(data_js_content)
    print(f"data.js saved ({len(data_js_content)} chars).")

    # 3. Update index.html
    print("Updating index.html...")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    start_marker = "<!-- EMBEDDED WORDS DATASET"
    end_marker = "// Data Structures"
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker, start_idx)

    if start_idx >= 0 and end_idx >= 0:
        script_start = html.rfind("<script", 0, end_idx)
        raw_json = json.dumps(raw_words, ensure_ascii=False)
        embedded_snippet = (
            "<!-- EMBEDDED WORDS DATASET (100% Offline, Zero-Latency, Zero-CORS) -->\r\n"
            f'    <script id="embeddedData">\r\n        const RAW_WORDS = {raw_json};\r\n    </script>\r\n\r\n    '
        )
        part1 = html[:start_idx] + embedded_snippet
        part2 = html[script_start:]
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(part1 + part2)
        print("index.html updated successfully.")
    else:
        print("WARNING: Could not find dataset markers in index.html!")

    # 4. Synchronize SQLite urdu_bangla.db
    print("Synchronizing SQLite urdu_bangla.db...")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("BEGIN TRANSACTION;")
    cur.execute("DELETE FROM words;")
    
    rows = []
    for item in entries:
        u = item["urdu"]
        b = item["bengali"]
        t = item.get("translations")
        if not t:
            t = [p.strip() for p in b.replace(";", ",").replace("।", ",").split(",") if p.strip()]
        t_json = json.dumps(t, ensure_ascii=False)
        rows.append((u, b, t_json))

    cur.executemany("INSERT INTO words (urdu, bengali, translations) VALUES (?, ?, ?);", rows)
    conn.commit()
    cur.execute("SELECT count(*) FROM words;")
    count_db = cur.fetchone()[0]
    conn.close()
    print(f"SQLite urdu_bangla.db synchronized with {count_db} words.")
    print("ALL 4 ARTIFACTS FULLY SYNCHRONIZED SUCCESSFULLY!")

if __name__ == "__main__":
    sync()
