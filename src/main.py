import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow
from viewer.browser_widget import display_html_content

NETCACHE = "/home/parallels/Documents/offpunk/netcache.py"

class HTMLContentFetcher:
    @staticmethod
    def fetch_direct(url):
        try:
            result = subprocess.run(["curl", url], capture_output=True, text=True, check=True)
            html_content = result.stdout.strip()
            return html_content
        except subprocess.CalledProcessError as e:
            print("Error fetching HTML content:", e)
            return None

    @staticmethod
    def fetch_from_cache(url):
        try:
            result = subprocess.run([NETCACHE, url], capture_output=True, text=True, check=True)
            html_content = result.stdout.strip()
            print("Content from", url)
            print(html_content)
            return html_content
        except subprocess.CalledProcessError as e:
            print("Error executing command:", e)
            return None

def handle_link_click(url):
    html_content = HTMLContentFetcher.fetch_direct(url)
    if not html_content:
        html_content = HTMLContentFetcher.fetch_from_cache(url)
    if html_content:
        display_html_content(html_content, url, handle_link_click, main_window)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <URL>")
        sys.exit(1)

    app = QApplication(sys.argv)
    url = sys.argv[1]

    main_window = QMainWindow()
    handle_link_click(url)
    main_window.show()

    sys.exit(app.exec_())