import PIL
from PIL import Image, ImageSequence, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import asyncio

def download_from_url(url):
  response = requests.get(url)
  avatar = Image.open(BytesIO(response.content))
  return avatar

def get_text_size(text: str, font: str, text_size: int):
    # imagem = Image.new('RGB', (1, 1), (255, 255, 255))
    fonte = ImageFont.FreeTypeFont(font, text_size)
    # draw = ImageDraw.Draw(imagem)

    return fonte.getbbox(text)

def draw_text_image(img_org, text, pos, max_size, font_path=None, font_size=30, text_color=(0, 0, 0), aling="center"):
    image = img_org
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(image)
    position = pos

    draw.text(position, text, fill=text_color, font=font, align=aling)

    return image

async def make_quote_image(Avatar: str, quote: str, author: str): # "this works good, don't mess with it" -Hades 2024
    avatar_img = download_from_url(Avatar).resize((720, 720))
    avatar_img = avatar_img.convert("L")
    gradient_img = Image.open("images/Quotes/gradient.png")
    # gradient_img = gradient_img.convert("RGBA")
    base_img = Image.new('RGB', (1280, 720))
    base_img.paste(avatar_img, (0, 0))
    # base_img.paste(gradient_img, (0,0))
    base_img = Image.alpha_composite(base_img.convert("RGBA"), gradient_img)

    lines = textwrap.wrap(quote, width=32)
    final_text_quote = ""
    for line in lines:
        final_text_quote = final_text_quote + line + "\n"
    base_img = draw_text_image(base_img, final_text_quote, (750, 200), 0, font_path="fonts/arial.ttf", font_size=32, text_color=(255,255,255), aling="center")
    base_img = draw_text_image(base_img, f"-{author}. 2024", (800, 620), 0, font_path="fonts/arial.ttf", font_size=24, text_color=(255,255,255), aling="center")
    base_img.save("images/Quotes/cache.png")

async def make_megamind_image(quote: str, image_filename: str): # why it's too hard to set max width to a text, AAAAAAAAAAAAAAAAAAAAAAAAAAA
    base = Image.open("images/MegamindImages/base.jpg")
    text_box = get_text_size(quote, "fonts/arial.ttf", 100)
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]
    text_size_converted = text_width / 512 # 512 = max size
    base = draw_text_image(base, quote, (20, 20), 0, font_path="fonts/arial.ttf", font_size=(text_size_converted * 100), text_color=(255,255,255), aling="center")
    base.save(f"images/MegamindImages/{image_filename}.jpg")
