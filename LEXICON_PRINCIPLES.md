# Hibban-Ul-Lughat (حبان اللغات): 32,000 Standard Urdu-Bangla Single-Word Compilation & Curation Principles
**A Comprehensive Methodology & Lexical Curation Guidelines for Urdu-Bangla Lexicography**

---

## 1. Introduction
In the **Hibban-Ul-Lughat** (Urdu-to-Bangla modern offline dictionary and Progressive Web Application) project, a total of **32,000 pure, contemporary, and standardized single-word Urdu entries** were compiled and curated by analyzing 11 extensive databases, including Pakistan's National Urdu Dictionary Board (*Qaumi Lughat*) and Kaikki Wiktionary.

This compilation eliminates distortions caused by machine translation and polysemous English homonyms, providing precise, natural, and multifaceted Bengali definitions for every entry. This document sets out in detail the **5 core principles and implementation guidelines** followed in selecting, refining, verifying, and ensuring the quality of these 32,000 words.

---

## 2. Principle 1: Orthographic Purity & Single-Word Principle (Monolexemic Strictness)

### 2.1. Monolexemic Strictness
- Every headword in the lexicon must be a single, standalone word.
- No multi-word compounds containing spaces (`\u0020`), hyphens (`-`), underscores, or zero-width non-joiners (`\u200c`) are permitted as headwords.
- **Regex Validation:** Every word strictly adheres to the regex pattern `^[\u0600-\u06FF]+$`. English letters, digits, or extraneous symbols are strictly forbidden.
- **Minimum Length:** Each entry must have a minimum length of 2 characters ($\text{Length} \ge 2$). Isolated single letters or incomplete diacritical marks are excluded.

### 2.2. Exclusion of Multi-word Compounds & Idioms
- Compound verbs in Urdu grammar (e.g., `کر دینا`, `ہو جانا`, `کھا لینا`) have been excluded.
- Compound phrases and *Izafat* constructions (e.g., `اہل زبان`, `آب و ہوا`, `دست بدست`) are omitted under the single-word rule.
- Epistolary greetings and fixed idioms (e.g., `والسلام`, `فی امان اللہ`, `با اندازہ`) have been pruned.
- Artificially prefixed fragments (e.g., `الآ`, `الابد`, `ابوال`, `ابوتر`) have been removed.

---

## 3. Principle 2: Currency, Prevalence & Authority Principle

From the vast repository of Urdu literature, only words that are recognized, active, and prevalent in contemporary society, literature, academia, media, and everyday life were selected.

### 3.1. Multi-Tier Lexical Cross-Verification
1. **Tier 1 (National Authority):** The 24-volume monumental and authoritative **Qaumi Lughat (102 MB, 165,995 entries)** published by the National Urdu Dictionary Board of Pakistan. Out of 32,000 compiled words, **98.7% (31,578 words)** are directly authenticated by the Qaumi Lughat.
2. **Tier 2 (Contemporary Active Usage):** The modern 21st-century spoken and standard lexicon **Offline Urno (31,363 single words)**. **64% (20,484 words)** of the compiled words are verified in Urno.
3. **Tier 3 (Spoken & Practical Core):** Contemporary practical educational lexicons from **Nerdcats English-Urdu & Hindi-Urdu**, cross-verifying over 5,700 high-frequency conversational words.
4. **Auxiliary Validation:** Kaikki Wiktionary Urdu dump (`kaikki_urdu.jsonl` - 9,183 words) for confirming parts of speech and primary lexical classifications.

### 3.2. Purging Archaic and Obsolete Entries
- Words marked in the Qaumi Lughat as **`متروک اللفظ`** (obsolete word) or **`متروک الاستعمال`** (disused in contemporary language) were purged.
- **Distinguishing Historical Etymology vs. Obsolete Usage:** Living words (e.g., `اداس`, `افسوس`, `الٹ`, `افلاطون`, `اجاڑ`, `اساطیر`) whose etymological notes reference `قدیم` (archaic origin) but remain fully active in modern speech were preserved.
- Obscure medieval Persian and Arabic jargon with no modern relevance or Bengali equivalent were eliminated (23,711 such entries filtered out during database processing).
- Obsolete Sanskrit or Greek adaptations (e.g., `اتبکتاد`, `اسپرشیہ`, `اہمجن`, `گما`) were excluded.

