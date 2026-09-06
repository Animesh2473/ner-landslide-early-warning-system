"""
alerts.py
Multilingual alert message templates for SMS/app-based early warnings.
In production, deliver via SMS gateway (e.g. state DM authority's bulk-SMS
provider), push notification service, and IVR for very low-literacy /
no-smartphone areas. Templates below cover English + four regional
languages commonly used across the NER.
"""

UI_TEXT = {
    "English": {
        "app_title": "NER Landslide Early Warning & Monitoring Platform",
        "overview": "Overview",
        "gis_dashboard": "GIS Risk Dashboard",
        "sensor_monitoring": "Sensor Monitoring",
        "field_reporting": "Field Reporting",
        "alerts": "Alerts & Notifications",
        "road_status": "Road Connectivity Status",
        "about": "System Architecture",
        "offline_mode": "Offline / Low-Network Mode",
        "language": "Language",
    },
    "Hindi": {
        "app_title": "पूर्वोत्तर भूस्खलन पूर्व चेतावनी एवं निगरानी प्रणाली",
        "overview": "सारांश",
        "gis_dashboard": "जीआईएस जोखिम डैशबोर्ड",
        "sensor_monitoring": "सेंसर निगरानी",
        "field_reporting": "फील्ड रिपोर्टिंग",
        "alerts": "अलर्ट और सूचनाएं",
        "road_status": "सड़क संपर्क स्थिति",
        "about": "सिस्टम संरचना",
        "offline_mode": "ऑफ़लाइन / कम-नेटवर्क मोड",
        "language": "भाषा",
    },
    "Assamese": {
        "app_title": "উত্তৰ-পূব ভূমিস্খলন সতৰ্কতা আৰু নিৰীক্ষণ প্লেটফৰ্ম",
        "overview": "চমু বিৱৰণ",
        "gis_dashboard": "জিআইএছ জোখিম ড্যাশব’ৰ্ড",
        "sensor_monitoring": "চেন্সৰ নিৰীক্ষণ",
        "field_reporting": "ফিল্ড ৰিপ’ৰ্টিং",
        "alerts": "সতৰ্কবাণী আৰু জাননী",
        "road_status": "সড়ক সংযোগৰ স্থিতি",
        "about": "প্ৰণালীৰ গঠন",
        "offline_mode": "অফলাইন / কম-নেটৱৰ্ক মোড",
        "language": "ভাষা",
    },
    "Bengali": {
        "app_title": "উত্তর-পূর্বাঞ্চল ভূমিধস পূর্ব সতর্কতা ও পর্যবেক্ষণ প্ল্যাটফর্ম",
        "overview": "সংক্ষিপ্ত বিবরণ",
        "gis_dashboard": "জিআইএস ঝুঁকি ড্যাশবোর্ড",
        "sensor_monitoring": "সেন্সর পর্যবেক্ষণ",
        "field_reporting": "ফিল্ড রিপোর্টিং",
        "alerts": "সতর্কতা ও বিজ্ঞপ্তি",
        "road_status": "সড়ক সংযোগ অবস্থা",
        "about": "সিস্টেম কাঠামো",
        "offline_mode": "অফলাইন / স্বল্প-নেটওয়ার্ক মোড",
        "language": "ভাষা",
    },
    "Manipuri": {
        "app_title": "নর্থ ইস্ট লেন্ডস্লাইড ৱার্নিং অমসুং মনিটরিং প্লেটফর্ম",
        "overview": "অচুম্বা",
        "gis_dashboard": "জিআইএস রিস্ক ড্যাশবোর্ড",
        "sensor_monitoring": "সেন্সর মনিটরিং",
        "field_reporting": "ফীল্ড রিপোর্টিং",
        "alerts": "এলার্ট অমসুং নোটিফিকেশন",
        "road_status": "লম্বী কনেক্টিভিটী স্টেটস",
        "about": "সিস্টেম আর্কিটেকচার",
        "offline_mode": "অফলাইন / নেটৱার্ক য়াম্লবা মোড",
        "language": "লোন",
    },
}

