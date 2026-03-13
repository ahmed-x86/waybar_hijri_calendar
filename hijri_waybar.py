#!/usr/bin/env python3

import json
import datetime
import urllib.request
import sys
import os

# مسار ملف التخزين (الملف النصي)
CACHE_FILE = os.path.expanduser("~/.cache/waybar_hijri_cache.json")

def load_cache():
    """قراءة البيانات من ملف التخزين إن وجد"""
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_cache(cache_data):
    """حفظ البيانات في ملف التخزين"""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def fetch_hijri_month(date_str):
    """جلب بيانات الشهر الهجري بالكامل من الإنترنت بناءً على تاريخ اليوم"""
    try:
        
        url_today = f"https://api.aladhan.com/v1/gToH?date={date_str}"
        req1 = urllib.request.Request(url_today, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req1, timeout=5) as response1:
            today_data = json.loads(response1.read().decode('utf-8'))
            h_month = today_data['data']['hijri']['month']['number']
            h_year = today_data['data']['hijri']['year']

        
        url_month = f"https://api.aladhan.com/v1/hToGCalendar/{h_month}/{h_year}"
        req2 = urllib.request.Request(url_month, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req2, timeout=5) as response2:
            month_data = json.loads(response2.read().decode('utf-8'))
            
        new_cache = {}
        days_list = month_data.get('data', [])
        month_length = len(days_list)
        
        for item in days_list:
            g_date = item['gregorian']['date']
            hijri = item['hijri']
            new_cache[g_date] = {
                "day": int(hijri['day']),
                "month_name": hijri['month']['ar'],
                "month_number": int(hijri['month']['number']),
                "year": hijri['year'],
                "weekday_ar": hijri['weekday']['ar'],
                "month_length": month_length
            }
        return new_cache
    except Exception:
        return None

def get_hijri_date():
    today_date = datetime.datetime.now()
    today_str = today_date.strftime("%d-%m-%Y")
    py_weekday = today_date.weekday()
    
    cache = load_cache()
    
    if today_str not in cache:

        new_data = fetch_hijri_month(today_str)
        if new_data:
            cache.update(new_data)
            save_cache(cache)
            
    if today_str in cache:
        h_data = cache[today_str]
        month_length = h_data.get("month_length", 30)
        month_number = h_data.get("month_number", 1) 
        return h_data['day'], h_data['month_name'], month_number, h_data['year'], h_data['weekday_ar'], py_weekday, month_length
        
    return None, None, None, None, None, None, None

def get_hijri_event(month, day):
    """دالة لمعرفة المناسبات الشرعية بناءً على اليوم والشهر"""
    events = []
    
    
    fixed_events = {
        (1, 9): "صيام تاسوعاء 🌙",
        (1, 10): "صيام عاشوراء 🌙",
        (9, 1): "أول أيام شهر رمضان 🌙",
        (9, 21): "ليلة وترية (العشر الأواخر) 🤲",
        (9, 23): "ليلة وترية (العشر الأواخر) 🤲",
        (9, 25): "ليلة وترية (العشر الأواخر) 🤲",
        (9, 27): "ليلة القدر (أرجح الأقوال) 🤲✨",
        (9, 29): "ليلة وترية (العشر الأواخر) 🤲",
        (10, 1): "عيد الفطر المبارك 🎉",
        (12, 8): "يوم التروية 🕋",
        (12, 9): "يوم عرفة 🤲",
        (12, 10): "عيد الأضحى المبارك 🐑",
        (12, 11): "أول أيام التشريق",
        (12, 12): "ثاني أيام التشريق",
        (12, 13): "ثالث أيام التشريق",
    }
    
    if (month, day) in fixed_events:
        events.append(fixed_events[(month, day)])
        
    
    if day in [13, 14, 15] and not (month == 12 and day == 13):
        events.append("صيام الأيام البيض ⚪")
        
    return " | ".join(events) if events else None

def main():
    result = get_hijri_date()
    if result[0] is None:
        print(json.dumps({
            "text": "🌙 خطأ",
            "tooltip": "لا يوجد اتصال بالإنترنت ولم يتم العثور على بيانات سابقة مسجلة لهذا اليوم."
        }))
        sys.exit(1)
        
    day, month_name, month_number, year, weekday_ar, py_weekday, month_length = result
    
    today_idx = (py_weekday + 1) % 7
    first_day_idx = (today_idx - (day - 1)) % 7
    
    calendar_days = "Su  Mo  Tu  We  Th  Fr  Sa\n"
    calendar_days += "    " * first_day_idx

    current_col = first_day_idx
    
    for i in range(1, month_length + 1):
        formatted_day = f"{i:2d}"
        
        if i == day:
            calendar_days += f"<span color='#A6E3A1' weight='bold' underline='single'>{formatted_day}</span>  "
        else:
            calendar_days += f"<span color='#CDD6F4'>{formatted_day}</span>  "
            
        current_col += 1
        if current_col == 7:
            calendar_days += "\n"
            current_col = 0

    text = f"🌙 {day} {month_name}"
    
    tooltip = f"<span size='16000' weight='bold' color='#CBA6F7'>{day} {month_name} {year}\n{weekday_ar}</span>\n\n<tt>{calendar_days.rstrip()}</tt>"
    
    today_event = get_hijri_event(month_number, day)
    if today_event:
        tooltip += f"\n\n<span color='#F9E2AF' weight='bold'>🌟 تذكير: {today_event}</span>"

    waybar_output = {
        "text": text,
        "tooltip": tooltip
    }
    
    print(json.dumps(waybar_output, ensure_ascii=False))

if __name__ == "__main__":
    main()