import sys
import subprocess
from themes.browser_widget import display_html_content

NETCACHE = "/home/parallels/Documents/offpunk/netcache.py"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    cmd = [NETCACHE, url]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        html_content = result.stdout

        display_html_content(html_content)

    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)