import requests
import xml.etree.ElementTree as ET
import gzip
import sys

urls = [
    "https://iptv-org.github.io/epg/guides/br.xml",
    "https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz"
]

print("Iniciando merge dos EPGs...")
root = ET.Element('tv')
sucesso = 0

for url in urls:
    try:
        print(f"Baixando: {url}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        
        content = r.content
        if url.endswith('.gz'):
            print("Descompactando .gz...")
            content = gzip.decompress(content)
        
        epg = ET.fromstring(content)
        for child in epg:
            root.append(child)
        print(f"OK: {url}")
        sucesso += 1
        
    except Exception as e:
        print(f"ERRO ao processar {url}: {e}")
        continue

if sucesso == 0:
    print("Nenhum EPG foi baixado com sucesso!")
    sys.exit(1)

tree = ET.ElementTree(root)
tree.write('epg-brasil.xml', encoding='UTF-8', xml_declaration=True)
print(f"Arquivo epg-brasil.xml gerado! {sucesso} fontes OK")
