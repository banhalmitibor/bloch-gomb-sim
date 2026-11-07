import sys
import os
import time
import webbrowser
from threading import Thread

if __name__ == '__main__':
    # 1. Beállítjuk a PyInstaller ideiglenes kicsomagolási útvonalát gyökérkönyvtárként
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(bundle_dir)
    app_path = os.path.join(bundle_dir, "app.py")

    # 2. Automatikus böngészőnyitás késleltetve
    def open_browser():
        time.sleep(2.5)
        webbrowser.open("http://127.0.0.1:8501")

    Thread(target=open_browser, daemon=True).start()

    # 3. Streamlit CLI indítása a beállított paraméterekkel
    import streamlit.web.cli as stcli

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=true",
        "--server.address=127.0.0.1",
        "--server.port=8501",
        "--browser.gatherUsageStats=false"
    ]
    sys.exit(stcli.main())