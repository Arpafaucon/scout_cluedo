from __future__ import annotations
from lxml import etree
from pathlib import Path
from cluedo import Card, Cluedo
import typing as tp
import pydantic
import networkx
import matplotlib.pyplot as plt

CLUEDO_GRAPH = Path("cluedo.graphml")

tree = etree.fromstring(CLUEDO_GRAPH.read_bytes())
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

# g = networkx.DiGraph()
# for c in cards.values():
#     g.add_node(c.label)
# for c in cards.values():
#     for target in c.required_for:
#         g.add_edge(c.id, target)

# FIG_OPTIONS = {
#     "tight_layout": {
#         'rect': (0, 0, .9, 1)
#     },
#     "figsize": (12, 8)
# }
# fig, ax = plt.subplots(**FIG_OPTIONS)
# pos = networkx.planar_layout(g)
# networkx.draw_networkx(g, ax=ax, pos=pos)
# fig.show()


# nodes_attributes = tree.xpath("//node")

# print(list(nodes_attributes))


# shape = "STAR6"
# for card_type, shape in shapes.items():
#     nodes = tree.xpath(f"""//gml:data[@key="d7"]/yjs:ShapeNodeStyle[@shape="{shape}"]/ancestor::gml:node""", namespaces=nss)
#     print(card_type)
#     # Retrieve text
#     for n in nodes:
#         text_nodes = n.xpath('.//y:Label.Text', namespaces=nss)
#         text = [tn.text for tn in text_nodes]
#         print("-", text)
