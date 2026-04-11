import requests
import re

# --- CONFIGURACIÓN ---
API_KEY = "996acb929b96ea421fc4404615f316b2"
ARCHIVO_M3U = "lista_fresca.m3u"

CANALES = [
    {"nombre": "Fox Sports 2", "url": "https://streamtpnew.com/global1.php?stream=fox2ar"}
]

def buscar_m3u8(url_web):
    # Construimos la URL para que pase a través del proxy de ScraperAPI
    proxy_url = f"http://api.scraperapi.com?api_key={API_KEY}&url={url_web}"
    
    print(f"Buscando link a través de ScraperAPI para la URL: {url_web}")
    
    try:
        # Hacemos el pedido a la API (ella se encarga de los proxies)
        r = requests.get(proxy_url, timeout=60)
        
        if r.status_code == 200:
            # Buscamos cualquier patrón que parezca un link .m3u8
            match = re.search(r'["\'](https?://[^\s\'"]+\.m3u8[^\s\'"]*)["\']', r.text)
            
            if not match:
                # Intento secundario si el link está "escapado" con barras
                match = re.search(r'(https?%3A%2F%2F[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)

            if match:
                link = match.group(1).replace('\\/', '/')
                # Si el link está url-encoded, lo limpiamos (opcional)
                import urllib.parse
                link = urllib.parse.unquote(link)
                return link
        else:
            print(f"Error de ScraperAPI: Código {r.status_code}")
            
        return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# --- GENERACIÓN DE LA LISTA ---
with open(ARCHIVO_M3U, "w") as f:
    f.write("#EXTM3U\n")
    encontrado_alguno = False
    
    for canal in CANALES:
        link = buscar_m3u8(canal['url'])
        if link:
            f.write(f"#EXTINF:-1, {canal['nombre']}\n")
            f.write(f"{link}\n")
            encontrado_alguno = True
            print(f"✅ Encontrado: {canal['nombre']}")
        else:
            print(f"❌ No se pudo encontrar link para: {canal['nombre']}")
    
    if not encontrado_alguno:
        f.write("# No se encontraron links activos en este intento\n")

print("Proceso finalizado.")
