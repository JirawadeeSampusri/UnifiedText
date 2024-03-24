# test_webengineview.py

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

def main():
    app = QApplication(sys.argv)
    
    # Create a QWebEngineView instance
    webview = QWebEngineView()
    
    # Load some simple HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test HTML</title>
    </head>
    <body>
        <h1>Hello, HTML!</h1>
        <p>This is a test paragraph.</p>
    </body>
    </html>
    """
    webview.setHtml(html_content)
    
    # Show the webview
    webview.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