---

## 4. Principle 3: Lemma Priority & Alphabetical Collation Order

### 4.1. Root Lemma Priority
- Root forms (*mufrad/masdar*) are prioritized over inflected grammatical variants or pluralizations:
  - Plural inflections (e.g., `کتابوں`, `باتوں`, `گھروں`) are omitted in favor of the base singular lemma (`کتاب`, `بات`, `گھر`).
  - Inflected verbal conjugations (e.g., `کرتے`, `ہوتے`, `تھی`) are omitted in favor of the base infinitive root (`کرنا`, `ہونا`).
  - Redundant gender-inflected duplicate entries (e.g., `اکٹھی` vs `اکٹھا`) are regularized.

### 4.2. Urdu Alphabetical Collation Order
The 32,000 words are systematically collated across all 35 letters of the Urdu alphabet proportional to literary frequency:

| # | Letter | Name | Entry Count | Morphological & Collation Characteristics |
|---|:---:|---|:---:|---|
| 01 | **آ** | Alif Madd | 581 | Words starting with long open back vowels |
| 02 | **ا** | Alif | 2,633 | High-frequency primary Alif-initial root words |
| 03 | **ب** | Be | 2,500 | Bilabial stop 'Be' class |
| 04 | **پ** | Pe | 2,130 | Urdu, Persian, and Indo-Aryan 'Pe' class |
| 05 | **ت** | Te | 2,415 | Dental 'Te' category |
| 06 | **ٹ** | Te-Dal | 487 | Retroflex 'Ta' class |
| 07 | **ث** | Se | 95 | Arabic-origin 'Tha' entries |
| 08 | **ج** | Jim | 1,198 | Voiced affricate 'Jim' entries |
| 09 | **چ** | Che | 1,170 | Voiceless affricate 'Che' entries |
| 10 | **ح** | He-Bari | 489 | Pharyngeal 'Ha' entries |
| 11 | **خ** | Khe | 692 | Velar fricative 'Kha' entries |
| 12 | **د** | Dal | 1,110 | Dental 'Dal' entries |
| 13 | **ڈ** | Dal-Re | 401 | Retroflex 'Dal' entries |
| 14 | **ذ** | Zal | 118 | Arabic-origin 'Zal' entries |
| 15 | **ر** | Re | 934 | Alveolar tap 'Re' entries |
| 16 | **ڑ** | Re-Ar | 0 | **Urdu Grammatical Rule:** No Urdu word begins with the retroflex flap 'Rra' |
| 17 | **ز** | Ze | 335 | Voiced sibilant 'Ze' entries |
| 18 | **ژ** | Zhe | 11 | Persian-origin voiced postalveolar fricative 'Zhe' entries |
| 19 | **س** | Sin | 1,516 | Voiceless alveolar sibilant 'Sin' entries |
| 20 | **ش** | Shin | 453 | Voiceless postalveolar fricative 'Shin' entries |
| 21 | **ص** | Swad | 189 | Emphatic 'Swad' entries |
| 22 | **ض** | Zwad | 94 | Emphatic 'Zwad' entries |
| 23 | **ط** | Toe | 278 | Emphatic 'Toe' entries |
| 24 | **ظ** | Zoe | 46 | Emphatic 'Zoe' entries |
| 25 | **ع** | Ain | 480 | Guttural 'Ain' entries |
| 26 | **غ** | Ghain | 200 | Voiced velar fricative 'Ghain' entries |
| 27 | **ف** | Fe | 489 | Labiodental 'Fe' entries |
| 28 | **ق** | Qaf | 403 | Uvular stop 'Qaf' entries |
| 29 | **ک** | Kaf | 1,594 | Velar stop 'Kaf' entries |
| 30 | **گ** | Gaf | 773 | Voiced velar stop 'Gaf' entries |
| 31 | **ل** | Lam | 705 | Lateral 'Lam' entries |
| 32 | **م** | Mim | 4,701 | Comprehensive bilabial nasal 'Mim' vocabulary |
| 33 | **ن** | Nun | 1,815 | Alveolar nasal 'Nun' entries |
| 34 | **و** | Waw | 438 | Labial-velar approximant 'Waw' entries |
| 35 | **ہ** | Chhoti-He | 381 | Glottal 'Chhoti He' entries |
| 36 | **ی** | Ye | 146 | Palatal approximant 'Ye' entries |
| **Total** | | | **32,000** | **100% Balanced & Complete Alphabetical Lexicon** |

