from pathlib import Path
from PIL.Image import Image
from pathlib import Path
import PIL.Image, PIL.ImageDraw, PIL.ImageFont, PIL.ImageShow
from size import Size
import numpy as np
from image_builder import HEIGHT_MM, LOGGER, WIDTH_MM, DPI, MM_TO_PX


source = Path("output")
files = list(source.glob("*"))


A4_mm = Size(210, 297) # mm
A4 = A4_mm * MM_TO_PX

MARGIN = Size(10,10) # mm

accesible_wh_mm =  Size(A4.array - 2*MARGIN.array)
accessible_wm = accesible_wh_mm * MM_TO_PX


OUT_PAGES = Path("output_pages")
OUT_PAGES.mkdir(exist_ok=True)

blit_locations = []
for ix in range(3):
    for iy in range(3):
        xy_mm = Size(MARGIN.array + np.array([WIDTH_MM*ix, HEIGHT_MM*iy]))
        xy = xy_mm * MM_TO_PX
        blit_locations.append(xy)


for page_ix in range(len(files)//9+1):
    page = PIL.Image.new("RGBA", A4.tuple_int(), color="white")
    imgs_to_paste = files[9*page_ix: 9*page_ix+9]
    for i, img in enumerate(imgs_to_paste):
        loc = blit_locations[i]
        LOGGER.info("%s", img)
        imgdata = PIL.Image.open(img)
        page.paste(imgdata, loc.tuple_int())
    page.save(OUT_PAGES/f"{page_ix}.png")

