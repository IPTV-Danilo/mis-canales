import requests
import re

CANALES = [
    {"nombre": "Fox Sports 2", "url": "https://streamtpnew.com/global1.php?stream=fox2ar"}
]

def buscar_m3u8(url_web):
    # Headers más agresivos para parecer un humano real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://google.com.ar/',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    try:
        session = requests.Session()
        r = session.get(url_web, headers=headers, timeout=20)
        
        if r.status_code != 200:
            print(f"❌ Error de acceso: La web devolvió código {r.status_code}")
            return None
            
        texto = r.text
        # Buscamos el link .m3u8
        match = re.search(r'["\'](https?://[^\s\'"]+\.m3u8[^\s\'"]*)["\']', texto)
        
        if match:
            return match.group(1).replace('\\/', '/')
        
        print("⚠️ No se encontró el link .m3u8 en el código de la página.")
        return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

with open("lista_fresca.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for canal in CANALES:
        link = buscar_m3u8(canal['url'])
        if link:
            f.write(f"#EXTINF:-1, {canal['nombre']}\n")
            f.write(f"{link}\n")
            print(f"✅ ¡Éxito! Canal {canal['nombre']} agregado.")
