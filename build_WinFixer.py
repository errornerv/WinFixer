import subprocess
import os
import shutil

def clean_old_builds():
    paths_to_remove = ['build', 'dist', 'WinFixer.spec']
    for path in paths_to_remove:
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"[+] Removed directory: {path}")
        elif os.path.isfile(path):
            os.remove(path)
            print(f"[+] Removed file: {path}")

def create_spec_file():
    spec_content = """# WinFixer.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['core'],
    binaries=[],
    datas=[('core', 'core')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WinFixer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False  # تغییر به False برای مخفی کردن کنسول
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WinFixer'
)
"""
    with open('WinFixer.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("[+] WinFixer.spec created successfully.")

def build_exe():
    print("[*] Building WinFixer.exe ...")
    result = subprocess.run(["pyinstaller", "--log-level=DEBUG", "WinFixer.spec"], capture_output=True, text=True)
    if result.returncode == 0:
        print("[+] Build completed successfully.")
    else:
        print("[!] Build failed.")
        print(result.stderr)

def main():
    clean_old_builds()
    create_spec_file()
    build_exe()

if __name__ == "__main__":
    main()