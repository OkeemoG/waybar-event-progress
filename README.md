# waybar-event-progress
A small Python utility that fetches iCal events, computes the progress of ongoing appointments, and outputs a JSON-formatted string for display in a Waybar custom widget.

## Overview
This project provides a lightweight script that periodically retrieves an iCal feed, detects whether an event is currently ongoing, and calculates its progress based on start and end timestamps.  
The script prints a JSON object suitable for consumption by a Waybar custom module.

## How It Works
The script:
1. Downloads the calendar data from the configured iCal URL.  
2. Identifies events that are active at the current time.  
3. Calculates the percentage of elapsed time.  
4. Builds a simple text-based progress bar.  
5. Outputs the information as JSON to Waybar.

## Installation

This project uses a Python virtual environment to keep dependencies isolated.  
Follow the steps below to set up everything after cloning the repository.

### 1. Clone the repository
```bash
git clone https://github.com/OkeemoG/waybar-event-progress
cd <waybar-event-progress>
```
### 2. Create a virtual environment
```bash
python3 -m venv ~/.config/waybar/scripts/venv
```
### 3. Activate the virtual environment
#### Bash / Zsh / Sh
```bash
source ~/.config/waybar/scripts/venv/bin/activate
```
#### Fish
```fish
source ~/.config/waybar/scripts/venv/bin/activate.fish
```
### 4. Install the dependencies
```bash
pip install -r requirements.txt
```
### 5. Install Waybar integration
Copy the script to your Waybar configuration directory:
```bash
mkdir -p ~/.config/waybar/scripts/ical_progress
cp scripts/ical_progress/ical_progress.py ~/.config/waybar/scripts/ical_progress/ical_progress.py
chmod +x ~/.config/waybar/scripts/ical_progress/ical_progress.py
```
Add the following block to your Waybar config:
```json
"custom/progress": {
        "format": "{}",
        "exec": "~/.config/waybar/scripts/ical_progress.py",
        "return-type": "json"
}
```
### 6. Configure the script
Open the script and adjust:
```bash
#!/home/<user>/.config/waybar/scripts/venv/bin/python

ICAL_URL = "https://example.com/calendar.ics"
TIMEZONE = tz.gettz("Your/Timezone")
```
After saving the changes, reload Waybar. The progress of the current event should now appear in your bar.