import subprocess
import re


def get_wifi_password(ssid):
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles', 'name=' + ssid, 'key=clear'], capture_output=True, text=True)
        output = result.stdout

        # Find the key content line
        key_content_line = re.search(r'Key Content\s*:\s*(.+)', output)
        if key_content_line:
            return key_content_line.group(1)
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_connected_wifi_info():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        output = result.stdout

        if "SSID" not in output:
            print("No Wi-Fi connection detected.")
            return

        ssid = None
        bssid = None
        signal = None
        security_type = None

        for line in output.split('\n'):
            if "SSID" in line and not ssid:
                ssid = line.split(":")[1].strip()
            elif "BSSID" in line:
                bssid = line.split(":")[1].strip()
            elif "Signal" in line:
                signal = line.split(":")[1].strip()
            elif "Authentication" in line:
                security_type = line.split(":")[1].strip()

        password = get_wifi_password(ssid)

        print(f"SSID: {ssid}")
        print(f"BSSID: {bssid}")
        print(f"Signal Strength: {signal}")
        print(f"Security Type: {security_type}")
        print(f"Password: {password}")

    except Exception as e:
        print(f"Error: {e}")


get_connected_wifi_info()
