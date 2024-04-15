from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import QUrl, QTimer
from datetime import datetime
import subprocess
import sys,re
from viewer.browser_widget import display_html_content
from themes.theme_1 import ThemeSwitcher

NETCACHE = "/home/parallels/Documents/offpunk/netcache.py"

class HTMLContentFetcher:
    @staticmethod
    def fetch_direct(url):
        try:
            result = subprocess.run(["curl", url], capture_output=True, text=True, check=True)
            return result.stdout.strip(), ''
        except subprocess.CalledProcessError as e:
            print("Error fetching HTML content:", e)
            return None, None


    def fetch_from_cache(url, force_refresh=False):
        try:
            def run_netcache_command(args):
                result = subprocess.run([NETCACHE, url] + args, capture_output=True, text=True, check=True)
                return result.stdout.strip()
            
            html_content = run_netcache_command([])

            if force_refresh or "Cache invalid" in run_netcache_command(["--cacheStatus"]):
                html_content = run_netcache_command(["--cache-validity", "1"])

            cache_status = run_netcache_command(["--cacheStatus"])

            return html_content, cache_status
            
        except subprocess.CalledProcessError as e:
            print("Error executing command:", e)
            return None, None


def fetch_content(url, force_refresh=False):
    html_content , cache_status = HTMLContentFetcher.fetch_direct(url)
    if not html_content:
        html_content, cache_status = HTMLContentFetcher.fetch_from_cache(url, force_refresh=force_refresh)
    return html_content, cache_status
 

def handle_link_click(url, main_window, cache_status=None):
    global web_view,  cache_status_label
    print("Fetching content for", url)

    html_content, cache_status = fetch_content(url)
   
    if html_content:
        if not web_view:
            create_web_view(html_content, url, main_window)
        else:
            web_view.setHtml(html_content, baseUrl=QUrl(url))

        update_cache_status(cache_status)
    else:
        print("Error fetching content for", url)
        update_cache_status(cache_status)

  

def create_web_view(html_content, url, main_window):
    global web_view
    web_view = display_html_content(html_content, url, handle_link_click, main_window)
    ThemeSwitcher.set_web_view(web_view)
    web_view.loadFinished.connect(apply_theme)


def apply_theme():
    QTimer.singleShot(0, ThemeSwitcher.apply_theme)


def toggle_theme():
    ThemeSwitcher.toggle_dark_mode()


def back():
    web_view.page().triggerAction(QWebEnginePage.Back)


def forward():
    web_view.page().triggerAction(QWebEnginePage.Forward)


def refresh():
    global web_view, cache_status_label
    url = web_view.url().toString() if web_view else ""
    
    html_content, cache_status = fetch_content(url, force_refresh=True)

    if html_content:
        if not web_view:
            create_web_view(html_content, url, main_window)
        else:
            web_view.setHtml(html_content, baseUrl=QUrl(url))

        update_cache_status(cache_status)
    else:
        print("Error fetching content for", url)
        update_cache_status(cache_status)


def update_cache_status(cache_status):
    global cache_status_label

    timestamp_match = re.search(r'Timestamp:\s*([\d.]+)', cache_status)
  
    if timestamp_match:
        timestamp = float(timestamp_match.group(1))
        timestamp_formatted = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        cache_status_label.setText(f"Cache Status: \nLast Updated: {timestamp_formatted}\n {cache_status.splitlines()[2]} ")
    else:

        cache_status_label.setText("Cache Status: " + cache_status)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <URL>")
        sys.exit(1)

    app = QApplication(sys.argv)
    url = sys.argv[1]

    main_window = QMainWindow()
    main_window.setWindowTitle("Browser")

    back_action = QAction("Back", main_window)
    back_action.triggered.connect(back)
    forward_action = QAction("Forward", main_window)
    forward_action.triggered.connect(forward)

    theme_action = QAction("Toggle Theme", main_window)
    theme_action.triggered.connect(toggle_theme)

    toolbar = main_window.addToolBar("Navigation")
    toolbar.addAction(back_action)
    toolbar.addAction(forward_action)
    toolbar.addAction(theme_action)

    refresh_action = QAction("Refresh", main_window)
    refresh_action.triggered.connect(refresh)
    toolbar.addAction(refresh_action)

    cache_status_label = QLabel()
    toolbar.addWidget(cache_status_label)

    # Initial Setting
    is_dark_mode = False
    web_view = None


    handle_link_click(url, main_window)

    main_window.show()
    

    sys.exit(app.exec_())