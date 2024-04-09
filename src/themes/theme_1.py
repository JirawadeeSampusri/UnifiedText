class ThemeSwitcher:
    is_dark_mode = False
    web_view = None

    @staticmethod
    def set_web_view(web_view):
        ThemeSwitcher.web_view = web_view

    @staticmethod
    def toggle_dark_mode():
        ThemeSwitcher.is_dark_mode = not ThemeSwitcher.is_dark_mode
        ThemeSwitcher.apply_theme()

    @staticmethod
    def apply_theme():
        if ThemeSwitcher.web_view:
            script = f'''
                var style = document.createElement('style');
                style.textContent = `
                    body {{
                        background-color: {"#1e1e1e" if ThemeSwitcher.is_dark_mode else "#FFFFFF"};
                        color: {"#FFFFFF" if ThemeSwitcher.is_dark_mode else "#000000"};
                    }}
                    * {{
                        color: {"#FFFFFF" if ThemeSwitcher.is_dark_mode else "#000000"};
                    }}
                `;
                document.head.append(style);
            '''
            ThemeSwitcher.web_view.page().runJavaScript(script)
