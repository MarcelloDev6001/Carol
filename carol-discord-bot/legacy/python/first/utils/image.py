import discord
from PIL import Image, ImageSequence, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
from config import config

def draw_text_image(img_org, text, pos, max_size, font_path=None, font_size=30, text_color=(0, 0, 0), aling="center"):
    # Abra a imagem
    image = img_org
    
    # Calcule o tamanho máximo permitido para o texto
    max_width, max_height = max_size
    
    # Carregue a fonte
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # Inicialize o objeto de desenho
    draw = ImageDraw.Draw(image)

    # Ajuste o tamanho da fonte para que o texto caiba na imagem
    # text_width, text_height = draw.textsize(text, font=font)
    # while text_width > max_width or text_height > max_height:
    #     font_size -= 1
    #     font = ImageFont.truetype(font_path, font_size)
    #     text_width, text_height = draw.textsize(text, font=font)

    # Calcule a posição para centralizar o texto na imagem
    position = pos

    # Desenhe o texto na imagem
    draw.text(position, text, fill=text_color, font=font, align=aling)

    return image

async def search_image(query, amount=1, isnsfw=False):
  if not isnsfw:
    try:
        search_engine_key = '40338feb698df4099'

        # Parâmetros da solicitação
        params = {
            'key': 'AIzaSyAA0zQA-QCJUcJ2mtriu5I0Z4KGuQH_74U',
            'cx': search_engine_key,
            'q': query,
            'searchType': 'image',  # Tipo de pesquisa: imagens
            'num': amount
        }

        # URL da API de pesquisa personalizada do Google
        url = 'https://www.googleapis.com/customsearch/v1'

        # Faz uma solicitação GET para a API de pesquisa personalizada do Google
        response = requests.get(url, params=params)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Obtemos os resultados da pesquisa como um dicionário JSON
            search_results = response.json()
            itemsarray = []
            
            # Verifica se há resultados na resposta
            if 'items' in search_results:
                # Itera sobre cada resultado e imprime o link da imagem
                for it in search_results['items']:
                  itemsarray.append(it['link'])
                  print(it['link'])
                return itemsarray
            else:
                return 'Nenhum resultado encontrado.'
        else:
            print('Falha ao pesquisar imagens:', response.text)
            return 'Falha ao pesquisar imagens:' + response.text
    except Exception as e:
        return "Ocorreu um erro ao realizar a pesquisa:" + str(e)
  else:
    url = f"https://api.rule34.xxx//index.php?page=dapi&s=post&q=index&limit={amount}&tags={query.replace(" ", "_").replace("(", "%28").replace(")", "%29")}&json=1"
    response = requests.get(url)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
      # Obtemos os resultados da pesquisa como um dicionário JSON
      try:
        search_results = response.json()
      except requests.exceptions.JSONDecodeError:
        return [""]
      itemsarray = []
      # print(search_results)
      
      for result in search_results:
        itemsarray.append(result["file_url"])
      return itemsarray
    else:
      print('Falha ao pesquisar imagens:', response.text)
      return 'Falha ao pesquisar imagens:' + response.text
    
def download_avatar(url):
  response = requests.get(url)
  avatar = Image.open(BytesIO(response.content))
  return avatar

def create_quote_with_avatar(message, avatar_url, font_path, output_path, width=500, height=300):
  # Carregar a imagem de fundo
  background = Image.new('RGB', (width, height), color='black')

  # Baixar o avatar da URL
  avatar = download_avatar(avatar_url)
  avatar = avatar.resize((height, height))  # Ajuste o tamanho do avatar conforme necessário

  # gradient = Image.

  # Colocar o avatar no fundo
  background.paste(avatar, (0, 0))  # Ajuste a posição do avatar conforme necessário
  gradient = Image.open("MemeImages/menções/gradient.png")
  background.paste(gradient, (0,0))

  # Carregar a fonte
  font = ImageFont.truetype(font_path, size=100)

  # Criar um objeto de desenho
  draw = ImageDraw.Draw(background)

  # Quebrar a mensagem em linhas para caber na imagem
  lines = textwrap.wrap(message, width=40)

  # Definir a posição inicial para desenhar o texto
  y_text = 120
  for line in lines:
      # Obter o retângulo de delimitação do texto
      bbox = draw.textbbox((0, y_text), line, font=font)
      # Calcular a largura e altura do texto
      width = bbox[2] - bbox[0]
      height = bbox[3] - bbox[1]
      # Desenhar o texto na imagem
      draw.text(((background.width - width) / 2, y_text), line, fill='white', font=font)
      y_text += height + 10

  # Salvar a imagem resultante
  background.save(output_path)

def create_hide_away_img(avatarone, avatartwo, path):
  base = Image.open("MemeImages/hideaway/base.png")
  avatone_pos = [621, 282, 77, 77]
  avattwo_pos = [[111, 178, 184, 184], [994, 267, 125, 125], [630, 53, 77, 77]]
  avatone_img = download_avatar(avatarone)
  avattwo_img = download_avatar(avatartwo)
  base.paste(avatone_img.resize((avatone_pos[2], avatone_pos[3])), (avatone_pos[0], avatone_pos[1]))
  for avatp in avattwo_pos:
    base.paste(avattwo_img.resize((avatp[2], avatp[3])), (avatp[0], avatp[1]))
  base.save(path)

def create_ship_img(base, avatarone, avataronepos, avatartwo, avatartwopos, path):
  base = Image.open("MemeImages/ship/" + base)
  avatone_img = download_avatar(avatarone)
  avattwo_img = download_avatar(avatartwo)
  base.paste(avatone_img.resize((avataronepos[2], avataronepos[3])), (avataronepos[0], avataronepos[1]))
  base.paste(avattwo_img.resize((avatartwopos[2], avatartwopos[3])), (avatartwopos[0], avatartwopos[1]))
  base.save(path)

def adicionar_fundo_branco(imagem_com_transparencia):
  # Abre a imagem
  imagem = imagem_com_transparencia

  # Verifica se a imagem possui canal alpha (transparência)
  if imagem.mode in ('RGBA', 'LA') or (imagem.mode == 'P' and 'transparency' in imagem.info):
      # Cria uma nova imagem com fundo branco
      nova_imagem = Image.new("RGB", imagem.size, "white")
      nova_imagem.paste(imagem, mask=imagem.split()[3])  # Copia a imagem original usando o canal alpha como máscara

      return nova_imagem
  else:
      # Se a imagem não tiver transparência, não é necessário adicionar fundo branco
      return imagem
    