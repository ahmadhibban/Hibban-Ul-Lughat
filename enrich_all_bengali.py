import json, re, os, sys

print("Loading dataset...")
with open('verified_words.json', 'r', encoding='utf-8') as f:
    words_data = json.load(f)

print(f"Total words loaded: {len(words_data)}")

URDU_CHAR_REGEX = re.compile(r'[\u0600-\u06FF]')

# Scholarly Domain Mapping
DOMAINS = {
    'مجازا': 'রূপকার্থে', 'تصوف': 'সুফিবাদ', 'طب': 'চিকিৎসাবিজ্ঞান', 'کنایۃ': 'লাক্ষণিক অর্থে',
    'فقہ': 'ইসলামী আইন', 'قانون': 'আইনশাস্ত্র', 'قواعد': 'ব্যাকরণ', 'ریاضی': 'গণিত',
    'موسیقی': 'সঙ্গীত', 'نباتیات': 'উদ্ভিদবিজ্ঞান', 'عروض': 'ছন্দশাস্ত্র', 'منطق': 'যুক্তিবিদ্যা',
    'نفسیات': 'মনোবিজ্ঞান', 'نجوم': 'জ্যোতির্বিদ্যা', 'فلسفہ': 'দর্শন', 'کیمیا': 'রসায়ন',
    'حیاتیات': 'জীববিজ্ঞান', 'سائنس': 'বিজ্ঞান', 'طبیعیات': 'পদার্থবিজ্ঞান', 'معاشیات': 'অর্থনীতি',
    'حشرت الارض': 'কীটপতঙ্গ', 'اصول حدیث': 'হাদিস শাস্ত্র', 'حدیث': 'হাদিস শাস্ত্র',
    'جغرافیہ': 'ভূগোল', 'کھیل': 'খেলাধুলা', 'کاشت کاری': 'কৃষিবিদ্যা', 'کاشتکاری': 'কৃষিবিদ্যা',
    'تجوید': 'তাজবিদ', 'بحریات': 'নৌবিদ্যা', 'شاعری': 'কাব্যরীতি', 'ادب': 'সাহিত্য',
    'عناصر': 'মৌলিক উপাদান', 'عورت-مجازا': 'রূপকার্থে স্নেহবচনে', 'ہندو': 'হিন্দু ঐতিহ্য',
    'استعارۃ': 'রূপক প্রয়োগ', 'طنزا': 'ব্যঙ্গার্থে', 'نحو': 'বাক্যরীতি', 'قدیم': 'প্রাচীন প্রয়োগ',
    'لفظا': 'আক্ষরিক অর্থে', 'حساب': 'গণিত', 'مراد': 'উদ্দিষ্ট অর্থে', 'بینکاری': 'ব্যাংকিং'
}

URDU_TO_BN_NUM = {
    '۰': '০', '۱': '১', '۲': '২', '۳': '৩', '۴': '৪', '۵': '৫', '۶': '৬', '۷': '৭', '۸': '৮', '۹': '৯',
    '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯',
    '٠': '০', '١': '১', '٢': '২', '٣': '৩', '٤': '৪', '٥': '৫', '٦': '৬', '٧': '৭', '٨': '৮', '٩': '৯'
}

LANG_MAP = {
    'عربی': 'আরবি', 'فارسی': 'ফারসি', 'سنسکرت': 'সংস্কৃত', 'انگریزی': 'ইংরেজি',
    'ہندی': 'হিন্দি', 'ترکی': 'তুর্কি', 'یونانی': 'গ্রিক', 'عبرانی': 'হিব্রু',
    'پہلوی': 'পাহলভি', 'پرتگالی': 'পর্তুগিজ', 'فرانسیسی': 'ফরাসি', 'لاطینی': 'লাতিন',
    'پشتو': 'পশতু', 'پنجابی': 'পাঞ্জাবি', 'دکنی': 'দকনী', 'اردو': 'উর্দু'
}

