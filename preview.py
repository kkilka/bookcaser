import numpy as np
from PIL import Image, ImageDraw, ImageFont
from livelib import Book, search_book, get_cover


def _corner(bevel: int):
        image = Image.new('RGB', (bevel, bevel), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, bevel*2, bevel*2), (255, 255, 255))

        return image
    

def frame(size: tuple, bevel: int, path: str = 'temp\\bevel.png') -> str:
    if bevel > size[0]/2 or bevel > size[1]/2: raise 'The bevel is too large for this image'

    image = Image.new('RGB', size, (255, 255, 255))
    corner = _corner(bevel)
    
    for xy in ((0, 0), (0, size[1]-bevel), (size[0]-bevel, size[1]-bevel), (size[0]-bevel, 0)):
        image.paste(corner, xy)
        corner = corner.rotate(90)

    image.save(path)
    return path


def gradient(color: tuple, width: int) -> Image:
    pixels = [[list(color) + [255] for i in range(width)] for j in range(500)]

    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            pixels[i][j][3] = int(abs(255-(255/width*(j))))

    return Image.fromarray(np.array(pixels).astype(np.uint8))
    

def main_color(image: Image) -> set:
    image = image.resize((50, int(image.height*(50/image.width))))
    pixels = list(image.getdata())

    for i in range(len(pixels)):
        pixels[i] = list(pixels[i])
        for j in range(len(pixels[i])):
            pixels[i][j] = pixels[i][j]//25*25

    return max(pixels, key=lambda x: pixels.count(x))


def color_box(size: set, color: set) -> Image:
    pixels = [[color for i in range(size[0])] for j in range(size[1])]
    return Image.fromarray(np.array(pixels).astype(np.uint8))


# def get_preview(book: Book, show=False):
#     indent = 0 # indentation on the left of the cover color
#     cover_height = 350

#     cover = Image.open(get_cover(book))
#     cover = cover.resize((int(cover.width*(cover_height/cover.height)), cover_height))
#     background = Image.open('Source\\Preview\\background.png')


#     color = tuple(main_color(cover))
#     text_color = (0, 0, 0)
    
#     background.paste(color_box((indent, 500), color), (0, 0))
#     background.paste(gradient(color).resize((500, 500)), (indent, 0), gradient(color).resize((500, 500)))
#     # background.paste(cover, (background.width//2 - cover.width//2, (500-cover_height)//2))
    
#     background.paste(cover, (indent+400, (500-cover_height)//2))
    
#     draw = ImageDraw.Draw(background)  
  
#     font_rating = ImageFont.truetype('Source\\Fonts\\Bahnschrift.ttf', 300) 
#     font_stars = ImageFont.truetype('Source\\Fonts\\SegoeUISymbol.ttf', 100)

#     shape = (indent+475+cover.width, (500-cover_height)//2)
#     draw.text(shape, text=str(book.rating), font=font_rating, fill=text_color)
#     draw.text((shape[0], shape[1]+225), '★'*int(float(book.rating)) + '☆'*(5-int(float(book.rating))), font=font_stars, fill=text_color)

#     watermark = Image.open(get_watermark())
#     # background.paste(watermark, (background.size[0]-watermark.size[0]-10, background.size[1]-watermark.size[1]-10), watermark)
#     background.paste(watermark, ((background.size[0]-watermark.size[0])//2+indent, background.size[1]-watermark.size[1]-10), watermark)

#     path = f'temp\\{book.id}.png'

#     if show:
#         background.show()
#     else:
#         background.save(path)

#     return path


def get_preview(book: Book, show=False):
    indent = 0 # indentation on the left of the cover color
    cover_height = 350

    cover = Image.open(get_cover(book))
    cover = cover.resize((int(cover.width*(cover_height/cover.height)), cover_height))
    background = Image.open('Source\\Preview\\background.png')


    color = tuple(main_color(cover))
    text_color = (0, 0, 0)
    
    # background.paste(color_box((indent, 500), color), (0, 0))
    background.paste(color_box((500, 500), color), (0, 0), gradient(color, 500))    
    
    draw = ImageDraw.Draw(background)  
  
    font_rating = ImageFont.truetype('Source\\Fonts\\Bahnschrift.ttf', 300) 
    font_stars = ImageFont.truetype('Source\\Fonts\\SegoeUISymbol.ttf', 100)

    text_width = int(draw.textlength(text=str(float(book.rating)), font=font_rating))
    print(text_width)

    block_width = cover.width + text_width + 30
    cover_x = background.width//2 - block_width//2
    text_x = cover_x + cover.width + 30
    
    cover.putalpha(Image.open(frame(cover.size, 20)).convert('L'))
    background.paste(cover, (cover_x, (background.height-cover.height)//2-15), cover)

    shape = (text_x, (background.height-cover.height)//2-15)
    draw.text(shape, text=str(float(book.rating)), font=font_rating, fill=text_color)
    draw.text((shape[0], shape[1]+225), '★'*int(float(book.rating)) + '☆'*(5-int(float(book.rating))), font=font_stars, fill=text_color)


    watermark = Image.open(get_watermark())
    # background.paste(watermark, (background.size[0]-watermark.size[0]-10, background.size[1]-watermark.size[1]-10), watermark)
    background.paste(watermark, ((background.width-watermark.width)//2, background.height-watermark.height-15), watermark)

    path = f'temp\\{book.book_id}.png'

    if show:
        background.show()
    else:
        background.save(path)

    return path

def get_watermark(text: str = 'Книжный Шкаф', space: int|float = 5, transperent_percent: int|float = 50, show: bool = False):
    ico = Image.open('Source\\Preview\\tg_icon.png')
    ico_mask = ico.split()[3].point(lambda i: i * transperent_percent/100)
    
    ico_x, ico_y = ico.size

    img = Image.new('RGBA', (1500, 500), (0, 0, 0, 0))

    font = ImageFont.truetype('Source\\Fonts\\Involve-Bold.otf', ico_y-10)
    draw = ImageDraw.Draw(img)

    x = draw.textbbox((ico_x+space, 5), text=text, font=font)[2]

    draw.text((ico_x+space, 5), text=text, font=font, fill=(0, 0, 0, 255*transperent_percent//100))
    img.paste(ico, mask=ico_mask)

    path = 'temp\\watermark.png'

    if show:
        img.crop((0, 0, x, 50)).show()
    else:
        img.crop((0, 0, x, 50)).save(path)

    return path
        

# print(get_preview(search_book('Звезда пленительного счастья'), True))
# get_watermark()