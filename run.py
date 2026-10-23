import os
import sys
import subprocess

def main():
    # Megkeresi az app.py helyét
    script_path = os.path.join(os.path.dirname(__file__), 'app.py')
    # Elindítja a Streamlit szervert a háttérben
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", script_path])

if __name__ == '__main__':
    main()