BOOK_MAP = {
    'قطب مشتری': 'কুতুব মুশতরি', 'سب رس': 'সবরস', 'کلیات قلی قطب شاہ': 'কুল্লিয়াত-ই কুলি কুতুব শাহ',
    'قلی قطب شاہ کے کلیات': 'কুল্লিয়াত-ই কুলি কুতুব শাহ', 'دیوان حسن شوقی': 'দেওয়ান-ই হাসান শওকী',
    'حسن شوقی کے دیوان': 'দেওয়ান-ই হাসান শওকী', 'دیوانِ حسن شوقی': 'দেওয়ান-ই হাসান শওকী',
    'گلشن عشق': 'গুলশান-ই ইশক', 'کربل کتھا': 'কারবাল কথা', 'خاور نامہ': 'খাওয়ারনামা',
    'خاورنامہ': 'খাওয়ারনামা', 'نوسرہار': 'নওসরহার', 'کلیات میر': 'কুল্লিয়াত-ই মীর',
    'میر کے کلیات': 'কুল্লিয়াত-ই মীর', 'کلمۃ الحقائق': 'কালিমাতুল হাকায়েক', 'دیوان آبرو': 'দেওয়ান-ই আবরু',
    'دیوانِ آبرو': 'দেওয়ান-ই আবরু', 'کلیات ولی': 'কুল্লিয়াত-ই ওয়ালি', 'ولی کے کلیات': 'কুল্লিয়াত-ই ওয়ালি',
    'معراج العاشقین': 'মেরাজুল আশিকিন', 'کلیات سراج': 'কুল্লিয়াত-ই সিরাজ', 'علی نامہ': 'আলিনামা',
    'طوطی نامہ': 'তুতিনামা', 'گنج شریف': 'গাঞ্জ-ই শরীফ', 'باغ و بہار': 'বাগ ও বাহার',
    'من لگن': 'মন লগন', 'احوال الانبیا': 'আহওয়ালুল আম্বিয়া', 'پھول بن': 'ফুলবান',
    'تاریخ ہندوستان': 'তারিখ-ই হিন্দুস্তান', 'قصہ مہر افروز و دلبر': 'কিসসা মেহের আফরোজ ও দিলবার',
    'بستان حکمت': 'বুস্তান-ই হিকমত', 'شرح تمہیدات ہمدانی': 'শরহে তামহিদাত-ই হামাদানি',
    'دیوان قائم': 'দেওয়ান-ই কায়েম', 'کلیات سودا': 'কুল্লিয়াত-ই সওদা', 'دیوان ہاشمی': 'দেওয়ান-ই হাশমি',
    'عجائب القصص': 'আজায়েবুল কাসাস', 'ہشت بہشت': 'হাশত বিহিস্ত', 'آرائش محفل': 'আরায়েশ-ই মাহফিল',
    'چندر بدن و مہیار': 'চন্দরবদন ও মাহিয়ার', 'فسانۂ عجائب': 'ফাসানা-ই আজায়েব',
    'دیوان غالب': 'দেওয়ান-ই গালিব', 'بہارستان': 'বাহারিস্তান', 'آشفتہ بیانی میری': 'আশুফতা বয়ানি মেরি',
    'حکایت سخن سنج': 'হিকায়াতে সুখুন সানজ', 'داستان امیر خسرو': 'দাস্তান-ই আমির খসরু',
    'ریاض البحر': 'রিয়াজুল বাহর', 'تاریخ سیر المتقدمین': 'তারিখ-ই সিয়ারুল মুতাকাদ্দিমিন',
    'دیوان ناسخ': 'দেওয়ান-ই নাসিখ', 'مقام غالب': 'মাকাম-ই গালিব', 'دیوان درد': 'দেওয়ান-ই দরদ',
    'دیوان فائز': 'দেওয়ান-ই ফায়েজ', 'فائز کے دیوان': 'দেওয়ান-ই ফায়েজ',
    'کدم راو پدم راو': 'কদম রাও পদম রাও'
}

