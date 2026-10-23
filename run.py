import sys
import os
from streamlit.web import cli as stcli

def main():
    # PyInstaller ideiglenes könyvtárának (MEIPASS) megkeresése
    if getattr(sys, 'frozen', False):
        dirname = sys._MEIPASS
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
        
    script_path = os.path.join(dirname, 'app.py')
    
    # Streamlit indítása közvetlenül a becsomagolt környezetből
    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())

if __name__ == '__main__':
    main()