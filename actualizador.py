import requests
import re

# Lista de canales
CANALES = [
    {"nombre": "Fox Sports 2", "url": "https://streamtpnew.com/global1.php?stream=fox2ar"}
]

def buscar_m3u8(url_web):
    # Simulamos ser un navegador real para que no nos bloqueen
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://streamtpnew.com/'
    }
    try:
        r = requests.get(url_web, headers=headers, timeout=15)
        texto = r.text

        # Intento 1: Buscar links estándar .m3u8
        match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', texto)
        
        # Intento 2: Buscar links que están "escondidos" con barras inclinadas (ej: http:\/\/...)
        if not match:
            match = re.search(r'(https?:\\\/\\\/[^\s\'"]+\.m3u8[^\s\'"]*)', texto)

        if match:
            link = match.group(1).replace('\\/', '/')
            return link
        
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Crear el archivo M3U
with open("lista_fresca.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for canal in CANALES:
        print(f"Buscando link para {canal['nombre']}...")
        link = buscar_m3u8(canal['url'])
        if link:
            # Agregamos el User-Agent al link para que el reproductor no falle
            f.write(f"#EXTINF:-1, {canal['nombre']}\n")
            f.write(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0\n')
            f.write(f"{link}\n")
        else:
            print(f"No se encontró nada para {canal['nombre']}")

print("Proceso finalizado.")
