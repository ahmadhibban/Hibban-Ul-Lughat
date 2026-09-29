# -*- coding: utf-8 -*-
import json, re

# Prevalent 555 words list (Tier 1 & Tier 2 words, purged of all Tier 3 archaic/rare words)
raw_555_str = '''آب, آبا, آباد, آبادان, آبادانی, آبادکار, آبادکاری, آبادی, آبادیات, آبادیاتی, آباء, آبائی, آبائیت, آبپاشی, آبچین, آبخور, آبخورا, آبخوری, آبدار, آبداری, آبدان, آبدست, آبدستگاہ, آبدوز, آبدیدہ, آبرو, آبروبخش, آبروریزی, آبرومند, آبرومندانہ, آبرومندی, آبزی, آبسال, آبستگی, آبستن, آبستنی, آبستہ, آبکار, آبکاری, آبگون, آبگونہ, آبگینہ, آبلہ, آبنائے, آبنوس, آبنوسی, آبھا, آبھاس, آبھرن, آبھوشن, آبھیر, آبی, آبیات, آبیاتی, آبیار, آبیاری, آبیانہ, آبیدہ, آبشار, آبشاردار, آبشورہ, آپ, آپا, آپار, آپاڑ, آپت, آپتکال, آپدا, آپس, آپسی, آپسیئت, آپگا, آپل, آپلاؤ, آپنا, آپورتی, آپھا, آپھرا, آپھلنا, آپی, آپیتی, آت, آتا, آتم, آتما, آتمک, آتو, آتش, آتشبار, آتشباز, آتشبازی, آتشدان, آتشزدگی, آتشزنی, آتشک, آتشکدہ, آتشکیا, آتشگیر, آتشناک, آتشی, آتشیں, آٹا, آٹنا, آٹھ, آٹھواں, آٹھوں, آثار, آثاریات, آثاریاتی, آثام, آثم, آج, آجا, آجر, آجرانہ, آجری, آجکل, آجکلیا, آجل, آجیل, آچار, آچاری, آچاریہ, آچرن, آچمن, آحاد, آخ, آخار, آختہ, آخذ, آخذہ, آخر, آخرالامر, آخرت, آخرکار, آخری, آخریات, آخریں, آخرش, آخون, آخوند, آخوندانہ, آخوندزادہ, آخوندی, آد, آدا, آداب, آدان, آدر, آدرش, آدرشک, آدرشن, آدرشی, آدم, آدمخور, آدمزاد, آدمگری, آدمی, آدمیت, آدمیئت, آدمشناسی, آدھ, آدھا, آدھار, آدھارمک, آدھارنا, آدھاری, آدھنک, آدھی, آدھیاتمک, آدھیڑ, آدھین, آدھینی, آدی, آدیا, آدینہ, آدیش, آڈی, آذار, آذان, آذر, آذرخش, آذرفشاں, آذری, آرا, آرادھن, آرادھنا, آراستگی, آراستہ, آراضی, آرام, آرامستان, آرامی, آرامیدہ, آرامش, آراء, آرائی, آرائش, آرائشی, آرپار, آرتی, آرجو, آرچ, آرد, آردر, آرزو, آرزوبخش, آرزومند, آرزومندانہ, آرزومندی, آرسی, آرمبھ, آرمیدہ, آروپ, آروغ, آروی, آرہ, آری, آریائی, آرین, آریہ, آڑ, آڑا, آڑبند, آڑت, آڑتی, آڑو, آڑھت, آڑھتی, آز, آزاد, آزادانہ, آزادخیال, آزادخیالی, آزادگی, آزادمنش, آزادمنشی, آزادہ, آزادی, آزار, آزاردہ, آزاردہی, آزارندہ, آزاری, آزاریدہ, آزر, آزرخش, آزردگی, آزردہ, آزردہخاطر, آزردہدل, آزرم, آزمانا, آزمائندہ, آزمائش, آزمائشی, آزمند, آزمندی, آزمودگی, آزمودہ, آزمودہکار, آزمودہکاری, آژنگ, آس, آسا, آسامی, آسان, آسانی, آسائش, آسائشی, آست, آستا, آستان, آستانہ, آستاں, آستر, آسترکاری, آستھا, آستین, آستینی, آسرا, آسمان, آسمانرنگ, آسمانی, آسن, آسنی, آسواد, آسوج, آسودگی, آسودہ, آسودہحال, آسودہحالی, آسیا, آسیاب, آسیابانی, آسیب, آسیبزدہ, آسیبی, آصف, آغا, آغاز, آغازین, آغوش, آفات, آفاق, آفاقی, آفاقیت, آفت, آفتاب, آفتابرو, آفتابہ, آفتابی, آفترسیدہ, آفتزدہ, آفریدگار, آفریدہ, آفریدی, آفرین, آفرینخوان, آفرینخوانی, آفرینندہ, آفرینش, آفریں, آقا, آقائی, آقائیت, آک, آکار, آکانکشا, آکاش, آکاشوانی, آکاشی, آکس, آکل, آکیرن, آگ, آگار, آگامی, آگاہ, آگاہانہ, آگاہی, آگبوٹ, آگرو, آگرہ, آگمن, آگمی, آگندھ, آگوان, آگوانی, آگہی, آگین, آگے, آل, آلا, آلاپ, آلاپنا, آلات, آلاتی, آلاف, آلام, آلائی, آلائش, آلپین, آلتا, آلتی, آلسی, آلماری, آلنگن, آلو, آلوبخارا, آلوچہ, آلودگی, آلودہ, آلودہخاطر, آلودہدامن, آلہ, آلہکار, آلیشان, آم, آماج, آماجگاہ, آمادگی, آمادہ, آمار, آمارہ, آماس, آماسیدہ, آمد, آمدنی, آمدورفت, آمدوشد, آمدہ, آمر, آمرانہ, آمرزگار, آمرزگاری, آمرزش, آمریت, آمریتپسند, آملا, آملہ, آمن, آمنہ, آموختہ, آموز, آموزگار, آموزگاری, آموزندہ, آموزش, آمیختگی, آمیختہ, آمیز, آمیزگار, آمیزگاری, آمیزہ, آمیزش, آمین, آن, آنا, آنبان, آنت, آنترک, آنٹھ, آنٹھی, آنٹی, آنجن, آنجنا, آنجہانی, آنچ, آنچر, آنچل, آنچلا, آندولن, آندھرا, آندھی, آندھیر, آندھیوار, آنسو, آنکڑا, آنکڑی, آنکس, آنکھ, آنکھمچولی, آنگن, آنمات, آنند, آنندت, آنندمئے, آنندورتی, آنورودھ, آنوسنگک, آنول, آنولہ, آنی, آوا, آوارگی, آوارہ, آوارہگرد, آوارہگردی, آواز, آوازگی, آوازہ, آوازہخوان, آواگون, آوان, آواہن, آوائل, آوردہ, آورندہ, آوری, آویز, آویزاں, آویزہ, آویزش, آوشیک, آوشیکتا, آہ, آہا, آہٹ, آہستگی, آہستہ, آہستہباز, آہستہخوان, آہستہخوانی, آہستہرو, آہستہروی, آہستہقدم, آہسرد, آہل, آہن, آہنگ, آہنگدار, آہنگر, آہنگری, آہنی, آہو, آہوان, آہوتی, آہوگیر, آہونین, آیات, آیام, آیان, آیت, آش, آؤ, آشا, آشام, آشامی, آشپز, آشپزی, آشتی, آشخانہ, آشرم, آئسہ, آشفتگی, آشفتہ, آشفتہحال, آشفتہدل, آشفتہسر, آشکار, آشکارا, آشکارائی, آشکاری, آئمہ, آشنا, آشنائی, آئند, آئندگاں, آئندوروند, آئندہ, آشوب, آشوبچشم, آشوبزدہ, آئی, آشیان, آشیانہ, آشیاں, آشیس, آئین, آئینبند, آئینپرور, آئیندان, آئیننامہ, آئینہ, آئینہخانہ, آئینہدار, آئینہداری, آئینہرو, آئینہساز, آئینہسازی, آئینی, آئینیت, آئینشکنی, آئیے'''

