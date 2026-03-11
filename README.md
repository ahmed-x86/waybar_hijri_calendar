waybar_hijri_calendar 🌙

A lightweight, zero-dependency Python script for Waybar. It displays the current Hijri date and features a perfectly aligned, dynamic monthly calendar grid in the tooltip. Uses English weekdays to solve Pango RTL rendering issues. AI-generated based on my idea.
## ⚙️ Configuration

Add this to your Waybar config file:
```JSON
"custom/hijri": {
    "format": "{}",
    "exec": "~/.config/waybar/scripts/hijri_waybar.py",
    "return-type": "json",
    "interval": 3600,
    "tooltip": true
},
```
### for tetsing

## 🎨 Styling

Add this to your Waybar style.css for a Catppuccin-themed look:
```CSS
.custom-hijri {
    color: #f9e2af;          
    font-weight: bold;
    font-size: 14px;
    padding: 0 8px;
}

.custom-hijri:hover {
    color: #fab387;          
}
```
### 🛠️ Installation

Create the script file: ~/.config/waybar/scripts/hijri_waybar.py

Paste the Python code and make it executable:
```Bash
chmod +x ~/.config/waybar/scripts/hijri_waybar.py
```
Restart Waybar.

Note: This tool was fully programmed by an AI Assistant based on my specific requirements and ideas. I'm sharing it to help others in the Linux community.