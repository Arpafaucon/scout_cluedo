from __future__ import annotations
from lxml import etree
from pathlib import Path
from cluedo import Card, Cluedo
import typing as tp

CLUEDO_GRAPH = Path("cluedo.graphml")

tree = etree.fromstring(CLUEDO_GRAPH.read_bytes())
# Edition des namespace XML pour expliciter le namespace par défaut
# pour les requetes XPATH
nss = tree.nsmap
nss["gml"] = nss.pop(None)

cards: tp.Dict[str, Card] = {}

for n in tree.xpath("//gml:node", namespaces=nss):
    card = Card.from_node(n, nss)
    cards[card.id] = card

for e in tree.xpath("//gml:edge", namespaces=nss):
    source = e.attrib["source"]
    target = e.attrib["target"]
    cards[source].required_for.add(target)
    cards[target].depends_on.add(source)

cluedo = Cluedo(cards=cards)

for id, card in cards.items():
    print(card)
Path("cluedo.json").write_text(cluedo.json(indent=2))

