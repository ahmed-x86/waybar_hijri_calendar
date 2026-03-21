#!/usr/bin/env python3

import json
import datetime
import urllib.request
import urllib.error
import sys
import os
import argparse
import ssl

# مسار ملف التخزين
CACHE_FILE = os.path.expanduser("~/.cache/waybar_hijri_cache.json")

# 1. قاموس الشهور لكل اللغات المدعومة
MONTHS_I18N = {
    "ar": ["محرم", "صفر", "ربيع الأول", "ربيع الآخر", "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان", "رمضان", "شوال", "ذو القعدة", "ذو الحجة"],
    "en": ["Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani", "Jumada al-ula", "Jumada al-akhira", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"],
    "fr": ["Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani", "Jumada al-ula", "Jumada al-akhira", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"],
    "de": ["Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani", "Jumada al-ula", "Jumada al-akhira", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"],
    "it": ["Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani", "Jumada al-ula", "Jumada al-akhira", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"],
    "es": ["Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani", "Jumada al-ula", "Jumada al-akhira", "Rajab", "Sha'ban", "Ramadán", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"],
    "tr": ["Muharrem", "Safer", "Rebiülevvel", "Rebiülahir", "Cemaziyelevvel", "Cemaziyelahir", "Recep", "Şaban", "Ramazan", "Şevval", "Zilkade", "Zilhicce"],
    "ku": ["Muherem", "Sefer", "Rebîul ewel", "Rebîul axir", "Cemaziyel ewel", "Cemaziyel axir", "Receb", "Şeban", "Remezan", "Şewal", "Zîlqe'de", "Zîlhice"],
    "ja": ["ムハッラム", "サファル", "ラビー・ウル・アウワル", "ラビー・ウッ・サーニー", "ジュマーダー・アル・ウーラー", "ジュマーダー・アル・アーヒラ", "ラジャブ", "シャアバーン", "ラマダーン", "シャウワール", "ズー・アル・カアダ", "ズー・アル・ヒッジャ"],
    "ko": ["무하람", "사파르", "라비 알아왈", "라비 알사니", "주마다 알울라", "주마다 알아키라", "라잡", "샤반", "라마단", "샤왈", "둘카다", "둘히자"],
    "id": ["Muharram", "Safar", "Rabi'ul Awal", "Rabi'ul Akhir", "Jumadil Awal", "Jumadil Akhir", "Rajab", "Sya'ban", "Ramadhan", "Syawal", "Dzulqa'dah", "Dzulhijjah"]
}

# 2. قاموس الإعدادات والمناسبات الكاملة (مترجمة لكل اللغات)
I18N = {
    "ar": {
        "error": "🌙 خطأ", "no_connection": "لا يوجد اتصال.", "reminder": "تذكير",
        "calendar_header": "Su  Mo  Tu  We  Th  Fr  Sa",
        "weekdays": ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
        "white_days": "صيام الأيام البيض ⚪",
        "events": {
            (1, 9): "تاسوعاء 🌙", (1, 10): "عاشوراء 🌙", (9, 1): "أول رمضان 🌙",
            (9, 21): "ليلة وترية 🤲", (9, 23): "ليلة وترية 🤲", (9, 25): "ليلة وترية 🤲",
            (9, 27): "ليلة القدر ✨", (9, 29): "ليلة وترية 🤲", (10, 1): "عيد الفطر 🎉",
            (12, 8): "التروية 🕋", (12, 9): "يوم عرفة 🤲", (12, 10): "عيد الأضحى 🐑",
            (12, 11): "تشريق 1", (12, 12): "تشريق 2", (12, 13): "تشريق 3"
        }
    },
    "en": {
        "error": "🌙 Error", "no_connection": "No connection.", "reminder": "Reminder",
        "calendar_header": "Su  Mo  Tu  We  Th  Fr  Sa",
        "weekdays": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "white_days": "White Days Fasting ⚪",
        "events": {
            (1, 9): "Tasu'a 🌙", (1, 10): "Ashura 🌙", (9, 1): "Ramadan Start 🌙",
            (9, 21): "Odd Night 🤲", (9, 23): "Odd Night 🤲", (9, 25): "Odd Night 🤲",
            (9, 27): "Laylat al-Qadr ✨", (9, 29): "Odd Night 🤲", (10, 1): "Eid al-Fitr 🎉",
            (12, 8): "Tarwiyah 🕋", (12, 9): "Arafah Day 🤲", (12, 10): "Eid al-Adha 🐑",
            (12, 11): "Tashreeq 1", (12, 12): "Tashreeq 2", (12, 13): "Tashreeq 3"
        }
    },
    "fr": {
        "error": "🌙 Erreur", "no_connection": "Pas de connexion.", "reminder": "Rappel",
        "calendar_header": "Di  Lu  Ma  Me  Je  Ve  Sa",
        "weekdays": ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"],
        "white_days": "Jours Blancs ⚪",
        "events": {
            (1, 9): "Tasu'a 🌙", (1, 10): "Achoura 🌙", (9, 1): "Début du Ramadan 🌙",
            (9, 21): "Nuit Impaire 🤲", (9, 23): "Nuit Impaire 🤲", (9, 25): "Nuit Impaire 🤲",
            (9, 27): "Nuit du Destin ✨", (9, 29): "Nuit Impaire 🤲", (10, 1): "Aïd el-Fitr 🎉",
            (12, 8): "Tarwiyah 🕋", (12, 9): "Jour d'Arafat 🤲", (12, 10): "Aïd el-Adha 🐑",
            (12, 11): "Tachriq 1", (12, 12): "Tachriq 2", (12, 13): "Tachriq 3"
        }
    },
    "de": {
        "error": "🌙 Fehler", "no_connection": "Keine Verbindung.", "reminder": "Erinnerung",
        "calendar_header": "So  Mo  Di  Mi  Do  Fr  Sa",
        "weekdays": ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
        "white_days": "Weiße Tage ⚪",
        "events": {
            (1, 9): "Tasu'a 🌙", (1, 10): "Aschura 🌙", (9, 1): "Ramadan Beginn 🌙",
            (9, 21): "Ungerade Nacht 🤲", (9, 23): "Ungerade Nacht 🤲", (9, 25): "Ungerade Nacht 🤲",
            (9, 27): "Lailat al-Qadr ✨", (9, 29): "Ungerade Nacht 🤲", (10, 1): "Eid al-Fitr 🎉",
            (12, 8): "Tarwiyah 🕋", (12, 9): "Tag von Arafat 🤲", (12, 10): "Eid al-Adha 🐑",
            (12, 11): "Taschriq 1", (12, 12): "Taschriq 2", (12, 13): "Taschriq 3"
        }
    },
    "it": {
        "error": "🌙 Errore", "no_connection": "Nessuna connessione.", "reminder": "Promemoria",
        "calendar_header": "Do  Lu  Ma  Me  Gi  Ve  Sa",
        "weekdays": ["Domenica", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"],
        "white_days": "Giorni Bianchi ⚪",
        "events": {
            (1, 9): "Tasu'a 🌙", (1, 10): "Ashura 🌙", (9, 1): "Inizio Ramadan 🌙",
            (9, 21): "Notte Dispari 🤲", (9, 23): "Notte Dispari 🤲", (9, 25): "Notte Dispari 🤲",
            (9, 27): "Notte del Destino ✨", (9, 29): "Notte Dispari 🤲", (10, 1): "Eid al-Fitr 🎉",
            (12, 8): "Tarwiyah 🕋", (12, 9): "Giorno di Arafat 🤲", (12, 10): "Eid al-Adha 🐑",
            (12, 11): "Tashreeq 1", (12, 12): "Tashreeq 2", (12, 13): "Tashreeq 3"
        }
    },
    "es": {
        "error": "🌙 Error", "no_connection": "Sin conexión.", "reminder": "Recordatorio",
        "calendar_header": "Do  Lu  Ma  Mi  Ju  Vi  Sá",
        "weekdays": ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
        "white_days": "Ayuno de los Días Blancos ⚪",
        "events": {
            (1, 9): "Tasu'a 🌙", (1, 10): "Ashura 🌙", (9, 1): "Inicio de Ramadán 🌙",
            (9, 21): "Noche Impar 🤲", (9, 23): "Noche Impar 🤲", (9, 25): "Noche Impar 🤲",
            (9, 27): "Laylat al-Qadr ✨", (9, 29): "Noche Impar 🤲", (10, 1): "Eid al-Fitr 🎉",
            (12, 8): "Tarwiyah 🕋", (12, 9): "Día de Arafat 🤲", (12, 10): "Eid al-Adha 🐑",
            (12, 11): "Tashreeq 1", (12, 12): "Tashreeq 2", (12, 13): "Tashreeq 3"
        }
    },
    "tr": {
        "error": "🌙 Hata", "no_connection": "Bağlantı yok.", "reminder": "Hatırlatma",
        "calendar_header": "Pz  Pt  Sa  Ça  Pe  Cu  Ct",
        "weekdays": ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"],
        "white_days": "Eyyam-ı Bız Orucu ⚪",
        "events": {
            (1, 9): "Tasua 🌙", (1, 10): "Aşure 🌙", (9, 1): "Ramazan Başlangıcı 🌙",
            (9, 21): "Tek Gece 🤲", (9, 23): "Tek Gece 🤲", (9, 25): "Tek Gece 🤲",
            (9, 27): "Kadir Gecesi ✨", (9, 29): "Tek Gece 🤲", (10, 1): "Ramazan Bayramı 🎉",
            (12, 8): "Terviye 🕋", (12, 9): "Arefe Günü 🤲", (12, 10): "Kurban Bayramı 🐑",
            (12, 11): "Teşrik 1", (12, 12): "Teşrik 2", (12, 13): "Teşrik 3"
        }
    },
    "ku": {
        "error": "🌙 Çewtî", "no_connection": "Têkildar tune.", "reminder": "Bîrxistin",
        "calendar_header": "Yk  Du  Sê  Ça  Pê  În  Şe",
        "weekdays": ["Yekşem", "Duşem", "Sêşem", "Çarşem", "Pêncşem", "În", "Şemî"],
        "white_days": "Rojiya Rojên Spî ⚪",
        "events": {
            (1, 9): "Tasûa 🌙", (1, 10): "Aşûra 🌙", (9, 1): "Destpêka Remezanê 🌙",
            (9, 21): "Şeva Taqe 🤲", (9, 23): "Şeva Taqe 🤲", (9, 25): "Şeva Taqe 🤲",
            (9, 27): "Şeva Qedrê ✨", (9, 29): "Şeva Taqe 🤲", (10, 1): "Cejna Remezanê 🎉",
            (12, 8): "Terwiye 🕋", (12, 9): "Roja Erefê 🤲", (12, 10): "Cejna Qurbanê 🐑",
            (12, 11): "Teşrîq 1", (12, 12): "Teşrîq 2", (12, 13): "Teşrîq 3"
        }
    },
    "ja": {
        "error": "🌙 エラー", "no_connection": "接続なし", "reminder": "リマインダー",
        "calendar_header": "日  月  火  水  木  金  土",
        "weekdays": ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日"],
        "white_days": "白き日の断食 ⚪",
        "events": {
            (1, 9): "タースーアー 🌙", (1, 10): "アーシューラー 🌙", (9, 1): "ラマダーン開始 🌙",
            (9, 21): "奇数の夜 🤲", (9, 23): "奇数の夜 🤲", (9, 25): "奇数の夜 🤲",
            (9, 27): "みいつの夜 ✨", (9, 29): "奇数の夜 🤲", (10, 1): "イード・アル＝フィトル 🎉",
            (12, 8): "タルウィヤ 🕋", (12, 9): "アラファトの日 🤲", (12, 10): "イード・アル＝アドハー 🐑",
            (12, 11): "タシュリーク 1", (12, 12): "タシュリーク 2", (12, 13): "タシュリーク 3"
        }
    },
    "ko": {
        "error": "🌙 오류", "no_connection": "연결 없음.", "reminder": "알림",
        "calendar_header": "일  월  화  수  목  금  토",
        "weekdays": ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"],
        "white_days": "하얀 날의 금식 ⚪",
        "events": {
            (1, 9): "타수아 🌙", (1, 10): "아슈라 🌙", (9, 1): "라마단 시작 🌙",
            (9, 21): "홀수 밤 🤲", (9, 23): "홀수 밤 🤲", (9, 25): "홀수 밤 🤲",
            (9, 27): "권능의 밤 ✨", (9, 29): "홀수 밤 🤲", (10, 1): "이드 알피트르 🎉",
            (12, 8): "타르위야 🕋", (12, 9): "아라파트의 날 🤲", (12, 10): "이드 알아드하 🐑",
            (12, 11): "타쉬리크 1", (12, 12): "타쉬리크 2", (12, 13): "타쉬리크 3"
        }
    },
    "id": {
        "error": "🌙 Eror", "no_connection": "Tidak ada koneksi.", "reminder": "Pengingat",
        "calendar_header": "Mg  Sn  Sl  Rb  Km  Jm  Sb",
        "weekdays": ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"],
        "white_days": "Puasa Ayyamul Bidh ⚪",
        "events": {
            (1, 9): "Tasu'a 🌙", (1, 10): "Asyura 🌙", (9, 1): "Awal Ramadhan 🌙",
            (9, 21): "Malam Ganjil 🤲", (9, 23): "Malam Ganjil 🤲", (9, 25): "Malam Ganjil 🤲",
            (9, 27): "Lailatul Qadar ✨", (9, 29): "Malam Ganjil 🤲", (10, 1): "Idul Fitri 🎉",
            (12, 8): "Tarwiyah 🕋", (12, 9): "Hari Arafah 🤲", (12, 10): "Idul Adha 🐑",
            (12, 11): "Tasyrik 1", (12, 12): "Tasyrik 2", (12, 13): "Tasyrik 3"
        }
    }
}

def load_cache():
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f: 
            return json.load(f)
    except: 
        return {}

def save_cache(cache_data):
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f: 
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except: 
        pass

def fetch_hijri_month(date_str):
    # إنشاء سياق أمان لتجاوز أخطاء SSL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url_today = f"https://api.aladhan.com/v1/gToH?date={date_str}"
    req = urllib.request.Request(url_today, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        h_month = data['data']['hijri']['month']['number']
        h_year = data['data']['hijri']['year']

    url_month = f"https://api.aladhan.com/v1/hToGCalendar/{h_month}/{h_year}"  
    req_month = urllib.request.Request(url_month, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req_month, timeout=10, context=ctx) as resp:  
        month_data = json.loads(resp.read().decode('utf-8'))  
          
    new_cache = {}  
    for item in month_data.get('data', []):  
        g_date, hijri = item['gregorian']['date'], item['hijri']  
        new_cache[g_date] = {  
            "day": int(hijri['day']),  
            "month_number": int(hijri['month']['number']),  
            "year": hijri['year'],  
            "month_length": len(month_data['data'])  
        }  
    return new_cache  

def safe_print(output_dict):
    """دالة لطباعة المخرجات وتجنب خطأ BrokenPipeError"""
    try:
        print(json.dumps(output_dict, ensure_ascii=False))
        sys.stdout.flush()
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-lang", "--language", default="ar", choices=list(I18N.keys()), help="Language")
    args = parser.parse_args()
    lang = args.language

    try:
        today_date = datetime.datetime.now()  
        today_str = today_date.strftime("%d-%m-%Y")  
          
        cache = load_cache()  
        if today_str not in cache:  
            new_data = fetch_hijri_month(today_str)  
            if new_data: 
                cache.update(new_data)
                save_cache(cache)  

        if today_str not in cache:  
            safe_print({
                "text": I18N[lang]["error"], 
                "tooltip": I18N[lang]["no_connection"],
                "class": "error"
            })
            sys.exit(0)

        h_data = cache[today_str]  
        month_name = MONTHS_I18N[lang][h_data['month_number'] - 1]  
        day_idx = (today_date.weekday() + 1) % 7  
        weekday_full = I18N[lang]['weekdays'][day_idx]  

        first_day_idx = (day_idx - (h_data['day'] - 1)) % 7  
        calendar_days = f"{I18N[lang]['calendar_header']}\n" + "    " * first_day_idx  
          
        curr_col = first_day_idx  
        for i in range(1, h_data['month_length'] + 1):  
            cell = f"{i:2d}"  
            if i == h_data['day']:  
                calendar_days += f"<span color='#A6E3A1' weight='bold' underline='single'>{cell}</span>  "  
            else:  
                calendar_days += f"<span color='#CDD6F4'>{cell}</span>  "  
            curr_col += 1  
            if curr_col == 7:  
                calendar_days = calendar_days.rstrip() + "\n"  
                curr_col = 0  

        ev_list = []  
        if (h_data['month_number'], h_data['day']) in I18N[lang]["events"]:  
            ev_list.append(I18N[lang]["events"][(h_data['month_number'], h_data['day'])])  
        if h_data['day'] in [13, 14, 15] and not (h_data['month_number'] == 12 and h_data['day'] == 13):  
            ev_list.append(I18N[lang]["white_days"])  

        text = f"🌙 {h_data['day']} {month_name}"  
        tooltip = f"<span size='16000' weight='bold' color='#CBA6F7'>{h_data['day']} {month_name} {h_data['year']}\n{weekday_full}</span>\n\n<tt>{calendar_days.rstrip()}</tt>"  
        if ev_list:  
            tooltip += f"\n\n<span color='#F9E2AF' weight='bold'>🌟 {I18N[lang]['reminder']}: {' | '.join(ev_list)}</span>"  

        safe_print({"text": text, "tooltip": tooltip})

    except Exception as e:
        error_json = {
            "text": I18N.get(lang, I18N["ar"])["error"],
            "tooltip": f"فشل الاتصال بسبب:\n{str(e)}",
            "class": "error"
        }
        safe_print(error_json)
        sys.exit(0)

if __name__ == "__main__":
    main()
    