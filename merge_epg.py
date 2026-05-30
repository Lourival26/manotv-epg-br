import requests
import xml.etree.ElementTree as ET
import gzip

urls = [
    "https://iptv-org.github.io/epg/guides/br.xml",
    "https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz"
]

print("Iniciando merge dos EPGs...")
root = ET.Element('tv')

for url in urls:
    print(f"Baixando: {url}")
    r = requests.get(url, timeout=30)
    content = r.content
    
    if url.endswith('.gz'):
        print("Descompactando .gz...")
        content = gzip.decompress(content)
    
    epg = ET.fromstring(content)
    for child in epg:
        root.append(child)
    print(f"Adicionado: {url}")

tree = ET.ElementTree(root)
tree.write('epg-brasil.xml', encoding='UTF-8', xml_declaration=True)
print("Arquivo epg-brasil.xml gerado com sucesso!")
