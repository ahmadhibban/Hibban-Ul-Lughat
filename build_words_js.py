import json, os

print("Reading verified_words.json...")
with open('verified_words.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

print(f"Total words: {len(master)}")

raw_tuples = []
for k, v in master.items():
    raw_tuples.append([
        k,
        v.get('bn', ''),
        v.get('ro', ''),
        v.get('tk', k),
        v.get('ud', []),
        v.get('hi', '')
    ])

print("Writing words.js...")
with open('words.js', 'w', encoding='utf-8') as f:
    f.write("window.RAW_WORDS = ")
    json.dump(raw_tuples, f, ensure_ascii=False, separators=(',', ':'))
    f.write(";\nif (typeof window.onWordsLoaded === 'function') { window.onWordsLoaded(); }\n")

words_js_size = os.path.getsize('words.js') / (1024 * 1024)
print(f"words.js written successfully! Size: {words_js_size:.2f} MB")

# Extract 1,000 representative words across all letters for instant 0ms first launch
# Distribute ~28 words per letter across 35 letters
letters_map = {}
for item in raw_tuples:
    w = item[0]
    first_char = w[0]
    if first_char not in letters_map:
        letters_map[first_char] = []
    letters_map[first_char].append(item)

initial_1000 = []
# Pick ~28 words from each letter
for l_char, l_words in letters_map.items():
    pick_count = min(len(l_words), 28)
    initial_1000.extend(l_words[:pick_count])

# If less than 1000, pad from top
if len(initial_1000) < 1000:
    remaining_needed = 1000 - len(initial_1000)
    seen = {x[0] for x in initial_1000}
    for item in raw_tuples:
        if item[0] not in seen:
            initial_1000.append(item)
            if len(initial_1000) >= 1000:
                break

print(f"Selected {len(initial_1000)} initial core words covering all {len(letters_map)} letters.")

with open('initial_1000.json', 'w', encoding='utf-8') as f:
    json.dump(initial_1000, f, ensure_ascii=False, separators=(',', ':'))

init_size_kb = os.path.getsize('initial_1000.json') / 1024
print(f"initial_1000.json size: {init_size_kb:.2f} KB")