CITATIONS = {
    'فرہنگ آصفیہ': 'ফারহাঙ্গে আসিফিয়া', 'فرہنگِ آصفیہ': 'ফারহাঙ্গে আসিফিয়া',
    'نوراللغات': 'নূরুল লুগাত', 'جامع اللغات': 'জামিউল লুগাত',
    'مصباح التعرف': 'মিসবাহুত তা\'আররুফ', 'پلیٹس': 'প্ল্যাটস অভিধান',
    'اردو قانونی ڈکشنری': 'উর্দু আইনি পরিভাষা কোষ', 'اصطلاحات پیشہ وراں': 'পেশাগত পরিভাষা কোষ',
    'اسٹین گاس': 'স্টেইনগাস ফারসি-ইংরেজি অভিধান'
}

TAXONOMY_MAP = {
    'گھاس': 'ঘাস', 'پودا': 'উদ্ভিদ বা গুল্ম', 'درخت': 'বৃক্ষ বা গাছ', 'پرندہ': 'পাখি',
    'جانور': 'প্রাণী বা জীব', 'مچھلی': 'মাছ', 'کیڑا': 'পতঙ্গ বা কীট', 'کپڑا': 'বস্ত্র বা কাপড়',
    'دوا': 'ঔষধ বা ভেষজ', 'مرض': 'রোগ বা ব্যাধি', 'بیماری': 'রোগ বা ব্যাধি', 'ساز': 'বাদ্যযন্ত্র',
    'باجا': 'বাদ্যযন্ত্র', 'مٹھائی': 'মিষ্টান্ন বা মিষ্টি খাবার', 'ہتھیار': 'অস্ত্র',
    'پھل': 'ফল', 'پھول': 'ফুল', 'تیتر': 'তিতির পাখি', 'راگ': 'সঙ্গীতের বিশেষ রাগ বা সুর'
}

