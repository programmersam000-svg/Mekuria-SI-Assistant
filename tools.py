"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║         Tools & Actions  — The Execution Layer               ║
╚══════════════════════════════════════════════════════════════╝
Comprehensive tool suite for Mekuria: system controls, telemetry,
web searching, weather, news, wikipedia, local file search, alarms,
media playback, screenshotting, clipboard, and math calculation.
"""

import datetime
import math
import os
import platform
import re
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from typing import Optional

# Enforce UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console

console = Console()


# ══════════════════════════════════════════════════════════════════
#  1. SYSTEM TELEMETRY & STATUS
# ══════════════════════════════════════════════════════════════════

def get_time_and_date() -> str:
    """Return the current date, time, and day of the week."""
    now = datetime.datetime.now()
    return now.strftime("It is %A, %B %d, %Y, and the time is %I:%M:%S %p.")


def get_system_telemetry() -> str:
    """Gather real-time system metrics (CPU, RAM, Disk, OS version)."""
    uname = platform.uname()

    ps_cmd = (
        "$mem = Get-CimInstance Win32_OperatingSystem; "
        "$disk = Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='C:'\"; "
        "$freeRamGB = [math]::Round($mem.FreePhysicalMemory / 1MB, 2); "
        "$totalRamGB = [math]::Round($mem.TotalVisibleMemorySize / 1MB, 2); "
        "$usedRamPct = [math]::Round((($totalRamGB - $freeRamGB) / $totalRamGB) * 100, 1); "
        "$freeDiskGB = [math]::Round($disk.FreeSpace / 1GB, 2); "
        "$totalDiskGB = [math]::Round($disk.Size / 1GB, 2); "
        "Write-Output \"RAM: ${freeRamGB}GB free of ${totalRamGB}GB (${usedRamPct}% used) | C: Drive: ${freeDiskGB}GB free of ${totalDiskGB}GB\""
    )

    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True, text=True, timeout=10
        )
        telemetry_str = res.stdout.strip() if res.returncode == 0 else "Metrics unavailable."
    except Exception:
        telemetry_str = "Metrics unavailable."

    return (
        f"System: {uname.system} {uname.release} ({uname.machine}) | "
        f"Processor: {uname.processor} | "
        f"Computer Name: {uname.node} | "
        f"{telemetry_str}"
    )


# ══════════════════════════════════════════════════════════════════
#  2. WEATHER & ONLINE INFORMATION (NO API KEYS REQUIRED)
# ══════════════════════════════════════════════════════════════════

def get_weather(city: str = "") -> str:
    """Fetch current weather and forecast for any city using wttr.in."""
    location = urllib.parse.quote(city.strip()) if city else ""
    url = f"https://wttr.in/{location}?format=3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            weather_data = response.read().decode("utf-8").strip()
            if weather_data:
                return f"Weather report: {weather_data}"
    except Exception as e:
        return f"Could not fetch weather data: {e}"
    return "Weather information currently unavailable."


def search_wikipedia(query: str) -> str:
    """Search Wikipedia for a topic and return a brief summary."""
    if not query:
        return "Please specify a topic to search on Wikipedia."
    clean_query = urllib.parse.quote(query.strip())
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_query}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MekuriaAI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            import json
            data = json.loads(response.read().decode("utf-8"))
            extract = data.get("extract")
            if extract:
                return f"According to Wikipedia: {extract[:300]}..."
    except Exception:
        pass
    return f"I couldn't find a direct summary for '{query}' on Wikipedia."


def get_news_headlines() -> str:
    """Fetch recent top news headlines."""
    url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as response:
            content = response.read().decode("utf-8")
            titles = re.findall(r"<title>(.*?)</title>", content)
            # Skip the main channel title
            headlines = [t for t in titles[1:6] if not t.startswith("Google News")]
            if headlines:
                return "Top Headlines: " + " | ".join(headlines)
    except Exception as e:
        return f"Could not fetch news headlines: {e}"
    return "News headlines currently unavailable."


# ══════════════════════════════════════════════════════════════════
#  3. TIMER & ALARM (BACKGROUND REMINDERS)
# ══════════════════════════════════════════════════════════════════

def set_timer(seconds: int = 60, message: str = "Timer is up!") -> str:
    """Set a background timer that alerts the user out loud when finished."""
    import tts

    def _timer_worker():
        time.sleep(seconds)
        alert_text = f"Attention user: Your timer for {message} has completed!"
        console.print(f"[bold red]⏰ ALARM:[/bold red] {alert_text}")
        tts.speak(alert_text)

    t = threading.Thread(target=_timer_worker, daemon=True)
    t.start()
    return f"Timer set for {seconds} seconds ({message})."


# ══════════════════════════════════════════════════════════════════
#  4. APPLICATION LAUNCHER
# ══════════════════════════════════════════════════════════════════

APP_MAP = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "files": "explorer.exe",
    "task manager": "taskmgr.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "terminal": "wt.exe",
    "powershell": "powershell.exe",
    "settings": "ms-settings:",
    "control panel": "control.exe",
    "snipping tool": "snippingtool.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "browser": "https://www.google.com",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "spotify": "spotify.exe",
    "vscode": "code",
    "code": "code",
}


def open_application(app_name: str) -> str:
    """Launch a Windows desktop application by name."""
    if not app_name:
        return "Please specify an application name."

    key = app_name.lower().strip()
    executable = APP_MAP.get(key)

    try:
        if executable:
            if executable.startswith("http"):
                webbrowser.open(executable)
            elif executable.startswith("ms-"):
                os.startfile(executable)
            else:
                subprocess.Popen(executable, shell=True)
            return f"Opening {app_name} now."
        else:
            subprocess.Popen(app_name, shell=True)
            return f"Attempting to launch '{app_name}'."
    except Exception as e:
        return f"Could not launch '{app_name}'. Error: {e}"


# ══════════════════════════════════════════════════════════════════
#  5. WEB SEARCH & MEDIA
# ══════════════════════════════════════════════════════════════════

def search_web(query: str) -> str:
    """Search Google in the user's default browser."""
    if not query:
        return "Please specify a query to search for."
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Opened Google search for '{query}'."


