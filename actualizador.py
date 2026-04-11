import requests
import re
import base64

CANALES = [
    {"nombre": "Fox Sports 2", "url": "https://streamtpnew.com/global1.php?stream=fox2ar"}
]

def buscar_m3u8(url_web):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://streamtpnew.com/'
    }
    try:
        response = requests.get(url_web, headers=headers, timeout=15)
        html = response.text

        # 1. Buscamos links m3u8 directos
        found = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', html)
        
        # 2. Si no hay, buscamos links en Base64 (muy común en estas webs)
        if not found:
            # Buscamos cadenas largas que parezcan base64
            b64_matches = re.findall(r'["\']([A-Za-z0-9+/]{40,})={0,2}["\']', html)
            for b in b64_matches:
                try:
                    decoded = base64.b64decode(b).decode('utf-8')
                    if '.m3u8' in decoded:
                        found.append(re.search(r'(https?://.*?\.m3u8.*)', decoded).group(1))
                except:
                    continue

        if found:
            # Limpiamos el link de barras raras
            final_link = found[0].replace('\\/', '/')
            return final_link
        
        return None
    except Exception as e:
        print(f"Error en script: {e}")
        return None

# Crear el archivo M3U
with open("lista_fresca.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for canal in CANALES:
        link = buscar_m3u8(canal['url'])
        if link:
            f.write(f"#EXTINF:-1, {canal['nombre']}\n")
            # Forzamos el User-Agent para que el reproductor lo use
            f.write(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0\n')
            f.write(f"{link}\n")
            print(f"✅ Link encontrado para {canal['nombre']}")
        else:
            print(f"❌ No se encontró nada para {canal['nombre']}")