ALERT_TEMPLATES = {
    "English": {
        "Low": "Advisory: {name} ({state}) risk level LOW ({score}/100). Routine monitoring continues.",
        "Medium": "Caution: {name} ({state}) risk level MEDIUM ({score}/100). Stay alert to weather updates.",
        "High": "WARNING: {name} ({state}) risk level HIGH ({score}/100). Avoid travel on affected stretch. District DM notified.",
        "Critical": "URGENT EVACUATION ADVISORY: {name} ({state}) risk level CRITICAL ({score}/100). Move to safer ground immediately. Emergency teams alerted.",
    },
    "Hindi": {
        "Low": "सूचना: {name} ({state}) में जोखिम स्तर निम्न ({score}/100)। सामान्य निगरानी जारी है।",
        "Medium": "सावधानी: {name} ({state}) में जोखिम स्तर मध्यम ({score}/100)। मौसम अपडेट पर ध्यान दें।",
        "High": "चेतावनी: {name} ({state}) में जोखिम स्तर उच्च ({score}/100)। प्रभावित मार्ग पर यात्रा से बचें। जिला प्रशासन को सूचित।",
        "Critical": "तत्काल निकासी सूचना: {name} ({state}) में जोखिम स्तर अति गंभीर ({score}/100)। तुरंत सुरक्षित स्थान पर जाएं। आपातकालीन दल सूचित।",
    },
    "Assamese": {
        "Low": "জাননী: {name} ({state})ৰ বিপদ স্তৰ নিম্ন ({score}/100)। নিয়মীয়া নিৰীক্ষণ চলি আছে।",
        "Medium": "সাৱধান: {name} ({state})ৰ বিপদ স্তৰ মধ্যম ({score}/100)। বতৰৰ আপডেটলৈ দৃষ্টি ৰাখক।",
        "High": "সতৰ্কবাণী: {name} ({state})ৰ বিপদ স্তৰ উচ্চ ({score}/100)। প্ৰভাৱিত পথত যাতায়াত পৰিহাৰ কৰক। জিলা প্ৰশাসনক অৱগত কৰা হ'ল।",
        "Critical": "জৰুৰী উলিয়াই অনাৰ সতৰ্কবাণী: {name} ({state})ৰ বিপদ স্তৰ অতি গুৰুতৰ ({score}/100)। তৎক্ষণাৎ সুৰক্ষিত স্থানলৈ যাওক। জৰুৰীকালীন দল অৱগত।",
    },
    "Bengali": {
        "Low": "বিজ্ঞপ্তি: {name} ({state})-এ ঝুঁকির মাত্রা নিম্ন ({score}/100)। নিয়মিত পর্যবেক্ষণ চলছে।",
        "Medium": "সতর্কতা: {name} ({state})-এ ঝুঁকির মাত্রা মাঝারি ({score}/100)। আবহাওয়ার আপডেটে নজর রাখুন।",
        "High": "সতর্কবার্তা: {name} ({state})-এ ঝুঁকির মাত্রা উচ্চ ({score}/100)। প্রভাবিত রাস্তায় ভ্রমণ এড়িয়ে চলুন। জেলা প্রশাসনকে জানানো হয়েছে।",
        "Critical": "জরুরি সরিয়ে নেওয়ার নির্দেশ: {name} ({state})-এ ঝুঁকির মাত্রা সংকটজনক ({score}/100)। অবিলম্বে নিরাপদ স্থানে সরে যান। জরুরি দলকে জানানো হয়েছে।",
    },
    "Manipuri": {
        "Low": "খংহনবা: {name} ({state}) গী রিস্ক লেভেল LOW ({score}/100)। রুটিন মনিটরিং চলবি।",
        "Medium": "চেক্সিন লৌবীয়ু: {name} ({state}) গী রিস্ক লেভেল MEDIUM ({score}/100)। ৱেদর আপডেট য়েংবীয়ু।",
        "High": "ৱার্নিং: {name} ({state}) গী রিস্ক লেভেল HIGH ({score}/100)। লম্বীদুদা চৎলগা থোক্না লৈরকউ। ডিস্ট্রিক্ট ডিএম-দা খংহল্লে।",
        "Critical": "য়াম্না থৌগৎপা ইভ্যাকুয়েসন খংহনবা: {name} ({state}) গী রিস্ক লেভেল CRITICAL ({score}/100)। খুদক্তা সেফ ফমদা চৎখো। ইমার্জেন্সি টীমদা খংহল্লে।",
    },
}


def get_alert_message(language: str, name: str, state: str, category: str, score: float) -> str:
    lang = language if language in ALERT_TEMPLATES else "English"
    template = ALERT_TEMPLATES[lang].get(category, ALERT_TEMPLATES[lang]["Medium"])
    return template.format(name=name, state=state, score=round(score, 1))


def t(language: str, key: str) -> str:
    """UI text lookup helper."""
    lang = language if language in UI_TEXT else "English"
    return UI_TEXT[lang].get(key, UI_TEXT["English"].get(key, key))
