from lxml import etree
from pathlib import Path

CLUEDO_GRAPH = Path("cluedo.graphml")
NS=r"{http://graphml.graphdrawing.org/xmlns}"

tree = etree.fromstring(CLUEDO_GRAPH.read_bytes())
nss=tree.nsmap
nss['gml'] = nss.pop(None)

tree.xpath("//gml:node/@id", namespaces=nss)

nodes_attributes = tree.xpath("//node")

print(list(nodes_attributes))