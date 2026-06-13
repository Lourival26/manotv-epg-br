import requests
import xml.etree.ElementTree as ET
import gzip
import sys

urls = [
    "https://iptv-org.github.io/epg/guides/br.xml",
    "https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz",
    "https://epg.pluto.tv/v2/pluto_br.xml.gz",  # Pluto TV Brasil
    "https://iptv-org.github.io/epg/guides/br_record.xml"  # Record TV + afiliadas
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
        print(f"Erro em {url}: {e}")

tree = ET.ElementTree(root)
tree.write('epg_mergeado.xml', encoding='UTF-8', xml_declaration=True)
print(f"\nMerge finalizado! {sucesso} EPGs juntados em epg_mergeado.xml")