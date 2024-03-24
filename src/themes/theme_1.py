def toggle_dark_mode(web_view, is_dark_mode):
    script = f'''
    var style = document.createElement('style');
    style.textContent = `
        body {{
            background-color: {"#1e1e1e" if is_dark_mode else "#FFFFFF"};
            color: {"#FFFFFF" if is_dark_mode else "#000000"};
        }}
        * {{
            color: {"#FFFFFF" if is_dark_mode else "#000000"};
        }}
    `;
    document.head.append(style);
    '''
    web_view.page().runJavaScript(script)