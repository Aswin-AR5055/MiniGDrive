def get_translations(lang):
    translations = {
        "select_all": {
            "en": "Select All",
            "ta": "அனைத்தையும் தேர்ந்தெடு",
            "hi": "सभी चुनें"
        },
        "delete_selected": {
            "en": "Delete Selected",
            "ta": "தேர்ந்தெடுத்தவற்றை நீக்கு",
            "hi": "चयनित हटाएँ"
        },
        "restore_selected": {
            "en": "Restore Selected",
            "ta": "தேர்ந்தெடுக்கப்பட்டவை மீட்க",
            "hi": "चयनित बहाल करें"
        },
        "sort_by_name": {
            "en": "Sort by Name",
            "ta": "பெயரால் வரிசைப்படுத்து",
            "hi": "नाम से छाँटें"
        },
        "sort_by_date": {
            "en": "Sort by Date",
            "ta": "தேதியால் வரிசைப்படுத்து",
            "hi": "तारीख से छाँटें"
        },
        "sort_by_size": {
            "en": "Sort by Size",
            "ta": "அளவால் வரிசைப்படுத்து",
            "hi": "आकार से छाँटें"
        },
        "sort_by_type": {
            "en": "Sort by Type",
            "ta": "வகையால் வரிசைப்படுத்து",
            "hi": "प्रकार से छाँटें"
        },
        "search_files": {
            "en": "Search files...",
            "ta": "கோப்புகளை தேடு...",
            "hi": "फ़ाइलें खोजें..."
        },
        "my_drive": {"en": "My Drive", "ta": "எனது டிரைவ்", "hi": "मेरा ड्राइव"},
        "hello": {"en": "Hello", "ta": "வணக்கம்", "hi": "नमस्ते"},
        "logout": {"en": "Logout", "ta": "வெளியேறு", "hi": "लॉगआउट"},
        "storage": {"en": "Storage:", "ta": "ஸ்டோரேஜ்:", "hi": "स्टोरेज:"},
        "drop_here": {
            "en": "Drop files here or click to upload",
            "ta": "இங்கே கோப்புகளை இடுக அல்லது கிளிக் செய்யவும்",
            "hi": "फ़ाइलें यहाँ छोड़ें या अपलोड करने के लिए क्लिक करें"
        },
        "my_files": {"en": "My Files", "ta": "எனது கோப்புகள்", "hi": "मेरी फाइलें"},
        "download": {"en": "Download", "ta": "பதிவிறக்கு", "hi": "डाउनलोड"},
        "trash": {"en": "Trash", "ta": "அகற்றுக", "hi": "ट्रैश"},
        "favourites": {"en": "Favourites", "ta": "பிடித்தவை", "hi": "पसंदीदा"},
        "share": {"en": "Share", "ta": "பகிர்", "hi": "साझा करें"},
        "no_files": {"en": "No files uploaded.", "ta": "எந்த கோப்புகளும் இல்லை.", "hi": "कोई फ़ाइल अपलोड नहीं की गई"},
        "download_selected": {"en": "Download Selected as ZIP", "ta": "ZIP ஆக பதிவிறக்கு", "hi": "चयनित ज़िप डाउनलोड करें"},
        "trash_bin": {"en": "Trash", "ta": "அகற்றியவை", "hi": "कचरा पात्र"},
        "restore": {"en": "Restore", "ta": "மீட்டமை", "hi": "पुनर्स्थापित"},
        "delete_forever": {"en": "Delete Permanently", "ta": "நிரந்தரமாக நீக்கு", "hi": "स्थायी रूप से हटाएं"},
        "used": {"en": "used", "ta": "பயன்பட்டது", "hi": "उपयोग किया गया"},
        "profile": {"en": "Profile", "ta": "சுயவிவரம்", "hi": "प्रोफ़ाइल"},
        "bio": {"en": "Bio", "ta": "வாழ்க்கை வரலாறு", "hi": "जीवनी"},
        "bio_placeholder": {"en": "Tell us something about you...", "ta": "உங்களைப் பற்றி எங்களிடம் சொல்லுங்கள்...", "hi": "हमें अपने बारे में बताएं..."},
        "age": {"en": "Age", "ta": "வயது", "hi": "उम्र"},
        "age_placeholder": {"en": "Your age", "ta": "உங்கள் வயது", "hi": "आपकी उम्र"},
        "profile_pic": {"en": "Profile Picture", "ta": "சுயவிவர படம்", "hi": "प्रोफ़ाइल चित्र"},
        "remove_pic": {"en": "Remove current profile picture", "ta": "தற்போதைய சுயவிவர படத்தை அகற்று", "hi": "वर्तमान प्रोफ़ाइल चित्र हटाएं"},
        "save_changes": {"en": "Save Changes", "ta": "மாற்றங்களை சேமிக்கவும்", "hi": "परिवर्तनों को सुरक्षित करें"},
        "back_to_dashboard": {"en": "Back to Dashboard", "ta": "டாஷ்போர்டுக்கு திரும்புக", "hi": "डैशबोर्ड पर वापस जाएं"},
    }
    return {key: val.get(lang, val["en"]) for key, val in translations.items()}
