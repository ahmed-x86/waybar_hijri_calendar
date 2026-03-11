#!/usr/bin/env python3

import json
import datetime
import urllib.request
import urllib.error
import sys

def get_hijri_date():
    today_date = datetime.datetime.now()
    today_str = today_date.strftime("%d-%m-%Y")
    url = f"https://api.aladhan.com/v1/gToH/{today_str}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        hijri = data['data']['hijri']
        day = int(hijri['day'])
        month_name = hijri['month']['ar']
        year = hijri['year']
        weekday_ar = hijri['weekday']['ar']
        
        py_weekday = today_date.weekday()
        
        return day, month_name, year, weekday_ar, py_weekday
        
    except (urllib.error.URLError, KeyError, ValueError):
        return None, None, None, None, None

def main():
    result = get_hijri_date()
    if result[0] is None:
        print(json.dumps({
            "text": "🌙 خطأ",
            "tooltip": "تعذر جلب التاريخ (تأكد من الاتصال بالإنترنت)"
        }))
        sys.exit(1)
        
    day, month_name, year, weekday_ar, py_weekday = result

    
    today_idx = (py_weekday + 1) % 7
    first_day_idx = (today_idx - (day - 1)) % 7

    
    calendar_days = "Su  Mo  Tu  We  Th  Fr  Sa\n"
    
   
    calendar_days += "    " * first_day_idx

    current_col = first_day_idx
    for i in range(1, 31):
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

    waybar_output = {
        "text": text,
        "tooltip": tooltip
    }
    
    print(json.dumps(waybar_output, ensure_ascii=False))

if __name__ == "__main__":
    main()