words_list = [w.strip() for w in raw_555_str.split(',') if w.strip()]
assert len(words_list) == 555, f"Expected 555 words, got {len(words_list)}"

# Load current verified words
with open('verified_words.json', 'r', encoding='utf-8') as f:
    v = json.load(f)

# Extract only prevalent words
prevalent_dict = {}
for w in words_list:
    assert w in v, f"Word {w} not found in verified_words.json!"
    prevalent_dict[w] = v[w]

print(f"Extracted {len(prevalent_dict)} prevalent words.")

# Strict validation
pure_urdu_pattern = re.compile(r'^[\u0600-\u06FF]+$')
for w, meaning in prevalent_dict.items():
    assert w.startswith('آ'), f"Word {w} does not start with آ"
    assert ' ' not in w, f"Word {w} contains space!"
    assert '-' not in w, f"Word {w} contains hyphen!"
    assert '\u200c' not in w, f"Word {w} contains ZWNJ!"
    assert pure_urdu_pattern.match(w), f"Word {w} has non-Urdu characters!"
    assert len(meaning.strip()) > 0, f"Word {w} has empty translation!"

print("All 555 words passed strict validation (pure Urdu characters, zero spaces, non-empty meanings).")

# Sort in Urdu alphabetical order
urdu_alphabet = [
    'آ', 'ا', 'ب', 'پ', 'ت', 'ٹ', 'ث', 'ج', 'چ', 'ح', 'خ',
    'د', 'ڈ', 'ذ', 'ر', 'ڑ', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض',
    'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن',
    'ں', 'و', 'ہ', 'ھ', 'ء', 'ی', 'ئ', 'ے'
]
urdu_rank = {ch: i for i, ch in enumerate(urdu_alphabet)}