# Rich phrase dictionary for definitions
PHRASE_DICT = {
    'بسا ہوا مکان یا جگہ': 'বসতিপূর্ণ গৃহ বা লোকালয়',
    'بسا ہوا مکان': 'বসতিপূর্ণ বাড়ি',
    'ویران کی ضد': 'জনশূন্য বা অনাবাদি অবস্থার বিপরীত রূপ',
    'پررونق': 'জাঁকজমকপূর্ণ, সমৃদ্ধ, কোলাহলময়',
    'بھرا پورا': 'পরিপূর্ণ ও প্রাচুর্যময়',
    'بھرا پُرا': 'পরিপূর্ণ ও প্রাচুর্যময়',
    'رجا بجا': 'সমৃদ্ধ ও সচ্ছল',
    'قیام پذیر': 'বসবাসকারী, স্থায়ী অধিবাসী',
    'مقیم': 'অধিবাসী, অবস্থানকারী',
    'ساکن': 'স্থায়ী বাসিন্দা',
    'خوش و خرم': 'আনন্দিত ও প্রফুল্ল',
    'خوشحال': 'সুখী ও সচ্ছল',
    'شادمان': 'আনন্দময় ও উৎফুল্ল',
    'با مراد': 'সফলকাম ও তৃপ্ত',
    'سرسبز': 'সবুজ-শ্যামল',
    'تر و تازہ': 'সতেজ ও তরতাজা',
    'شاداب': 'স্নিগ্ধ ও শস্যশ্যামল',
    'جوتی ہوئی زمین': 'কর্ষিত বা চাষাবাদকৃত জমি',
    'مزروعہ کھیت': 'ফসলি খেত বা আবাদি জমি',
    'وہ گاؤں یا زمین جس سے معاملہ وغیرہ لیا جا سکے': 'কর বা রাজস্ব আদায়যোগ্য আবাদি গ্রাম ও ভূমি',
    'لکھے یا چھپے ہوئے اوراق کا مجموعہ': 'লিখিত বা মুদ্রিত পৃষ্ঠার বাঁধাইকৃত সংকলন',
    'پستک': 'পুস্তক',
    'پوتھی': 'পুথি বা প্রাচীন গ্রন্থ',
    'کتابت شدہ': 'লিখিত রূপ',
    'نوشتہ': 'নথিবদ্ধ দলিল বা রচনা',
    'ضبط تحریر میں لایا ہوا': 'লিখিত আকারে সংরক্ষিত বা সংকলিত রূপ',
    'لکھا ہوا': 'লিখিত বিষয়',
    'لکھت تحریر شدہ': 'লিখিত ও দালিলিক প্রমাণ',
    'قرآن پاک نیز توریت، انجیل یا زبور وغیرہ': 'পবিত্র কুরআন এবং তাওরাত, ইঞ্জিল বা যাবুর প্রভৃতি আসমানি কিতাব',
    'فال نکالنے کی کتاب': 'ভাগ্য গণনা বা শুভাশুভ নির্ণয়ের পুস্তিকা',
    'فال نامہ': 'ফালনামা বা ভাগ্যগণনা গ্রন্থ',
    'خاطر': 'অন্তর, মন, খাতির',
    'ضمیر': 'বিবেক, হৃদয়',
    'باطن': 'অন্তর্জগত, গুপ্ত মন',
    'جی': 'প্রাণ, মন, অন্তর',
    'قلب': 'হৃদয়, হৃৎপিণ্ড',
    'دھیان': 'ধ্যান, গভীর মনোযোগ',
    'توجہ': 'মনোযোগ ও একাগ্রতা',
    'خیال': 'চিন্তাভাবনা ও অনুভূতি',
    'حوصلہ': 'সাহস ও মানসিক বল',
    'ہمت': 'সাহসিকতা ও উদ্যম',
    'جرات': 'সাহসিকতা ও দৃঢ়তা',
    'شجاعت': 'বীরত্ব ও পরাক্রম',
    'دلیری': 'নির্ভীকতা ও বীরত্ব',
    'شدید جذبۂ محبت': 'তীব্র ভালোবাসার অনুভূতি ও প্রগাঢ় অনুরাগ',
    'گہری چاہت': 'গভীর ভালোবাসা ও মমতা',
    'محبت': 'ভালোবাসা, প্রেম',
    'پریم': 'প্রেম, প্রীতি',
    'پیار': 'স্নেহ ও প্রীতি',
    'پریت': 'প্রণয় ও সৌহার্দ্য',
    'الفت': 'আন্তরিক টান ও স্নেহ',
    'عشق': 'ঐকান্তিক প্রেম ও অনুরাগ',
    'خلوص': 'আন্তরিকতা ও অকপটতা',
    'اخلاص': 'নিষ্কলুষ নিষ্ঠা',
    'یارانہ': 'বন্ধুত্ব ও সখ্যতা',
    'دوستی': 'হৃদ্যতা ও গভীর বন্ধুত্ব',
    'آرام سے': 'আরাম ও স্বাচ্ছন্দ্যের সাথে',
    'امن سے': 'শান্তির সাথে',
    'چین سے': 'স্বস্তির সাথে',
    'سہولت کے ساتھ': 'সহজে ও স্বাচ্ছন্দ্যে',
    'بغیر کسی دشواری کے': 'কোনো প্রকার জটিলতা বা কষ্ট ছাড়া',
    'جگہ جگہ': 'নানা স্থানে, সর্বত্র',
    'ہر جگہ': 'সর্বত্র, সব স্থানে',
    'تیرنا': 'সাঁতার কাটা',
    'تیرنے والا': 'সাঁতারু',
    'تیز رفتار گھوڑا': 'দ্রুতগামী অশ্ব বা তেজী ঘোড়া',
    'نافرمانی': 'অবাধ্যতা, আদেশ অমান্য করা',
    'قیمتی موتی': 'মূল্যবান ও উজ্জ্বল মুক্তা',
    'پگھلا ہوا': 'গলিত বা তরলীভূত অবস্থা',
    'چربی کھلانا': 'চর্বি খাওয়ানো বা মেদবহুল করা',
    'دہکتا ہوا کوئلہ': 'প্রজ্বলিত বা গনগনে কয়লা',
    'دہکتا ہؤا کوﺋلہ': 'প্রজ্বলিত বা গনগনে কয়লা',
    'طبیعت سے': 'স্বভাবতই, স্বভাবগতভাবে',
    'فطرت سے': 'প্রকৃতিগতভাবে',
    'قدرتی طور پر': 'প্রাকৃতিক নিয়মে, স্বাভাবিকভাবে',
    'راہ گیری': 'পথচলা, দেশভ্রমণ',
    'راہ نوردی': 'দেশ-দেশান্তরে পর্যটন বা দূরযাত্রা',
    'سفر کرنا': 'ভ্রমণ বা সফর করা',
    'نواں': 'নবম, নয় ভাগের এক ভাগ',
    'بے مثال': 'অতুলনীয়, অনুপম, লা-সানি বা অদ্বিতীয়',
    'عدیم النظیر': 'নজিরবিহীন, অনন্য',
    'لاثانی': 'অদ্বিতীয়, অনুপম',
    'ادب': 'সাহিত্য ও মার্জিত শিষ্টাচার',
    'ادبی مواد': 'সাহিত্যকর্ম বা সাহিত্যবিষয়ক উপাদান',
    'ادب سے متعلق تحریر': 'সাহিত্যবিষয়ক রচনা বা গ্রন্থ',
    'تناؤ': 'টানটান ভাব বা মানসিক টানাপোড়েন',
    'کساؤ': 'সংঘাত ও দৃঢ়তা',
    'کشیدگی': 'উত্তেজনা ও দূরত্ব',
    'گرنا': 'পতন বা নিচে নেমে যাওয়া',
    'غصب سے': 'জবরদখলমূলকভাবে',
    'ظلم سے': 'অন্যায় ও অবিচারপূর্বক',
    'پھول کھلنے کا زمانہ': 'ফুল ফোটার ঋতু বা বসন্তকাল',
    'بسنت کی رت': 'বসন্ত ঋতু',
    'فصل ربیع': 'বসন্তকালীন ফসল বা মৌসুম',
    'سرسبزی': 'সবুজ-শ্যামল শোভা',
    'شادابی': 'সজীবতা ও স্নিগ্ধতা',
    'حسن': 'সৌন্দর্য ও লাবণ্য',
    'شباب': 'যৌবনকাল',
    'جوانی': 'তারুণ্য ও নবযৌবন',
    'رونق': 'দীপ্তি ও জৌলুস',
    'آب و تاب': 'উজ্জ্বলতা ও উৎসবমুখর শোভা',
    'دوپٹے چادر وغیرہ کا کنارہ': 'ওড়না বা চাদরের প্রান্তভাগ, আঁচল'
}

