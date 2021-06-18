from __future__ import annotations
from lxml import etree
from pathlib import Path
import typing as tp
import pydantic
import networkx
import matplotlib.pyplot as plt

CLUEDO_GRAPH = Path("cluedo.graphml")
NS = r"{http://graphml.graphdrawing.org/xmlns}"

tree = etree.fromstring(CLUEDO_GRAPH.read_bytes())
nss = tree.nsmap
nss["gml"] = nss.pop(None)

shapes = {
    "action": "ROUND_RECTANGLE",
    "statement": "ELLIPSE",
    "fingerprint": "TRIANGLE2",
    "evidence": "STAR6",
    "proof": "DIAMOND",
}
rev_shapes = {v: k for k, v in shapes.items()}


class Card(pydantic.BaseModel):
    id: str
    type: str
    label: str
    description: str = ""
    url: str = ""

    depends_on: tp.Set[str] = pydantic.Field(default_factory=set)
    required_for: tp.Set[str] = pydantic.Field(default_factory=set)

    @staticmethod
    def from_node(elt) -> Card:
        id = elt.attrib["id"]

        shape = elt.xpath(".//yjs:ShapeNodeStyle/@shape", namespaces=nss)[0]
        type = rev_shapes[shape]

        label_texts = elt.xpath(".//y:Label.Text/text()", namespaces=nss)
        label = "\n".join(label_texts)

        return Card(
            id=id,
            type=type,
            label=label,
        )

cards: tp.Dict[str, Card] = {}

for n in tree.xpath("//gml:node", namespaces=nss):
    card = Card.from_node(n)
    cards[card.id] = card

for e in tree.xpath("//gml:edge", namespaces=nss):
    source = e.attrib["source"]
    target = e.attrib["target"]
    cards[source].required_for.add(target)
    cards[target].depends_on.add(source)



g = networkx.DiGraph()
for c in cards.values():
    g.add_node(c.label)
for c in cards.values():
    for target in c.required_for:
        g.add_edge(c.id, target)

for id, card in cards.items():
    print(card)


FIG_OPTIONS = {
    "tight_layout": {
        'rect': (0, 0, .9, 1)
    },
    "figsize": (12, 8)
}
fig, ax = plt.subplots(**FIG_OPTIONS)
pos = networkx.planar_layout(g)
networkx.draw_networkx(g, ax=ax, pos=pos)
fig.show()


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
