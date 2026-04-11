def buscar_m3u8(url_web):
    # Agregamos &render=true para que la API use un navegador real
    proxy_url = f"http://api.scraperapi.com?api_key={API_KEY}&url={url_web}&render=true"
    
    print(f"Buscando con Navegador Virtual para: {url_web}")
    
    try:
        # Al usar render=true, el timeout debe ser más largo (60 seg)
        r = requests.get(proxy_url, timeout=80)
        
        if r.status_code == 200:
            # Buscamos el m3u8. Estas páginas suelen ponerlo en una variable 'file' o 'source'
            match = re.search(r'["\'](https?://[^\s\'"]+\.m3u8[^\s\'"]*)["\']', r.text)
            
            if match:
                link = match.group(1).replace('\\/', '/')
                return link
            else:
                # Si no lo encuentra, imprimimos un pedacito del código para ver qué pasa
                print("Código recibido pero sin link m3u8.")
        else:
            print(f"Error ScraperAPI: {r.status_code}")
            
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