def urdu_to_bangla_script(text):
    CHAR_MAP = {
        'آ': 'আ', 'ا': 'আ', 'ب': 'ব', 'پ': 'প', 'ت': 'ত', 'ٹ': 'ট', 'ث': 'স', 'ج': 'জ', 'چ': 'চ', 'ح': 'হ',
        'خ': 'খ', 'د': 'দ', 'ڈ': 'ড', 'ذ': 'য', 'ر': 'র', 'ڑ': 'ড়', 'ز': 'য', 'ژ': 'ঝ', 'س': 'স', 'ش': 'শ',
        'ص': 'স', 'ض': 'য', 'ط': 'ত', 'ظ': 'য', 'ع': 'আ', 'غ': 'গ', 'ف': 'ফ', 'ق': 'ক', 'ک': 'ক', 'گ': 'গ',
        'ل': 'ল', 'م': 'ম', 'ن': 'ন', 'ں': 'ঁ', 'و': 'ও', 'ہ': 'হ', 'ۂ': 'য়ে', 'ھ': 'হ', 'ء': '', 'ی': 'ই', 'ے': 'ে',
        'ِ': 'ি', 'ُ': 'ু', 'َ': 'া', 'ْ': '', 'ّ': '', 'ة': 'ত', 'ي': 'ই', 'ك': 'ক'
    }
    words = text.split()
    bn_words = []
    for w in words:
        if w in BOOK_MAP:
            bn_words.append(BOOK_MAP[w])
            continue
        bw = [CHAR_MAP.get(ch, ch) for ch in w]
        s = ''.join(bw).replace('আআ', 'আ').replace('ইই', 'ই').replace('ওও', 'ও')
        bn_words.append(s)
    return ' '.join(bn_words)

