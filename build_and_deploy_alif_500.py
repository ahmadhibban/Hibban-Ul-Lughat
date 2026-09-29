# -*- coding: utf-8 -*-
import sqlite3, json, re

# 1. Existing verified 247 valid words
alif = json.load(open('verified_alif.json', 'r', encoding='utf-8'))
valid_existing = {
    k: v.strip() for k, v in alif.items() 
    if k.startswith('ا') and not k.startswith('آ') 
    and ' ' not in k and '-' not in k and '\u200c' not in k 
    and re.match(r'^[\u0600-\u06FF]+$', k) and v.strip()
}
print(f'Starting with existing valid Alif words: {len(valid_existing)}')

# 2. Curated corrections dictionary for high-frequency fundamental words
corrections = {
    'اب': 'এখন, এই মুহূর্তে, বর্তমান সময়ে, আজকাল',
    'اس': 'এই, এটি, এটা, এতৎ (নিকটবর্তী নির্দেশক)',
    'اسے': 'তাকে, তাহাকে, একে, এটিকে',
    'اسی': 'এই, এটিই, এই ব্যক্তিটিই / আশি (৮০)',
    'اگر': 'যদি, যদ্যপি, যদিচ / আগর কাঠ',
    'الگ': 'আলাদা, পৃথক, ভিন্ন, স্বতন্ত্র, বিশ্লিষ্ট',
    'الٹ': 'উল্টো, বিপরীত, প্রতিকূল, বিপরীতমুখী',
    'الٹا': 'উল্টো, বিপরীত, অধোমুখ, অবিকল উল্টানো',
    'الٹی': 'বমি, উদ্গিরণ / উল্টো (স্ত্রীলিঙ্গ)',
    'الٹنا': 'উল্টানো, উল্টে দেওয়া, উপুড় করা, ওলটপালট করা',
    'اٹل': 'অটল, অনড়, স্থির, অবিচল, অকাট্য',
    'اٹوٹ': 'অটুট, অভঙ্গুর, অবিভাজ্য, মজবুত, সুদৃঢ়',
    'اٹکنا': 'আটকে যাওয়া, ঠেকে যাওয়া, বাধাগ্রস্ত হওয়া',
    'اٹھنا': 'ওঠা, জেগে ওঠা, দাঁড়ানো, উত্থিত হওয়া',
    'اٹھانا': 'তোলা, উঠানো, উত্তোলন করা, জাগানো',
    'اچھাল': 'লাফ, লম্ফন, উচ্ছ্বাস, ছিটকে ওঠা',
    'اچھلنا': 'লাফানো, ছিটকে ওঠা, নৃত্য করা',
    'اچھا': 'ভালো, উত্তম, চমৎকার, সুন্দর, বেশ',
    'اچھے': 'ভালো (বহুবচন), উত্তম ব্যক্তিবর্গ',
    'اچھی': 'ভালো (স্ত্রীলিঙ্গ), সুশীলা, সুন্দর',
    'اچھائی': 'ভালোত্ব, সততা, পুণ্য, মঙ্গল, কল্যাণ',
    'اچانک': 'হঠাৎ, অকস্মাৎ, আচমকা, অপ্রত্যাশিতভাবে',
    'امی': 'মা, আম্মা, জননী / নিরক্ষর ব্যক্তি (উম্মী)',
    'انچ': 'ইঞ্চি (এক ফুটের বারো ভাগের এক ভাগ)',
    'انگوٹھا': 'বৃদ্ধাঙ্গুলি, বুড়ো আঙুল, হাতের বা পায়ের বুড়ো আঙুল',
    'اونچا': 'উঁচু, উচ্চ, উন্নত, সমুচ্চ, দীর্ঘকায়',
    'اونچائی': 'উচ্চতা, খাড়াই, সমুন্নতি, বিস্তার',
    'اوپر': 'উপরে, ঊর্ধ্বভাগে, ওপর, উপরিভাগে',
    'اوڑھنا': 'গায়ে জড়ানো, চাদর ঢাকা, পরিধান করা',
    'اور': 'এবং, ও, আর, অধিকন্তু, তাছাড়া',
    'اوس': 'শিশির, নীহার, শিশিরবিন্দু, কুয়াশাকণা',
    'اڑنا': 'ওড়া, উড়ে যাওয়া, শূন্যে বিচরণ করা',
    'اوسط': 'গড়, গড়পড়তা, মধ্যবর্তী, মাঝামাঝি মান',
    'اجر': 'প্রতিদান, সওয়াব, পারিশ্রমিক, বিনিময়, পুরস্কার',
    'اجتماع': 'সমাবেশ, সম্মেলন, জমায়েত, মিলন, একত্র হওয়া',
    'اجتماعی': 'সম্মিলিত, সমষ্টিগত, যৌথ, সামাজিক',
    'اجتناব': 'পরিহার, বর্জন, বিরত থাকা, সংযম',
    'احاطہ': 'সীমানা, চত্বর, প্রাচীরঘেরা স্থান, ঘের',
    'احساسات': 'অনুভূতিসমূহ, আবেগ, ভাবাবেগ, সংবেদন',
    'احسان': 'উপকার, অনুগ্রহ, বদান্যতা, দয়া',
    'احسانمند': 'কৃতজ্ঞ, চিরকৃতজ্ঞ, ঋণী, বাধিত',
    'احترام': 'শ্রদ্ধা, সম্মান, মর্যাদা, তাযিম',
    'احتیاط': 'সতর্কতা, সাবধানতা, পরিমিতিবোধ',
    'احتجاج': 'প্রতিবাদ, বিক্ষোভ, আপত্তি জ্ঞাপন',
    'احتساب': 'জবাবদিহিতা, হিসাব নিরীক্ষা, আত্মশুদ্ধি',
    'احمق': 'বোকা, নির্বোধ, মূর্খ, অজ্ঞ',
    'احوال': 'অবস্থা, পরিস্থিতি, বৃত্তান্ত, হালচাল',
    'اخبار': 'সংবাদপত্র, পত্রিকা, খবরসমূহ, সংবাদ',
    'اخراجات': 'ব্যয়সমূহ, খরচপাতি, বাজেটের ব্যয়',
    'اختیار': 'ক্ষমতা, কর্তৃত্ব, নিয়ন্ত্রণ, স্বাধীনতা, অধিকার',
    'اختیارات': 'ক্ষমতাসমূহ, অধিকারসমূহ, কর্তৃত্ব',
    'اخلاق': 'চরিত্র, স্বভাব, নৈতিকতা, সদ্ব্যবহার',
    'اخلاقی': 'নৈতিক, চরিত্রগত, নীতিসংক্রান্ত',
    'اخلاقیات': 'নীতিশাস্ত্র, নীতিবিজ্ঞান, নৈতিক আদর্শ',
    'اخلاص': 'আন্তরিকতা, নিষ্ঠা, বিশুদ্ধচিত্ততা, অকপটতা',
    'اخروٹ': 'আখরোট (পুষ্টিকর বাদাম ফল ও গাছ)',
    'اختتام': 'সমাপ্তি, অবসান, শেষ, ইতি',
    'اختتامی': 'সমাপনী, সমাপ্তিসূচক, অন্তিম',
    'انا': 'অহং, অহংকার, আত্মমর্যাদা, আত্মবোধ / আনা (মুদ্রার ষোল ভাগের এক ভাগ)',
    'الف': 'উর্দু বর্ণমালার প্রথম হরফ (আলিফ), শুরু, সূচনা',
    'اتالیق': 'শিক্ষক, গৃহশিক্ষক, অভিভাবক, নির্দেশক',
    'اتارنا': 'নামানো, নামিয়ে আনা, অবতীর্ণ করা, পরিধানমুক্ত করা',
    'اجوائن': 'জোয়ান, জওয়াইন (সুগন্ধি ও ঔষধি মসলাবীজ)',
    'اکٹھা': 'একত্রিত, সংগৃহীত, পুঞ্জীভূত, একজায়গায় জড়ো করা',
    'اٹکنا': 'আটকে যাওয়া, ঠেকে যাওয়া, বাধাগ্রস্ত হওয়া',
    'اونی': 'পশমি, উলের তৈরি, উষ্ণ পশমের বস্ত্র',
    'اگست': 'আগস্ট মাস (ইংরেজি বর্ষপঞ্জির অষ্টম মাস)',
    'السی': 'তিসি, তিসি গাছ, তিসির বীজ',
    'اگلے': 'পরবর্তী, আগামী, সম্মুখবর্তী',
    'امبر': 'আকাশ, গগন, আসমান / অম্বর (বস্ত্র)'
}

