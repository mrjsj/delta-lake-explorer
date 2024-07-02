from code_editor import code_editor
import sys

def load_code_editor():

    cmd_button_text = "Cmd-Enter" if sys.platform == "darwin" else "Ctrl-Enter"        

    custom_btns = [
        {
            "name": f"{cmd_button_text} to execute",
            "hasText": True,
            "alwaysOn": True,
            "commands": [
                "submit"
            ],
            "style": {
                "fontSize": "0.8rem",
                "position": "fixed",
                "bottom": "0.1rem",
                "right": "0.1rem",
                "zIndex": "1000"
            }
        }
    ]

    code_editor(
        key="query",
        code="",
        lang="sql",
        height="300px",
        theme="dracula",
        buttons=custom_btns
    )