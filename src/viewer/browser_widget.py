from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon

from themes.theme_1 import ThemeSwitcher

def display_html_content(html_content, url, callback=None, main_window=None):
    class CustomWebEnginePage(QWebEnginePage):
        def acceptNavigationRequest(self, url, _type, is_main_frame):
            if is_main_frame and _type == QWebEnginePage.NavigationTypeLinkClicked:
                if callback:
                    callback(url.toString(), main_window)
                return False
            return super().acceptNavigationRequest(url, _type, is_main_frame)

    web_view = QWebEngineView()
    web_view.setPage(CustomWebEnginePage(web_view))

    ThemeSwitcher.set_web_view(web_view)
    ThemeSwitcher.apply_theme()

    web_view.setStyleSheet("background-color: #2C3E50; color: #ECF0F1;")

    web_view.setHtml(html_content, baseUrl=QUrl(url))
   

    layout = QVBoxLayout()
    layout.addWidget(web_view)

    central_widget = QWidget()
    central_widget.setLayout(layout)

    main_window.setCentralWidget(central_widget)

    main_window.setStyleSheet("background-color: #2C3E50; color: #ECF0F1;")
    main_window.setWindowIcon(QIcon("icon.png")) 
    main_window.setWindowTitle(f"UnifiedText")

    main_window.show()

    return web_view



