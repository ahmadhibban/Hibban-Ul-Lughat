# -*- coding: utf-8 -*-
import sqlite3, os, json, re
from collections import defaultdict

# -----------------------------------------------------------------------------
# Configuration: Letters and exact 32,000 prevalent targets
# -----------------------------------------------------------------------------
LETTER_TARGETS = [
    (1,  'آ', 'alif_madd', 581),
    (2,  'ا', 'alif',      2633),
    (3,  'ب', 'be',        2500),
    (4,  'پ', 'pe',        2130),
    (5,  'ت', 'te',        2415),
    (6,  'ٹ', 'te_dal',     487),
    (7,  'ث', 'se',          95),
    (8,  'ج', 'jim',       1198),
    (9,  'چ', 'che',       1170),
    (10, 'ح', 'he_bari',    489),
    (11, 'خ', 'khe',        692),
    (12, 'د', 'dal',       1110),
    (13, 'ڈ', 'dal_re',     401),
    (14, 'ذ', 'zal',        118),
    (15, 'ر', 're',         934),
    (16, 'ڑ', 're_ar',        0),   # No words start with ڑ
    (17, 'ز', 'ze',         335),
    (18, 'ژ', 'zhe',         11),
    (19, 'س', 'sin',       1516),
    (20, 'ش', 'shin',       453),
    (21, 'ص', 'swad',       189),
    (22, 'ض', 'zwad',        94),
    (23, 'ط', 'toe',        278),
    (24, 'ظ', 'zoe',         46),
    (25, 'ع', 'ain',        480),
    (26, 'غ', 'ghain',      200),
    (27, 'ف', 'fe',         489),
    (28, 'ق', 'qaf',        403),
    (29, 'ک', 'kaf',       1594),
    (30, 'گ', 'gaf',        773),
    (31, 'ل', 'lam',        705),
    (32, 'م', 'mim',       4701),
    (33, 'ن', 'nun',       1815),
    (34, 'و', 'waw',        438),
    (35, 'ہ', 'chhoti_he',  381),
    (36, 'ی', 'ye',         146),
]

assert sum(t[3] for t in LETTER_TARGETS) == 32000, "Targets must sum to 32,000 exactly!"

URDU_ALPHABET = [
    'آ', 'ا', 'ب', 'پ', 'ت', 'ٹ', 'ث', 'ج', 'چ', 'ح', 'خ',
    'د', 'ڈ', 'ذ', 'ر', 'ڑ', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض',
    'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن',
    'ں', 'و', 'ہ', 'ھ', 'ء', 'ی', 'ئ', 'ے'
]
URDU_RANK = {ch: i for i, ch in enumerate(URDU_ALPHABET)}

def urdu_sort_key(word):
    return [URDU_RANK.get(ch, 999) for ch in word]

