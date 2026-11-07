import sys
import os
import streamlit
from PyInstaller.utils.hooks import collect_data_files, copy_metadata, collect_submodules

# 1. Kikényszerítjük a Streamlit statikus mappájának pontos helyét a saját gépeden!
streamlit_root = os.path.dirname(streamlit.__file__)
streamlit_static = os.path.join(streamlit_root, 'static')

# Automatikus adat- és metagyűjtések
streamlit_datas = collect_data_files('streamlit')
streamlit_metadata = copy_metadata('streamlit')
plotly_datas = collect_data_files('plotly')

# 2. Hozzáadjuk az app.py-t ÉS a manuálisan megkeresett static mappát is!
all_datas = [
    ('app.py', '.'), 
    (streamlit_static, 'streamlit/static') # <-- EZ OLDJA MEG A NOT FOUND HIBÁT
] + streamlit_datas + streamlit_metadata + plotly_datas

all_hidden_imports = collect_submodules('streamlit') + ['plotly', 'numpy']

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=all_datas,
    hiddenimports=all_hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BlochSimulator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True, # Ideiglenesen hagyjuk bekapcsolva a tesztig
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=['app_icon.ico'] 
)