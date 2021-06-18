from __future__ import annotations
import pydantic
import typing as tp

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
    def from_node(elt, xmlns) -> Card:
        id = elt.attrib["id"]

        shape = elt.xpath(".//yjs:ShapeNodeStyle/@shape", namespaces=xmlns)[0]
        type = rev_shapes[shape]

        label_texts = elt.xpath(".//y:Label.Text/text()", namespaces=xmlns)
        label = "\n".join(label_texts)

        description_res = elt.xpath(""".//gml:data[@key="d3"]/text()""", namespaces=xmlns)
        if description_res:
            description = description_res[0]
        else:
            description = ""

        return Card(
            id=id,
            type=type,
            label=label,
            description = description
        )

    def pretty_type(self) -> str:
        return {
            "statement": "déclaration",
            "fingerprint": "empreinte",
            "evidence": "indice",
            "proof": "preuve"
        }.get(self.type, self.type)



    # def description_smart(self) -> str:
    #     if self.type == "statement":
    #         return self.pretty_type()

class Cluedo(pydantic.BaseModel):
    cards: tp.Dict[str, Card]