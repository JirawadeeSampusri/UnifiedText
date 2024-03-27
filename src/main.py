import sys
import subprocess
from viewer.browser_widget import display_html_content

NETCACHE = "/home/parallels/Documents/offpunk/netcache.py"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        result = subprocess.run([NETCACHE, url], capture_output=True, text=True, check=True)
        html_content = result.stdout.strip()
        
        print("Content from", url)
        print(html_content)

        display_html_content(html_content)

    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
  