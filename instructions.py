from cluedo import Cluedo, Card
import textwrap

clu = Cluedo.parse_file("cluedo.json")
action_cards = [c for c in clu.cards.values() if c.type == "action"]
action_cards = sorted(action_cards, key=lambda c: c.label)

def short_description(c: Card):
    short_desc = textwrap.shorten(c.description, 50)
    short_label = textwrap.shorten(c.description, 50)
    return f"{c.id} {c.pretty_type()}: {short_desc}"

for c in action_cards:
    print("__________________")
    print("ID: ", c.id)
    print("Label: ", c.label)
    if c.depends_on:
        print("Prérequis:")
        for id in c.depends_on:
            print("-", short_description(clu.cards[id]))
    if c.required_for:
        print("Donner:")
        for id in c.required_for:
            print("-", short_description(clu.cards[id]))
    if c.description:
        print("Autres infos:", c.description)