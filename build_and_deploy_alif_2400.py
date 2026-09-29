# -*- coding: utf-8 -*-
import sqlite3, json, re

# 1. Load current 1000 verified words of Alif
with open('verified_alif.json', 'r', encoding='utf-8') as f:
    alif_1000 = json.load(f)

print(f"Base verified Alif words: {len(alif_1000)}")
assert len(alif_1000) == 1000, f"Expected 1000, got {len(alif_1000)}"

# 2. Extract next candidates from Qaumi Lughat & Urno & UB
conn1 = sqlite3.connect('databases/Offline_Urdu_to_Urdu_Lughat_urno_dict.db')
c1 = conn1.cursor()
c1.execute("SELECT word FROM urdu WHERE word LIKE 'ا%';")
urno = set(r[0].strip() for r in c1.fetchall() if r[0] and not r[0].startswith('آ') and ' ' not in r[0].strip() and '-' not in r[0].strip() and re.match(r'^[\u0600-\u06FF]+$', r[0].strip()))
conn1.close()

conn2 = sqlite3.connect('databases/Offline_Urdu_to_Urdu_Lughat_urdu_dict.db')
c2 = conn2.cursor()
c2.execute("SELECT word FROM contents WHERE word LIKE 'ا%';")
qaumi = set(r[0].strip() for r in c2.fetchall() if r[0] and not r[0].startswith('آ') and ' ' not in r[0].strip() and '-' not in r[0].strip() and re.match(r'^[\u0600-\u06FF]+$', r[0].strip()))
conn2.close()

with open('urdu_bangla.json', 'r', encoding='utf-8') as f:
    ub = json.load(f)
ub_keys = set(k.strip() for k in ub if k.startswith('ا') and not k.startswith('آ') and ' ' not in k and '-' not in k and re.match(r'^[\u0600-\u06FF]+$', k))

# Filter candidates:
# Prime: in Qaumi, Urno, and UB
prime = (qaumi & ub_keys & urno) - set(alif_1000.keys())
clean_prime = []
for w in prime:
    if 2 <= len(w) <= 8 and re.match(r'^[\u0600-\u06FF]+$', w):
        if not any(sub in w for sub in ['الآ', 'الابد', 'ابوال', 'ابوتر']):
            clean_prime.append(w)

clean_prime.sort(key=lambda w: (abs(len(w) - 5), w))

# Secondary: in Qaumi and UB
sec = (qaumi & ub_keys) - set(alif_1000.keys()) - set(clean_prime)
clean_sec = []
for w in sec:
    if 2 <= len(w) <= 7 and re.match(r'^[\u0600-\u06FF]+$', w):
        if not any(sub in w for sub in ['الآ', 'الابد', 'ابوال', 'ابوتر']):
            clean_sec.append(w)

clean_sec.sort(key=lambda w: (abs(len(w) - 5), w))

target_total = 2400
needed = target_total - len(alif_1000)
selected_1400 = clean_prime + clean_sec[:needed - len(clean_prime)]
assert len(selected_1400) == needed, f"Expected {needed}, got {len(selected_1400)}"

# Assemble total 2400 words
total_2400 = dict(alif_1000)
for w in selected_1400:
    m = ub[w].strip()
    m = re.sub(r'[,،;\s]+$', '', m)
    total_2400[w] = m

print(f"Total entries combined: {len(total_2400)}")
assert len(total_2400) == target_total

# Strict verification
pure_urdu = re.compile(r'^[\u0600-\u06FF]+$')
for w, m in total_2400.items():
    assert w.startswith('ا') and not w.startswith('آ'), f"Word {w} does not start with regular Alif"
    assert ' ' not in w, f"Word {w} contains space"
    assert '-' not in w, f"Word {w} contains hyphen"
    assert '\u200c' not in w, f"Word {w} contains ZWNJ"
    assert pure_urdu.match(w), f"Word {w} contains non-Urdu characters"
    assert len(m.strip()) > 0, f"Word {w} has empty translation"

print("Strict verification: ALL 2,400 WORDS ARE 100% PURE SINGLE WORDS!")

# Collation sorting
urdu_alphabet = [
    'آ', 'ا', 'ب', 'پ', 'ت', 'ٹ', 'ث', 'ج', 'چ', 'ح', 'خ',
    'د', 'ڈ', 'ذ', 'ر', 'ڑ', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض',
    'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن',
    'ں', 'و', 'ہ', 'ھ', 'ء', 'ی', 'ئ', 'ے'
]
urdu_rank = {ch: i for i, ch in enumerate(urdu_alphabet)}

def urdu_sort_key(word):
    return [urdu_rank.get(ch, 999) for ch in word]

sorted_keys = sorted(total_2400.keys(), key=urdu_sort_key)
sorted_2400_alif = {k: total_2400[k] for k in sorted_keys}

# 1. Save verified_alif.json
with open('verified_alif.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_2400_alif, f, ensure_ascii=False, indent=2)
print("Saved verified_alif.json with exactly 2,400 pure single words!")

# 2. Merge with verified_alif_madd.json (581 words) into verified_words.json
with open('verified_alif_madd.json', 'r', encoding='utf-8') as f:
    alif_madd = json.load(f)

cumulative_dict = {}
for k in sorted(alif_madd.keys(), key=urdu_sort_key):
    cumulative_dict[k] = alif_madd[k]

for k in sorted_keys:
    cumulative_dict[k] = sorted_2400_alif[k]

total_all = len(cumulative_dict)
print(f"Total cumulative verified words: {total_all} (581 Alif-Madd + 2,400 Alif)")

# Save verified_words.json
with open('verified_words.json', 'w', encoding='utf-8') as f:
    json.dump(cumulative_dict, f, ensure_ascii=False, indent=2)
print("Saved verified_words.json successfully.")

# 3. Write words.js
js_words = [[k, val] for k, val in cumulative_dict.items()]
words_js_content = 'window.RAW_WORDS = ' + json.dumps(js_words, ensure_ascii=False) + ';\nif (window.onWordsLoaded) { window.onWordsLoaded(); }\n'
with open('words.js', 'w', encoding='utf-8') as f:
    f.write(words_js_content)
print("Saved words.js successfully.")

# 4. Update index.html INITIAL_WORDS (top 50)
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

initial_50 = js_words[:50]
initial_js = 'const INITIAL_WORDS = ' + json.dumps(initial_50, ensure_ascii=False) + ';'
new_html = re.sub(r'const INITIAL_WORDS = \[.*?\];', initial_js, html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Updated index.html INITIAL_WORDS successfully.")

# 5. Bump sw.js cache to v10
with open('sw.js', 'r', encoding='utf-8') as f:
    sw = f.read()
new_sw = re.sub(r"const CACHE_NAME = 'hubban-lughat-v\d+';", "const CACHE_NAME = 'hubban-lughat-v10';", sw)
with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(new_sw)
print("Bumped sw.js cache to hubban-lughat-v10.")

print("\n--- SUMMARY ---")
print(f"Alif words: {len(sorted_2400_alif)}")
print(f"Cumulative total: {total_all}")
print(f"1st Alif: {sorted_keys[0]} -> {sorted_2400_alif[sorted_keys[0]]}")
print(f"1200th Alif: {sorted_keys[1199]} -> {sorted_2400_alif[sorted_keys[1199]]}")
print(f"2400th Alif: {sorted_keys[-1]} -> {sorted_2400_alif[sorted_keys[-1]]}")
