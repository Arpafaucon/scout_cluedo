from __future__ import annotations
import shutil
from cluedo import Cluedo, Card
from size import Size
from PIL.Image import Image
from pathlib import Path
import PIL.Image, PIL.ImageDraw, PIL.ImageFont, PIL.ImageShow

import typing_extensions as tp_ext
import typing as tp
from dataclasses import dataclass
import numpy as np

import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
# coordinate system from the top le1ft corne
# X is width
# Y is height

DPI = 300
MM_TO_INCHES = 0.03937008
MM_TO_PX = MM_TO_INCHES * DPI


HEIGHT_MM = 90
WIDTH_MM = 65.02

IMG_SIZE_MM = Size(WIDTH_MM, HEIGHT_MM)
IMG_SIZE_PX = IMG_SIZE_MM * MM_TO_PX
LOGGER.info("Card size: %s", IMG_SIZE_PX)

# Title text
TITLE_SIZE = int(0.16*DPI)
TITLE_CENTER_RT = Size(0.5, 0.07)

# ID text
ID_SIZE = int(0.08*DPI)
ID_CENTER_RT = Size(0.9, 0.05)
ID_SIZE_RT = Size(0.1, 0.08)

# Depends on text
DEPON_SIZE = int(0.08*DPI)
DEPON_CENTER_RT = Size(0.5, 0.95)
DEPON_SIZE_RT = Size(0.9, 0.05)


# coordinates of the image, in percent of the view
IMG_CENTER_X_PC = 50
IMG_CENTER_Y_PC = 30
IMG_WIDTH_PC = 80
IMG_HEIGHT_PC = 30

# coordinates of the description view, as a ratio
DESCRIPTION_TEXT_SIZE = int(0.1*DPI)
DESCRIPTION_SIZE_RT = Size(0.8, 0.4)
DESCRIPTION_CENTER_RT = Size(0.5, 0.7)


# Size: tp_ext.TypeAlias = tp.Tuple[float, float] # Width, height


def to_px(length_mm: float) -> int:

    return int(length_mm * MM_TO_INCHES * DPI)


def resize_to_fit(original_size: Size, box_size: Size) -> Size:
    ratio_to_box = original_size.array / box_size.array
    downsize_ratio = ratio_to_box.max()
    return Size(original_size.array / downsize_ratio)


assert resize_to_fit(Size(10, 10), Size(10, 10)) == Size(10, 10)
assert resize_to_fit(Size(20, 10), Size(10, 10)) == Size(10, 5)


def topleft_from_center(center: Size, rectangle: Size) -> Size:
    return Size(center.array - rectangle.array / 2)


assert topleft_from_center(Size(5, 5), Size(10, 10)) == Size(0, 0)
assert topleft_from_center(Size(5, 5), Size(8, 4)) == Size(1, 3)

def format_id(i:str) -> str:
    return f"#{i}#"


def build_card(card: Card) -> Image:
    # main_image = PIL.Image.new(
    #     "RGBA", IMG_SIZE_PX.tuple_int(), color="yellow"
    # )
    main_image = PIL.Image.open("template.png")
    draw: PIL.ImageDraw.ImageDraw = PIL.ImageDraw.Draw(main_image)
    LOGGER.info("loaded main image, size=%s", main_image.size)

    # title
    ################
    title_font = PIL.ImageFont.truetype("fonts/topsecretstamp.ttf", size=TITLE_SIZE)
    title_text_size = Size(title_font.getsize(card.label))
    title_xy = topleft_from_center(TITLE_CENTER_RT*IMG_SIZE_PX, title_text_size)
    draw.text(title_xy.tuple_int(), card.label, font=title_font, fill="black")
    LOGGER.info("drawn text")

    # ID
    ################
    id_font = PIL.ImageFont.truetype("fonts/topsecretstamp.ttf", size=ID_SIZE)
    id_text = format_id(card.id)
    id_text_size = Size(id_font.getsize(id_text))
    id_xy = topleft_from_center(ID_CENTER_RT*IMG_SIZE_PX, id_text_size)
    draw.text(id_xy.tuple_int(), id_text, font=id_font, fill="black")
    LOGGER.info("drawn ID")

    # Requires
    ################
    requires_text = "requiert: " + ",".join(map(format_id, card.depends_on))
    depon_text_size = Size(id_font.getsize(requires_text))
    depon_xy = topleft_from_center(DEPON_CENTER_RT*IMG_SIZE_PX, depon_text_size)
    draw.text(depon_xy.tuple_int(), requires_text, font=id_font, fill="black")
    LOGGER.info("drawn depends-on")

    # description
    ################
    description_font = title_font
    description_text_size = Size(description_font.getsize(card.description))
    description_xy = topleft_from_center(DESCRIPTION_CENTER_RT, DESCRIPTION_SIZE_RT) * IMG_SIZE_PX
    draw.multiline_text(description_xy.tuple_int(), card.description, font=description_font, fill="black")


    # Illustration
    ################
    # compute image box size
    template_img_size = (
        Size(IMG_WIDTH_PC, IMG_HEIGHT_PC) * 1e-2 * IMG_SIZE_PX
    )
    template_img_center = (
        Size(IMG_CENTER_X_PC, IMG_CENTER_Y_PC) * 1e-2 * IMG_SIZE_PX
    )

    image_url = card.url
    if not image_url:
        image_url = "fingerprint.png"
    illustration_raw = PIL.Image.open(Path("images") / image_url).convert("RGBA")
    illustration_raw_size_wh = Size(illustration_raw.size)
    LOGGER.info("Initial illustration size:  %s", illustration_raw_size_wh)
    # resize
    illustration_resized_size = resize_to_fit(
        illustration_raw_size_wh, template_img_size
    )
    LOGGER.info("Resizing illustration to %s", illustration_resized_size)
    illustration_resized = illustration_raw.resize(
        illustration_resized_size.tuple_int()
    )
    illustration_resized_size = Size(illustration_resized.size)
    LOGGER.info("Resized illustration to %s", illustration_resized_size)
    # paste
    xy = topleft_from_center(template_img_center, illustration_resized_size)
    main_image.paste(illustration_resized, xy.tuple_int(), illustration_resized)
    LOGGER.info("Pasted illustration")

    return main_image


clu = Cluedo.parse_file("cluedo.json")

dest_folder = Path("output")
if dest_folder.exists():
    shutil.rmtree(dest_folder)
dest_folder.mkdir(parents=True)

for i, (card_id, card) in enumerate(clu.cards.items()):
    im = build_card(card)
    im.save(dest_folder/f"{card_id}.png")
    # if i > 10:
    #     break

# any_card = clu.cards["n2"]
# PIL.ImageShow.register(PIL.ImageShow.EogViewer, -1)
# im.show()
