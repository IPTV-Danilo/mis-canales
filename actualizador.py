import requests
import re

CANALES = [
    {"nombre": "Fox Sports 2", "url": "https://streamtpnew.com/global1.php?stream=fox2ar"}
]

def buscar_m3u8(url_web):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Referer': 'https://streamtpnew.com/'
    }
    try:
        r = requests.get(url_web, headers=headers, timeout=20)
        # Esto busca cualquier URL que tenga .m3u8 adentro, sin importar comillas
        links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r.text)
        
        for link in links:
            if '.m3u8' in link:
                # Limpiamos posibles residuos de código
                clean_link = link.split('"')[0].split("'")[0].replace('\\', '')
                return clean_link
        return None
    except:
        return None

# Generar el archivo
with open("lista_fresca.m3u", "w") as f:
    f.write("#EXTM3U\n")
    encontrado = False
    for canal in CANALES:
        link = buscar_m3u8(canal['url'])
        if link:
            f.write(f"#EXTINF:-1, {canal['nombre']}\n{link}\n")
            encontrado = True
            print(f"✅ Encontrado: {canal['nombre']}")
    
    if not encontrado:
        # Esto es para que te des cuenta si falló
        f.write("# El script no pudo encontrar ningun link activo en este momento\n")
        print("❌ No se encontró ningún link.")