def open_website(url: str) -> str:
    """Navigate to a specified web address."""
    if not url:
        return "Please specify a website URL."
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened website {url}."


def play_youtube(search_term: str) -> str:
    """Play a video or music track on YouTube."""
    if not search_term:
        return "Please specify what you would like to play."
    url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching YouTube for '{search_term}'."


# ══════════════════════════════════════════════════════════════════
#  6. LOCAL FILE SEARCH
# ══════════════════════════════════════════════════════════════════

def search_local_files(query: str) -> str:
    """Search for files on Desktop and Downloads by name."""
    if not query:
        return "Please specify a file name to search for."

    search_dirs = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Documents"),
    ]

    matches = []
    clean_q = query.lower()

    for d in search_dirs:
        if os.path.exists(d):
            try:
                for root, dirs, files in os.walk(d):
                    for f in files:
                        if clean_q in f.lower():
                            matches.append(os.path.join(root, f))
                            if len(matches) >= 5:
                                break
                    if len(matches) >= 5:
                        break
            except Exception:
                pass

    if matches:
        return f"Found matching files: " + ", ".join(os.path.basename(m) for m in matches)
    return f"No local files found matching '{query}' on Desktop or Downloads."


# ══════════════════════════════════════════════════════════════════
#  7. SYSTEM AUDIO & VOLUME
# ══════════════════════════════════════════════════════════════════