# 3. Urno, Qaumi, Nerdcats candidate pools
conn = sqlite3.connect('databases/Offline_Urdu_to_Urdu_Lughat_urno_dict.db')
c = conn.cursor()
c.execute("SELECT word FROM urdu WHERE word LIKE 'ا%';")
urno_words = set(r[0].strip() for r in c.fetchall() if r[0] and not r[0].startswith('آ') and ' ' not in r[0].strip() and '-' not in r[0].strip())
conn.close()

conn = sqlite3.connect('databases/Offline_Urdu_to_Urdu_Lughat_urdu_dict.db')
c = conn.cursor()
c.execute("SELECT word FROM contents WHERE word LIKE 'ا%';")
qaumi_words = set(r[0].strip() for r in c.fetchall() if r[0] and not r[0].startswith('آ') and ' ' not in r[0].strip() and '-' not in r[0].strip())
conn.close()

conn = sqlite3.connect('databases/Nerdcats_English_Urdu_Dictionary.db')
c = conn.cursor()
c.execute("SELECT fr FROM word WHERE fr LIKE 'ا%';")
nerdcats_words = set()
for r in c.fetchall():
    for part in re.split(r'[,،;\n]+', r[0]):
        w = part.strip()
        if w.startswith('ا') and not w.startswith('آ') and ' ' not in w and '-' not in w:
            nerdcats_words.add(w)