---

## 5. Principle 4: Semantic Sanitation & Elimination of Machine-Translation Errors

This represents one of the most critical aspects of the project. Legacy raw databases generated translations through an intermediate English pivot, introducing severe semantic distortions and inappropriate mistranslations, all of which were meticulously cleaned:

### 5.1. Remediation of Polysemous English Homonyms
Due to multiple diverging meanings of intermediate English words, erroneous meanings frequently corrupted the Bengali definitions. These were identified and corrected:

| Urdu Word | Intended Meaning | Previous Machine-Generated Erroneous Meaning | Corrected Bengali Definition |
|---|---|---|---|
| **`ابا`** | Father, dad | *"ফট শব্দ, পট শব্দ, ফুৎকার, পপ"* (Eng: 'pop') | পিতা, বাবা, আব্বা, জনক |
| **`ابابیل`** | Swallow bird | *"গলাধঃকরণ, কণ্ঠনালী, গেলা, গ্রাস করা"* (Eng: 'swallow') | আবাবিল পাখি, চড়ুই সদৃশ ক্ষুদ্র পরিযায়ী পাখি |
| **`استانی`** | Female teacher | *"উপপত্নী, কত্র্রী, উপস্ত্রী, প্রতিপালিতা বেশ্যা"* (Eng: 'mistress') | শিক্ষিকা, শিক্ষাদাত্রী, ওস্তাদ নারী, গৃহশিক্ষিকা |
| **`بت` / `بتاں`** | Idol / Beloved | *"উপপত্নী, উপস্ত্রী, প্রতিপালিতা বেশ্যা"* (Eng: 'mistress/idol') | মূর্তি, প্রতিমা, ভাস্কর্য, কাব্যের রূপসী প্রিয়া |
| **`ٹانگا`** | Horse carriage (Tanga) | *"বেশ্যা, হীন ভাড়াটে লোক, যৌনসঙ্গমার্থ ভাড়া দেওয়া"* (Eng: 'hackney') | ঘোড়ার গাড়ি, টাঙ্গা গাড়ি, দুই চাকার এক্কা গাড়ি |
| **`پالک`** | Spinach / Guardian | *"গৃহিণী, উপপত্নী, উপস্ত্রী, প্রতিপালিতা বেশ্যা"* | পালং শাক, লালন-পালনকারী, পালক অভিভাবক |
| **`پلاس`** | Pliers (tool) | *"নৌকা, বেশ্যা, হীন ভাড়াটে লোক"* | প্লাস, প্লায়ার্স, তার কাটার সাঁড়াশি |
| **`تکلا`** | Spindle | *"বেশ্যালয়ের মালিকানী, কুট্নী"* (Eng: 'madam') | তাকলি, চরকার টাকু, সুতা কাটার শলাকা |
| **`چندر`** | Moon | *"আকাশকুসুম, অবসন্নভাবে চলাফেরা করা"* | চাঁদ, চন্দ্র, শশী, ইন্দু |
| **`زنجیر`** | Chain, shackles | *"দ্বীপপুঞ্জ, দ্বীপবহুল সমুদ্র, দ্বীপমালা"* (Eng: 'chain of islands') | শিকল, শৃঙ্খল, লোহার বেড়ি |
| **`مہماں`** | Guest | *"প্রচারাভিযান, অপপ্রচার, প্রোপাগান্ডা"* (Eng: 'campaign') | মেহমান, অতিথি, মেহমানদার |
| **`سویٹر`** | Sweater | *"দাবা, পাশা ইত্যাদির ছক্কা, প্রাণ ত্যাগ করা, মরা"* (Eng: 'die/dice') | সোয়েটার, শীতের পশমি পোশাক |
| **`صدمہ`** | Shock, grief | *"দাবা, পাশা ইত্যাদির ছক্কা, মরা"* | আঘাত, শোক, মানসিক আঘাত, তীব্র বেদনা |
| **`مالکن`** | Mistress of house | *"উপপত্নী, প্রণয়িনী, রক্ষিতা"* | মালকিন, গৃহকর্ত্রী, স্বত্বাধিকারিণী নারী |
| **`ابل`** | Camels | *"অংশ, অঙ্গ, পক্ষ, ভাগ, এলাকা"* | উটসমূহ, উটের পাল |
| **`ابوین`** | Parents | *"আব্বুমণ্ডলী, আব্বুগণ, সকল আব্বু"* | পিতা-মাতা, মা-বাবা, অভিভাবকদ্বয় |
| **`ابین`** | Most manifest | *"এখনমণ্ডলী, এখনগণ, সকল এখন"* (اب + ین) | অধিকতর স্পষ্ট, সুস্পষ্টতম, প্রত্যক্ষ |

