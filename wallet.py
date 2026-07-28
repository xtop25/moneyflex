# -*- coding: utf-8 -*-
"""Nova Wallet - launcher for a desktop-looking window (fake/demo wallet UI).
Opens CryptoWallet.html in a chromeless app window (Chrome / Edge / Brave).
Build to .exe:  build_exe.bat
"""
import os
import subprocess
import sys
import tempfile
import webbrowser

HTML_NAME = "CryptoWallet.html"
WIN_SIZE = "1280,800"


def resource_path(name: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


def stable_copy(src: str) -> str:
    """Copy the UI next to a stable profile dir so localStorage settings persist."""
    target_dir = os.path.join(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()), "NovaWallet")
    os.makedirs(target_dir, exist_ok=True)
    dst = os.path.join(target_dir, HTML_NAME)
    with open(src, "rb") as f:
        data = f.read()
    try:
        with open(dst, "rb") as f:
            if f.read() == data:
                return dst
    except OSError:
        pass
    with open(dst, "wb") as f:
        f.write(data)
    return dst


def find_browser():
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    local = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        os.path.join(pf, r"Google\Chrome\Application\chrome.exe"),
        os.path.join(pf86, r"Google\Chrome\Application\chrome.exe"),
        os.path.join(local, r"Google\Chrome\Application\chrome.exe"),
        os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe"),
        os.path.join(pf, r"Microsoft\Edge\Application\msedge.exe"),
        os.path.join(pf, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
        os.path.join(local, r"Programs\Opera\opera.exe"),
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return None


def main():
    html = stable_copy(resource_path(HTML_NAME))
    url = "file:///" + html.replace("\\", "/")
    profile = os.path.join(os.path.dirname(html), "profile")
    browser = find_browser()
    if browser:
        subprocess.run([
            browser,
            "--app=" + url,
            "--window-size=" + WIN_SIZE,
            "--user-data-dir=" + profile,
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-features=Translate,DefaultBrowserPrompt",
            "--allow-file-access-from-files",
        ])
    else:
        webbrowser.open(url)


if __name__ == "__main__":
    main()
