import requests
import re

# Lista de canales: podés agregar más siguiendo el mismo formato
CANALES = [
    {"nombre": "Fox Sports 2", "url": "https://streamtpnew.com/global1.php?stream=fox2ar"}
]

def buscar_m3u8(url_web):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url_web, headers=headers, timeout=15)
        # Buscamos algo que empiece con http y termine en .m3u8
        match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)
        if match:
            return match.group(1).replace('\\/', '/')
        return None
    except:
        return None

# Crear el archivo M3U
with open("lista_fresca.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for canal in CANALES:
        link = buscar_m3u8(canal['url'])
        if link:
            f.write(f"#EXTINF:-1, {canal['nombre']}\n")
            f.write(f"{link}\n")

print("Lista creada!")
