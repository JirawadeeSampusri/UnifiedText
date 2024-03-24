from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

from themes.theme_1 import toggle_dark_mode

def display_html_content(html_content):
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("UnifiedText")
    window.setGeometry(100, 100, 800, 600)

    web_view = QWebEngineView()
    web_view.setHtml(html_content)

    layout = QVBoxLayout()
    layout.addWidget(web_view)

    central_widget = QWidget()
    central_widget.setLayout(layout)

    window.setCentralWidget(central_widget)

    # toolbar
    nav_toolbar = QToolBar()
    back_action = QAction("<", window)
    back_action.triggered.connect(web_view.back)
    forward_action = QAction(">", window)
    forward_action.triggered.connect(web_view.forward)
    # refresh_action = QAction("Refresh", window)
    # refresh_action.triggered.connect(web_view.reload)
    dark_mode_action = QAction("Dark", window)
    dark_mode_action.triggered.connect(lambda: toggle_dark_mode(web_view, True))
    normal_mode_action = QAction("Normal", window)
    normal_mode_action.triggered.connect(lambda: toggle_dark_mode(web_view, False))
    nav_toolbar.addAction(back_action)
    nav_toolbar.addAction(forward_action)
    # nav_toolbar.addAction(refresh_action)
    nav_toolbar.addAction(dark_mode_action)
    nav_toolbar.addAction(normal_mode_action)
    window.addToolBar(nav_toolbar)

    window.show()

    sys.exit(app.exec_())