os.makedirs('letters', exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Load Data Sources
# -----------------------------------------------------------------------------
print("Loading Qaumi Lughat...")
conn1 = sqlite3.connect('databases/Offline_Urdu_to_Urdu_Lughat_urdu_dict.db')
c1 = conn1.cursor()
c1.execute("SELECT word, info FROM contents;")
qaumi_by_letter = defaultdict(dict)
for w, info in c1.fetchall():
    clean = w.strip()
    if ' ' not in clean and '-' not in clean and '\u200c' not in clean:
        if re.match(r'^[\u0600-\u06FF]+$', clean) and len(clean) >= 2:
            first_ch = clean[0]
            if first_ch not in qaumi_by_letter[first_ch]:
                qaumi_by_letter[first_ch][clean] = info or ''
conn1.close()
print("Qaumi Lughat loaded.")

print("Loading Offline Urno Modern Dictionary...")
conn2 = sqlite3.connect('databases/Offline_Urdu_to_Urdu_Lughat_urno_dict.db')
c2 = conn2.cursor()
c2.execute("SELECT word FROM urdu;")
urno_by_letter = defaultdict(set)
for r in c2.fetchall():
    w = r[0].strip()
    if ' ' not in w and '-' not in w and '\u200c' not in w:
        clean = re.sub(r'[\u064b-\u065f\u0670]', '', w)
        if re.match(r'^[\u0600-\u06FF]+$', clean) and len(clean) >= 2:
            first_ch = clean[0]
            urno_by_letter[first_ch].add(clean)
conn2.close()
print("Offline Urno loaded.")

print("Loading Nerdcats Conversational Dictionary...")
conn3 = sqlite3.connect('databases/Nerdcats_English_Urdu_Dictionary.db')
c3 = conn3.cursor()
c3.execute("SELECT fr FROM word;")
nerdcats_by_letter = defaultdict(set)
for r in c3.fetchall():
    for part in re.split(r'[,،;\n]+', r[0]):
        w = part.strip()
        if ' ' not in w and '-' not in w and '\u200c' not in w:
            clean = re.sub(r'[\u064b-\u065f\u0670]', '', w)
            if re.match(r'^[\u0600-\u06FF]+$', clean) and len(clean) >= 2:
                first_ch = clean[0]
                nerdcats_by_letter[first_ch].add(clean)
conn3.close()
print("Nerdcats loaded.")

print("Loading Urdu-Bangla Lexicon...")
with open('urdu_bangla.json', 'r', encoding='utf-8') as f:
    ub = json.load(f)
ub_by_letter = defaultdict(dict)
for k, v in ub.items():
    clean = k.strip()
    if ' ' not in clean and '-' not in clean and '\u200c' not in clean:
        if re.match(r'^[\u0600-\u06FF]+$', clean) and len(clean) >= 2:
            first_ch = clean[0]
            m = v.strip()
            if m:
                ub_by_letter[first_ch][clean] = m
print("Urdu-Bangla Lexicon loaded.")

# -----------------------------------------------------------------------------
# 2. Process Each Letter
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("PROCESSING ALL LETTERS TO COMPILE EXACTLY 32,000 PRISTINE WORDS")
print("=" * 80)

master_verified_dictionary = {}

for idx, letter, name, target in LETTER_TARGETS:
    filepath = f"letters/verified_{idx:02d}_{name}.json"
    
    if letter == 'ڑ' or target == 0:
        print(f"[{idx:02d}/36] Letter {letter} ({name}): 0 words (No words start with ڑ in Urdu).")
        continue

    # For Alif-Madd, preserve exact 581 verified words
    if letter == 'آ':
        with open('verified_alif_madd.json', 'r', encoding='utf-8') as f:
            letter_dict = json.load(f)
        assert len(letter_dict) == 581
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(letter_dict, f, ensure_ascii=False, indent=2)
        print(f"[{idx:02d}/36] Letter {letter} ({name}): Preserved {len(letter_dict)} verified words.")
        for k in sorted(letter_dict.keys(), key=urdu_sort_key):
            master_verified_dictionary[k] = letter_dict[k]
        continue

    # Build or expand verified dictionary for letter
    q_words = qaumi_by_letter.get(letter, {})
    u_words = urno_by_letter.get(letter, set())
    n_words = nerdcats_by_letter.get(letter, set())
    b_words = ub_by_letter.get(letter, {})

    # Load existing if available (e.g. Alif has curated words)
    existing_for_letter = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_for_letter = json.load(f)
        except Exception:
            existing_for_letter = {}

    # Tier 1: Prime candidates (in Urno OR Nerdcats, in Qaumi, and in UB)
    prime = (u_words | n_words) & set(q_words.keys()) & set(b_words.keys())
    clean_prime = [
        w for w in prime 
        if 'قدیم' not in q_words.get(w, '') 
        and 'متروک' not in q_words.get(w, '')
        and not any(sub in w for sub in ['الآ', 'الابد', 'ابوال', 'ابوتر'])
    ]
    clean_prime.sort(key=lambda w: (0 if w in n_words else 1, abs(len(w) - 5), w))

    # Tier 2: Secondary candidates (in Qaumi and in UB)
    sec = (set(q_words.keys()) & set(b_words.keys())) - set(clean_prime)
    clean_sec = [
        w for w in sec 
        if 'قدیم' not in q_words.get(w, '') 
        and 'متروک' not in q_words.get(w, '') 
        and 2 <= len(w) <= 8
        and not any(sub in w for sub in ['الآ', 'الابد', 'ابوال', 'ابوتر'])
    ]
    clean_sec.sort(key=lambda w: (abs(len(w) - 5), w))

    # Combine existing + clean_prime + clean_sec up to target
    letter_dict = dict(existing_for_letter)
    if len(letter_dict) < target:
        for w in clean_prime:
            if w not in letter_dict:
                m = b_words[w].strip()
                m = re.sub(r'[,،;\s]+$', '', m)
                letter_dict[w] = m
                if len(letter_dict) == target:
                    break
    if len(letter_dict) < target:
        for w in clean_sec:
            if w not in letter_dict:
                m = b_words[w].strip()
                m = re.sub(r'[,،;\s]+$', '', m)
                letter_dict[w] = m
                if len(letter_dict) == target:
                    break

    # Collation sort
    sorted_keys = sorted(letter_dict.keys(), key=urdu_sort_key)
    sorted_letter_dict = {k: letter_dict[k] for k in sorted_keys}

    assert len(sorted_letter_dict) == target, f"Letter {letter}: expected {target}, got {len(sorted_letter_dict)}"

    # Save letter file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(sorted_letter_dict, f, ensure_ascii=False, indent=2)

    # If Alif, also update verified_alif.json
    if letter == 'ا':
        with open('verified_alif.json', 'w', encoding='utf-8') as f:
            json.dump(sorted_letter_dict, f, ensure_ascii=False, indent=2)

    print(f"[{idx:02d}/36] Letter {letter} ({name}): Compiled and saved exactly {len(sorted_letter_dict)} words (target: {target}).")

    # Add to master dictionary
    for k in sorted_keys:
        master_verified_dictionary[k] = sorted_letter_dict[k]

# -----------------------------------------------------------------------------
# 3. Final Master Collation & App Updates
# -----------------------------------------------------------------------------
total_words = len(master_verified_dictionary)
print("\n" + "=" * 80)
print(f"MASTER DICTIONARY COMPILATION COMPLETE: {total_words} TOTAL VERIFIED WORDS")
print("=" * 80)
assert total_words == 32000, f"Expected exactly 32000 words, got {total_words}"

# Sort all words by Urdu alphabetical order
master_sorted_keys = sorted(master_verified_dictionary.keys(), key=urdu_sort_key)
master_sorted_dict = {k: master_verified_dictionary[k] for k in master_sorted_keys}

# 1. Save verified_words.json
with open('verified_words.json', 'w', encoding='utf-8') as f:
    json.dump(master_sorted_dict, f, ensure_ascii=False, indent=2)
print("Saved master verified_words.json successfully with exactly 32,000 words.")

# 2. Write words.js
js_words = [[k, val] for k, val in master_sorted_dict.items()]
words_js_content = 'window.RAW_WORDS = ' + json.dumps(js_words, ensure_ascii=False) + ';\nif (window.onWordsLoaded) { window.onWordsLoaded(); }\n'
with open('words.js', 'w', encoding='utf-8') as f:
    f.write(words_js_content)
print("Saved words.js successfully.")

# 3. Update index.html INITIAL_WORDS (top 50)
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

initial_50 = js_words[:50]
initial_js = 'const INITIAL_WORDS = ' + json.dumps(initial_50, ensure_ascii=False) + ';'
new_html = re.sub(r'const INITIAL_WORDS = \[.*?\];', initial_js, html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Updated index.html INITIAL_WORDS successfully.")

# 4. Bump sw.js cache to v12
with open('sw.js', 'r', encoding='utf-8') as f:
    sw = f.read()
new_sw = re.sub(r"const CACHE_NAME = 'hubban-lughat-v\d+';", "const CACHE_NAME = 'hubban-lughat-v12';", sw)
with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(new_sw)
print("Bumped sw.js cache to hubban-lughat-v12.")

print("\nALL TASKS 100% COMPLETE: EXACTLY 32,000 PREVALENT WORDS LIVE!")