### 5.2. Sanctity of Asma-ul-Husna (99 Divine Names of Allah)
Entries representing the Divine Names of Allah that suffered severe machine distortions were restored in accordance with authentic Islamic terminology:
- **`اللطیف`:** Replaced machine distortion *"swelling, bloating"* with: **পরম সূক্ষ্মদর্শী, অতিস্নেহশীল, পরম দয়ালু, মহান আল্লাহর গুণবাচক নাম** (The All-Subtle, The Most Affectionate).
- **`الغفور`:** Replaced machine distortion *"infatuated, puffing up"* with: **পরম ক্ষমাশীল, মার্জনাদানকারী, ক্ষমা প্রদর্শনকারী, মহান আল্লাহর গুণবাচক নাম** (The All-Forgiving).
- **`المحصی`:** Replaced machine distortion *"dice, dying, expiring"* with: **সর্ব হিসাবকারী, নিখুঁত গণনাকারী, সর্বসংখ্যাতত্ত্বজ্ঞানী, মহান আল্লাহর গুণবাচক নাম** (The Appraiser, The Accounter of All).
- **`القوی`:** Replaced machine distortion *"blister, unfortunate, attacking violently"* with: **মহাশক্তিমান, পরম পরাক্রমশালী, সর্বশক্তিমান, মহান আল্লাহর গুণবাচক নাম** (The All-Strong, The Omnipotent).

### 5.3. Regularization of Archaic Orthography into Modern Standard Bengali
19th-century archaic spellings and typographical artifacts from historical scanned sources were standardized into modern standard Bengali:
- `যাত্তয়া` $\rightarrow$ **যাওয়া**
- `দেত্তয়া` / `দেওযা` $\rightarrow$ **দেওয়া**
- `হত্তয়া` / `হত্তয়া` / `হোয়া` $\rightarrow$ **হওয়া**
- `লইয়া` $\rightarrow$ **নিয়ে**
- `করিয়া` $\rightarrow$ **করে**
- `বলিয়া` $\rightarrow$ **বলে**
- `হইয়া` $\rightarrow$ **হয়ে**
- `কত্র্রী` $\rightarrow$ **কর্ত্রী**
- `দু্যতি` $\rightarrow$ **দ্যুতি**

---

## 6. Principle 5: Utility, Aesthetics & Modern Web Architecture

### 6.1. High Synonym Density
- An average of **4.28 contextual Bengali synonyms** is provided per Urdu headword, empowering students, researchers, and translators to grasp exact nuances and literary connotations.

### 6.2. Clean Formatting & Punctuation
- Eliminated double commas (`,,`), trailing delimiters, spurious whitespace, and redundant synonym duplications.
- Completely free of HTML tags, stray backslashes, or unescaped characters.

### 6.3. Modern Architecture & Progressive Web App (PWA)
- **Master Data Files:** Complete synchronization between `verified_words.json`, `words.js`, and alphabetical partitions under `letters/`.
- **Service Worker Caching:** Automatic cache versioning ensures seamless offline functionality for the full 32,000-word dataset on mobile devices.
- **GitHub Pages Live Deployment:** Continuous deployment pipeline hosted directly at:  
  [https://ahmadhibban.github.io/Hibban-Ul-Lughat/](https://ahmadhibban.github.io/Hibban-Ul-Lughat/)

---

## 7. Conclusion
Through the strict adherence to these lexicographical principles, **Hibban-Ul-Lughat** stands as an authoritative, modern, reliable, and academically rigorous Urdu-to-Bangla lexicon. These principles serve as the permanent benchmark for any future expansions or lexical refinements.