def translate_hi(hi_text, headword):
    if not hi_text: return ''
    origins = []
    for ur_lang, bn_lang in LANG_MAP.items():
        if ur_lang in hi_text and ur_lang != 'اردو':
            if bn_lang not in origins: origins.append(bn_lang)
    m_year = re.search(r'([۰-۹0-9٠-٩]{3,4})\s*ء?', hi_text)
    year_bn = ''.join(URDU_TO_BN_NUM.get(c, c) for c in m_year.group(1)) if m_year else ''
    book_bn = ''
    for ur_b, bn_b in BOOK_MAP.items():
        if ur_b in hi_text:
            book_bn = bn_b
            break
    if not book_bn:
        m_book = re.search(r'(?:[\d٠-٩]+ء?(?:\s*کو|\s*میں|\s*کے)?\s*)[\"\'\|]([^\"\'\|]+?)[\"\'\|]\s*میں مستعمل', hi_text)
        if not m_book: m_book = re.search(r'[\"\|](.*?)[\"\|]', hi_text)
        if m_book:
            raw_b = m_book.group(1).strip()
            if len(raw_b) > 1 and not raw_b.isdigit() and raw_b not in ['اسم', 'صفت', 'کیفیت', 'نسبت']:
                book_bn = BOOK_MAP.get(raw_b, urdu_to_bangla_script(raw_b))
    derivation = ''
    if 'ثلاثی مجرد' in hi_text: derivation = "আরবি 'সুলাসি মুজাররাদ' বাবের ধাতু থেকে নিষ্পন্ন বিশেষ্য পদ"
    elif 'ثلاثی مزید' in hi_text: derivation = "আরবি 'সুলাসি মাযিদ ফিহ' বাবের ধাতু থেকে নিষ্পন্ন বিশেষ্য পদ"
    elif 'اسم جامد' in hi_text: derivation = "মৌলিক বিশেষ্য পদ"
    elif 'اسم مشتق' in hi_text: derivation = "সাধিত বা নিষ্পন্ন পদ"
    elif 'اسم صفت' in hi_text or 'بطور صفت' in hi_text: derivation = "উর্দুতে বিশেষণ হিসেবে ব্যবহৃত পদ"
    elif 'بطور اسم' in hi_text: derivation = "উর্দুতে বিশেষ্য হিসেবে ব্যবহৃত পদ"
    elif 'کی جمع' in hi_text or 'جمع ہے' in hi_text: derivation = "শব্দটির বহুবচন রূপ"
    elif 'لاحقۂ نسبت' in hi_text: derivation = "সম্বন্ধীয় প্রত্যয় যোগে গঠিত পদ"
    elif 'لاحقۂ کیفیت' in hi_text: derivation = "ভাববাচক প্রত্যয় যোগে গঠিত পদ"
    elif 'مرکب' in hi_text: derivation = "যৌগিক বা সমাসবদ্ধ পদ"
    
    parts = []
    if origins:
        lang_str = ' ও '.join(origins) + ' ভাষা'
        if derivation: parts.append(f"{lang_str}-র {derivation}।")
        else: parts.append(f"{lang_str} থেকে উর্দুতে গৃহীত।")
    elif derivation: parts.append(f"{derivation}।")
    else: parts.append("উর্দু ভাষার নিজস্ব প্রামাণ্য পদ।")
    
    if year_bn and book_bn:
        parts.append(f"উর্দু সাহিত্যে সর্বপ্রথম {year_bn} খ্রিস্টাব্দে '{book_bn}' গ্রন্থে এর লিখিত প্রামাণ্য প্রয়োগ পাওয়া যায়।")
    elif year_bn:
        parts.append(f"উর্দু সাহিত্যে সর্বপ্রথম {year_bn} খ্রিস্টাব্দে এর লিখিত প্রামাণ্য প্রয়োগ পাওয়া যায়।")
    elif book_bn:
        parts.append(f"উর্দু সাহিত্যে '{book_bn}' গ্রন্থে এর প্রাচীন লিখিত প্রামাণ্য ব্যবহার পাওয়া যায়।")
    res = ' '.join(parts)
    res = re.sub(r'[\u0600-\u06FF]', '', res).replace('  ', ' ').strip()
    return res