def set_volume(level: int) -> str:
    """Set system audio volume (0 to 100)."""
    try:
        vol = max(0, min(100, int(level)))
        script = (
            "$wshShell = New-Object -ComObject WScript.Shell; "
            "1..50 | ForEach-Object { $wshShell.SendKeys([char]174) }; "
            f"1..{vol // 2} | ForEach-Object {{ $wshShell.SendKeys([char]175) }}"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True)
        return f"System volume set to {vol}%."
    except Exception as e:
        return f"Failed to set volume: {e}"


def mute_volume() -> str:
    """Toggle mute on system audio."""
    try:
        script = "$wshShell = New-Object -ComObject WScript.Shell; $wshShell.SendKeys([char]173)"
        subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True)
        return "System audio muted."
    except Exception as e:
        return f"Failed to mute audio: {e}"


# ══════════════════════════════════════════════════════════════════
#  8. SCREENSHOT CAPTURE
# ══════════════════════════════════════════════════════════════════

def take_screenshot() -> str:
    """Capture a full-screen screenshot and save it to the Desktop."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(desktop, filename)

    ps_script = (
        "Add-Type -AssemblyName System.Windows.Forms, System.Drawing; "
        "$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
        "$bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height; "
        "$graphics = [System.Drawing.Graphics]::FromImage($bitmap); "
        "$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size); "
        f"$bitmap.Save('{filepath.replace('\\', '/')}'); "
        "$graphics.Dispose(); $bitmap.Dispose()"
    )

    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
        if os.path.exists(filepath):
            return f"Screenshot saved to your Desktop as '{filename}'."
        return f"Screenshot capture completed. File location: {filepath}"
    except Exception as e:
        return f"Failed to take screenshot: {e}"


# ══════════════════════════════════════════════════════════════════
#  9. CLIPBOARD OPERATIONS
# ══════════════════════════════════════════════════════════════════

def get_clipboard() -> str:
    """Read current text content from the Windows clipboard."""
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
            capture_output=True, text=True
        )
        content = res.stdout.strip()
        if content:
            return f"Clipboard text: \"{content}\""
        return "Clipboard is empty."
    except Exception as e:
        return f"Could not read clipboard: {e}"


def set_clipboard(text: str) -> str:
    """Copy text to the Windows clipboard."""
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value \"{text}\""],
            capture_output=True
        )
        return f"Copied text to clipboard."
    except Exception as e:
        return f"Could not write to clipboard: {e}"


# ══════════════════════════════════════════════════════════════════
#  10. UTILITIES (MATH & HUMOR)
# ══════════════════════════════════════════════════════════════════

def calculate_math(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    allowed_names = {
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "sqrt": math.sqrt, "log": math.log, "pi": math.pi, "e": math.e,
        "pow": math.pow, "abs": abs, "round": round
    }
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"The result of {expression} is {result}."
    except Exception as e:
        return f"Invalid mathematical expression: {e}"


def tell_joke() -> str:
    """Return a witty quip."""
    import random
    jokes = [
        "I'd tell you a UDP joke, but you might not get it.",
        "There are 10 types of people in the world: those who understand binary and those who don't.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "I'm not saying I'm efficient, but I optimized my routine to O(1).",
        "A SQL query walks into a bar, sees two tables, and asks: 'Can I JOIN you?'",
        "I would make a joke about recursion, but first I'd need to make a joke about recursion.",
    ]
    return random.choice(jokes)


# ══════════════════════════════════════════════════════════════════
#  11. TOOL REGISTRY & MATCHER
# ══════════════════════════════════════════════════════════════════

TOOLS_MAP = {
    "get_time_and_date": get_time_and_date,
    "get_system_telemetry": get_system_telemetry,
    "get_weather": get_weather,
    "search_wikipedia": search_wikipedia,
    "get_news_headlines": get_news_headlines,
    "set_timer": set_timer,
    "open_application": open_application,
    "search_web": search_web,
    "open_website": open_website,
    "play_youtube": play_youtube,
    "search_local_files": search_local_files,
    "set_volume": set_volume,
    "mute_volume": mute_volume,
    "take_screenshot": take_screenshot,
    "get_clipboard": get_clipboard,
    "set_clipboard": set_clipboard,
    "calculate_math": calculate_math,
    "tell_joke": tell_joke,
}

KEYWORD_RULES = [
    (["time", "date", "clock", "what day", "today"], get_time_and_date, {}),
    (["weather", "temperature", "forecast", "climate"], get_weather, {}),
    (["wikipedia", "wiki", "who is", "what is"], search_wikipedia, {}),
    (["news", "headlines", "latest news", "current events"], get_news_headlines, {}),
    (["system", "telemetry", "specs", "ram", "cpu", "memory", "battery", "status"], get_system_telemetry, {}),
    (["screenshot", "snip", "capture screen"], take_screenshot, {}),
    (["mute", "silence audio"], mute_volume, {}),
    (["clipboard", "paste text"], get_clipboard, {}),
    (["find file", "search file", "locate file"], search_local_files, {}),
    (["joke", "humor", "funny"], tell_joke, {}),
]


def match_tool(user_input: str):
    """Fallback keyword matcher for natural language input."""
    lower = user_input.lower()
    for keywords, func, params in KEYWORD_RULES:
        if any(k in lower for k in keywords):
            return func.__name__, func
    return None, None


def execute_tool(tool_name: str, user_input: str) -> str:
    """Execute tool by name and extract arguments if needed."""
    func = TOOLS_MAP.get(tool_name)
    if not func:
        return f"Unknown action '{tool_name}'."

    lower = user_input.lower()

    if tool_name == "get_weather":
        for trigger in ["weather in ", "weather for ", "temperature in "]:
            if trigger in lower:
                city = lower.split(trigger, 1)[1].strip().rstrip(".")
                return func(city=city)
        return func(city="")

    elif tool_name == "search_wikipedia":
        for trigger in ["wikipedia ", "wiki ", "who is ", "what is "]:
            if trigger in lower:
                q = lower.split(trigger, 1)[1].strip().rstrip(".")
                return func(query=q)
        return func(query=user_input)

    elif tool_name == "set_timer":
        nums = re.findall(r"\d+", user_input)
        secs = int(nums[0]) * 60 if "minute" in lower else (int(nums[0]) if nums else 60)
        return func(seconds=secs, message=user_input)

    elif tool_name == "search_local_files":
        for trigger in ["file ", "search file ", "find file "]:
            if trigger in lower:
                q = lower.split(trigger, 1)[1].strip().rstrip(".")
                return func(query=q)
        return func(query=user_input)

    elif tool_name == "open_application":
        for trigger in ["open ", "launch ", "start ", "run "]:
            if trigger in lower:
                app = lower.split(trigger, 1)[1].strip().rstrip(".")
                return func(app_name=app)
        return func(app_name=user_input)

    elif tool_name == "search_web":
        for trigger in ["search for ", "search ", "google ", "look up "]:
            if trigger in lower:
                query = lower.split(trigger, 1)[1].strip().rstrip(".")
                return func(query=query)
        return func(query=user_input)

    elif tool_name == "play_youtube":
        for trigger in ["play ", "youtube "]:
            if trigger in lower:
                term = lower.split(trigger, 1)[1].strip().rstrip(".")
                return func(search_term=term)
        return func(search_term=user_input)

    elif tool_name == "set_volume":
        nums = re.findall(r"\d+", user_input)
        level = int(nums[0]) if nums else 50
        return func(level=level)

    elif tool_name == "open_website":
        words = user_input.split()
        for w in words:
            if "." in w and len(w) > 3:
                return func(url=w.strip(".,!?"))
        return func(url="https://google.com")

    elif tool_name == "calculate_math":
        expr = re.sub(r"[^\d\+\-\*\/\(\)\.\s\^]", "", user_input).strip()
        return func(expression=expr) if expr else "No valid expression found."

    else:
        return func()