conn.close()

ub = json.load(open('urdu_bangla.json', 'r', encoding='utf-8'))
candidate_pool = (qaumi_words & set(ub.keys()) & (urno_words | nerdcats_words)) - set(valid_existing.keys())
clean_pool = [w for w in candidate_pool if re.match(r'^[\u0600-\u06FF]+$', w) and len(w) >= 2]

def score_w(w):
    s = 0
    if w in corrections: s += 50
    if w in nerdcats_words: s += 10
    if w in urno_words: s += 5
    s += max(0, 8 - len(w))
    return s

clean_pool.sort(key=score_w, reverse=True)
needed_count = 500 - len(valid_existing)
selected_253 = clean_pool[:needed_count]

combined_500 = dict(valid_existing)
for w in selected_253:
    if w in corrections:
        combined_500[w] = corrections[w]
    else:
        m = ub[w].strip()
        m = re.sub(r'[,،;\s]+$', '', m)
        combined_500[w] = m

print(f"Total entries combined: {len(combined_500)}")
assert len(combined_500) == 500, f"Expected 500 words, got {len(combined_500)}"

# Strict validation
pure_urdu = re.compile(r'^[\u0600-\u06FF]+$')
for w, m in combined_500.items():
    assert w.startswith('ا') and not w.startswith('آ'), f"Word {w} does not start with regular Alif"
    assert ' ' not in w, f"Word {w} contains space"
    assert '-' not in w, f"Word {w} contains hyphen"
    assert '\u200c' not in w, f"Word {w} contains ZWNJ"
    assert pure_urdu.match(w), f"Word {w} contains non-Urdu characters"
    assert len(m.strip()) > 0, f"Word {w} has empty translation"

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

sorted_keys = sorted(combined_500.keys(), key=urdu_sort_key)
sorted_500 = {k: combined_500[k] for k in sorted_keys}

# Save verified_alif.json
with open('verified_alif.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_500, f, ensure_ascii=False, indent=2)

print("Saved verified_alif.json with exactly 500 pure single words!")
print(f"First word: {sorted_keys[0]} -> {sorted_500[sorted_keys[0]]}")
print(f"250th word: {sorted_keys[249]} -> {sorted_500[sorted_keys[249]]}")
print(f"500th word: {sorted_keys[-1]} -> {sorted_500[sorted_keys[-1]]}")
