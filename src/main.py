import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from viewer.browser_widget import display_html_content
from themes.theme_1 import ThemeSwitcher
from PyQt5.QtCore import QUrl, QTimer
from datetime import datetime

NETCACHE = "/home/parallels/Documents/offpunk/netcache.py"


class HTMLContentFetcher:
    @staticmethod
    def fetch_direct(url):
        try:
            result = subprocess.run(["curl", url], capture_output=True, text=True, check=True)
            return result.stdout.strip(), None
        except subprocess.CalledProcessError as e:
            print("Error fetching HTML content:", e)
            return None, None

    @staticmethod
    def fetch_from_cache(url):
        try:
            result = subprocess.run([NETCACHE, url], capture_output=True, text=True, check=True)
            html_content = result.stdout.strip()

            timestamp_result = subprocess.run([NETCACHE, url, "--timestamp"], capture_output=True, text=True,
                                              check=True)
            timestamp = timestamp_result.stdout.strip()

            return html_content, timestamp
        except subprocess.CalledProcessError as e:
            print("Error executing command:", e)
            return None, None  


def fetch_content(url):
    html_content, timestamp = HTMLContentFetcher.fetch_direct(url)
    if not html_content:
        html_content, timestamp = HTMLContentFetcher.fetch_from_cache(url)
    return html_content, timestamp


def handle_link_click(url, main_window, timestamp=None):
    global web_view, timestamp_label
    print("Fetching content for", url)
    html_content, timestamp = fetch_content(url)
    if html_content:
        if not web_view:
            create_web_view(html_content, url, main_window, timestamp)
        else:
            web_view.setHtml(html_content, baseUrl=QUrl(url))
            update_timestamp(timestamp)



def create_web_view(html_content, url, main_window, timestamp=None):
    global web_view, timestamp_label
    web_view = display_html_content(html_content, url, handle_link_click, main_window)
    ThemeSwitcher.set_web_view(web_view)
    web_view.loadFinished.connect(apply_theme)
    if timestamp:
        update_timestamp(timestamp)


def apply_theme():
    QTimer.singleShot(0, ThemeSwitcher.apply_theme)


def toggle_theme():
    ThemeSwitcher.toggle_dark_mode()


def back():
    web_view.page().triggerAction(QWebEnginePage.Back)


def forward():
    web_view.page().triggerAction(QWebEnginePage.Forward)


def update_timestamp(timestamp):
    global timestamp_label
    timestamp_label.setText("Last Updated: " + datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))


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


    timestamp_label = QLabel()
    toolbar.addWidget(timestamp_label)

    # Initial Setting
    is_dark_mode = False
    web_view = None

    handle_link_click(url, main_window)
    main_window.show()

    sys.exit(app.exec_())
