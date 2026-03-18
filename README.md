# waybar_hijri_calendar 🌙

A lightweight, zero-dependency Python script for Waybar. It displays the current Hijri date and features a perfectly aligned, dynamic monthly calendar grid in the tooltip. Supports multiple languages and uses optimized headers to solve Pango rendering issues. AI-generated based on my idea.

### ✨ Features

* 🌍 **Multi-language Support:** Choose between Arabic, English, French, German, or Italian.
* 📅 **Dynamic Month Length:** Accurately calculates and displays 29 or 30 days based on the actual Hijri month.
* ⚡ **Offline Caching:** Fetches data once per month and stores it locally (`~/.cache/waybar_hijri_cache.json`) for zero-lag performance and offline support.
* 🌟 **Authentic Islamic Events:** Displays reminders for authentic Sunnah occasions in the tooltip (e.g., White Days, Ramadan, Eids, Arafah).

---

## 🌐 Supported Languages

Use the `-lang` flag to change the display language. The default is Arabic.

| Flag | Language | Month Names | Weekday Headers |
| --- | --- | --- | --- |
| `-lang ar` | **Arabic** | العربية | Su Mo Tu... (Fixed for alignment) |
| `-lang en` | **English** | English | Su Mo Tu We Th Fr Sa |
| `-lang fr` | **French** | French | Di Lu Ma Me Je Ve Sa |
| `-lang de` | **German** | German | So Mo Di Mi Do Fr Sa |
| `-lang it` | **Italian** | Italian | Do Lu Ma Me Gi Ve Sa |

---

## ⚙️ Configuration

Add this to your Waybar config file (change `-lang ar` to your preferred language):

```json
"custom/hijri": {
    "format": "{}",
    "exec": "~/.config/waybar/scripts/hijri_waybar.py -lang ar",
    "return-type": "json",
    "interval": 3600,
    "tooltip": true
}

```

## 🎨 Styling

Add one of the following themes to your Waybar `style.css`:

### ☕ Catppuccin

```css
#custom-hijri {
    color: #f9e2af;          
    font-weight: bold;
    font-size: 14px;
    padding: 0 8px;
}

#custom-hijri:hover {
    color: #fab387;          
}
#custom-hijri.error {
    color: #f38ba8; 
    background-color: rgba(243, 139, 168, 0.1);
}
```

### 🎨 Dracula

```css
#custom-hijri {
    color: #bd93f9;          
    font-weight: bold;
    font-size: 14px;
    padding: 0 8px;
}

#custom-hijri:hover {
    color: #ff79c6;          
}
#custom-hijri.error {
    color: #f38ba8; 
    background-color: rgba(243, 139, 168, 0.1);
}

```

### ❄️ Nord

```css
#custom-hijri {
    color: #88C0D0;          
    font-weight: bold;
    font-size: 14px;
    padding: 0 8px;
}

#custom-hijri:hover {
    color: #81A1C1;          
}
#custom-hijri.error {
    color: #f38ba8; 
    background-color: rgba(243, 139, 168, 0.1);
}

```

### 📦 Gruvbox

```css
#custom-hijri {
    color: #fabd2f;          
    font-weight: bold;
    font-size: 14px;
    padding: 0 8px;
}

#custom-hijri:hover {
    color: #fe8019;          
}
#custom-hijri.error {
    color: #f38ba8; 
    background-color: rgba(243, 139, 168, 0.1);
}


```

### 🌃 Tokyo Night

```css
#custom-hijri {
    color: #7aa2f7;          
    font-weight: bold;
    font-size: 14px;
    padding: 0 8px;
}

#custom-hijri:hover {
    color: #bb9af7;          
}

```

## 🛠️ Installation

1. Create the script file: `~/.config/waybar/scripts/hijri_waybar.py`
2. Paste the Python code into the file.
3. Make it executable:

```bash
chmod +x ~/.config/waybar/scripts/hijri_waybar.py

```

4. **Critical:** If you are upgrading from a previous version, clear the old cache file to avoid errors:

```bash
rm ~/.cache/waybar_hijri_cache.json

```

5. Restart Waybar.

---

> **Note:** This tool was fully programmed by an AI Assistant based on my specific requirements and ideas. I'm sharing it to help others in the Linux community.