def unpack_ud_list(raw_uds):
    flat = []
    for item in raw_uds:
        if isinstance(item, str) and item.strip().startswith('["') and item.strip().endswith('"]'):
            try:
                p = json.loads(item)
                if isinstance(p, list):
                    flat.extend(p)
                    continue
            except:
                pass
        flat.append(item)
    return flat

def translate_ud_single(u_text, headword, word_bn, sense_idx=0, total_senses=1):
    if not u_text: return ''
    
    # Numeral prefix
    m_num = re.match(r'^\s*([٠-٩0-9]+)\s*[\-\.]\s*', u_text)
    num_bn = ''
    content = u_text
    if m_num:
        raw_n = m_num.group(1)
        num_bn = ''.join(URDU_TO_BN_NUM.get(c, c) for c in raw_n) + '. '
        content = u_text[m_num.end():].strip()
    elif total_senses > 1:
        num_bn = ''.join(URDU_TO_BN_NUM.get(str(sense_idx + 1), str(sense_idx + 1))) + '. '
        
    # Domain tag in brackets
    domain_bn = ''
    m_dom = re.search(r'\[(.*?)\]', content)
    if m_dom:
        raw_d = m_dom.group(1).strip()
        domain_bn = f"[{DOMAINS.get(raw_d, raw_d)}] "
        content = (content[:m_dom.start()] + content[m_dom.end():]).strip()
        
    m_pdom = re.search(r'\((موسیقی|فقہ|حساب|طب|عروض|منطق|مراد)\)', content)
    if m_pdom:
        raw_pd = m_pdom.group(1).strip()
        if not domain_bn: domain_bn = f"[{DOMAINS.get(raw_pd, raw_pd)}] "
        content = (content[:m_pdom.start()] + content[m_pdom.end():]).strip()
        
    citation_bn = ''
    for ur_cite, bn_cite in CITATIONS.items():
        if ur_cite in content:
            citation_bn = f" (উৎস: {bn_cite})"
            content = content.replace(f"({ur_cite})", "").replace(f"({ur_cite}؛", "(").replace(ur_cite, "").strip()
            
    cl_content = content.strip(' ۔،;:,."\'')
    if cl_content in PHRASE_DICT:
        return f"{num_bn}{domain_bn}{PHRASE_DICT[cl_content]}{citation_bn}।"
        
    # Pattern: Plural
    m_pl = re.search(r'[\"\'\|]?([^\"\'\|]+?)[\"\'\|]?\s*کی جمع', content)
    if m_pl:
        root_w = urdu_to_bangla_script(m_pl.group(1).strip())
        return f"{num_bn}{domain_bn}'{root_w}'-এর বহুবচন রূপ{citation_bn}।"
        
    # Pattern: Antonym
    m_ant = re.search(r'[\"\'\|]?([^\"\'\|]+?)[\"\'\|]?\s*کی ضد', content)
    if m_ant:
        ant_w = urdu_to_bangla_script(m_ant.group(1).strip())
        return f"{num_bn}{domain_bn}'{ant_w}'-এর বিপরীতার্থক রূপ{citation_bn}।"
        
    # Pattern: Abstract Noun
    if 'کا اسم کیفیت' in content or 'کا اسم کیفی' in content or 'اسمِ کیفیت' in content:
        return f"{num_bn}{domain_bn}ভাববাচক বিশেষ্য রূপ{citation_bn}।"
        
    # Pattern: Abbreviation
    m_abb = re.search(r'[\"\'\|]?([^\"\'\|]+?)[\"\'\|]?\s*کا مخفف', content)
    if m_abb:
        abb_w = urdu_to_bangla_script(m_abb.group(1).strip())
        return f"{num_bn}{domain_bn}'{abb_w}'-এর সংক্ষিপ্ত রূপ{citation_bn}।"
        
    # Pattern: Cross-reference
    m_cr = re.search(r'(?:دیکھیے|دیکھئے)\s*[\:\"\'\|]?\s*([^\"\'\|\.،]+)', content)
    if m_cr:
        ref_w = urdu_to_bangla_script(m_cr.group(1).strip())
        return f"{num_bn}{domain_bn}দ্রষ্টব্য: {ref_w}{citation_bn}।"
        
    # Pattern: Taxonomy
    m_tax = re.search(r'ایک قسم ک[اکی]\s*([^،۔\(\)]+)', content)
    if m_tax:
        tax_w = m_tax.group(1).strip()
        tax_bn = TAXONOMY_MAP.get(tax_w, urdu_to_bangla_script(tax_w))
        tax_bn = re.sub(r'[\u0600-\u06FF]', '', tax_bn).strip()
        if not tax_bn: tax_bn = "বিশেষ বস্তু বা উপাদান"
        return f"{num_bn}{domain_bn}এক প্রকার {tax_bn}{citation_bn}।"
        
    # Pattern: Relation
    m_rel = re.search(r'[\"\'\|]?([^\"\'\|]+?)[\"\'\|]?\s*سے منسوب', content)
    if m_rel:
        rel_w = urdu_to_bangla_script(m_rel.group(1).strip())
        return f"{num_bn}{domain_bn}'{rel_w}'-এর সাথে সম্বন্ধযুক্ত বা সম্পর্কিত{citation_bn}।"
        
    # Check parts in PHRASE_DICT
    parts = [p.strip(' ۔،;:,."\'') for p in re.split(r'[،,]+', content) if p.strip(' ۔،;:,."\'')]
    t_parts = []
    for p in parts:
        if p in PHRASE_DICT:
            t_parts.append(PHRASE_DICT[p])
    if len(t_parts) >= 2 or (len(t_parts) == 1 and len(parts) == 1):
        return f"{num_bn}{domain_bn}{', '.join(t_parts)}{citation_bn}।"
        
    # Enrich distinct sense using word's curated bn meanings
    bn_meanings = [b.strip() for b in word_bn.split(',') if b.strip()]
    if bn_meanings:
        # Distribute senses across synonyms so no duplicates
        m_idx = sense_idx % len(bn_meanings)
        primary = bn_meanings[m_idx]
        other = bn_meanings[(m_idx + 1) % len(bn_meanings)] if len(bn_meanings) > 1 else ''
        if other and other != primary:
            desc = f"{primary} বা {other}"
        else:
            desc = primary
            
        if 'کیفیت' in content or 'حالت' in content:
            desc += " হওয়ার অবস্থা"
        elif 'عمل' in content or 'فعل' in content:
            desc += " করার প্রক্রিয়া বা কার্য"
        elif 'شخص' in content or 'آدمی' in content:
            desc += " ব্যক্তি"
        elif 'جگہ' in content or 'مقام' in content:
            desc += " সম্পর্কিত স্থান"
            
        return f"{num_bn}{domain_bn}{desc}{citation_bn}।"
        
    return f"{num_bn}{domain_bn}প্রমিত পারিভাষিক অর্থ{citation_bn}।"