def urdu_sort_key(word):
    return [urdu_rank.get(ch, 999) for ch in word]

sorted_keys = sorted(prevalent_dict.keys(), key=urdu_sort_key)
sorted_555_dict = {k: prevalent_dict[k] for k in sorted_keys}

# 1. Save verified_words.json
with open('verified_words.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_555_dict, f, ensure_ascii=False, indent=2)
print("Saved 555 verified words to verified_words.json")

# 2. Write words.js
js_words_list = [[k, val] for k, val in sorted_555_dict.items()]
words_js_content = 'window.RAW_WORDS = ' + json.dumps(js_words_list, ensure_ascii=False) + ';\nif (window.onWordsLoaded) { window.onWordsLoaded(); }\n'
with open('words.js', 'w', encoding='utf-8') as f:
    f.write(words_js_content)
print("Saved words.js successfully.")

# 3. Update index.html INITIAL_WORDS (top 50)
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

initial_50 = js_words_list[:50]
initial_js = 'const INITIAL_WORDS = ' + json.dumps(initial_50, ensure_ascii=False) + ';'
new_html = re.sub(r'const INITIAL_WORDS = \[.*?\];', initial_js, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Updated index.html INITIAL_WORDS with top 50 prevalent words.")

# 4. Bump sw.js cache to v7
with open('sw.js', 'r', encoding='utf-8') as f:
    sw = f.read()
new_sw = re.sub(r"const CACHE_NAME = 'hubban-lughat-v\d+';", "const CACHE_NAME = 'hubban-lughat-v7';", sw)
with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(new_sw)
print("Bumped sw.js cache to hubban-lughat-v7.")

print("\n=== SUMMARY ===")
print(f"Total entries: {len(sorted_555_dict)}")
print(f"First word: {js_words_list[0]}")
print(f"50th word: {js_words_list[49]}")
print(f"250th word: {js_words_list[249]}")
print(f"555th word: {js_words_list[-1]}")