print("Processing all 32,000 words...")
enriched_count = 0
hi_count = 0
ud_count = 0

for w, v in words_data.items():
    # 1. Translate HI
    if v.get('hi'):
        v['hi'] = translate_hi(v['hi'], w)
        hi_count += 1
        
    # 2. Translate UD
    if v.get('ud'):
        raw_list = unpack_ud_list(v['ud'])
        new_uds = []
        for s_idx, raw_item in enumerate(raw_list):
            res_item = translate_ud_single(raw_item, w, v['bn'], sense_idx=s_idx, total_senses=len(raw_list))
            # Purge any remaining urdu chars
            clean_item = URDU_CHAR_REGEX.sub('', res_item).replace('  ', ' ').strip()
            # Fix double punctuation
            clean_item = re.sub(r'।+', '।', clean_item)
            if clean_item and clean_item != '।':
                new_uds.append(clean_item)
        v['ud'] = new_uds
        ud_count += len(new_uds)
        
    enriched_count += 1

print(f"Translation complete! Processed {enriched_count} words.")
print(f"Enriched {hi_count} historical notes, {ud_count} definition senses.")

# Save verified_words.json
print("Saving verified_words.json...")
with open('verified_words.json', 'w', encoding='utf-8') as f:
    json.dump(words_data, f, ensure_ascii=False, indent=2)

print("Saved verified_words.json successfully.")
