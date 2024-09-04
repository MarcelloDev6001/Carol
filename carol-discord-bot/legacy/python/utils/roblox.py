import requests
import re
from bs4 import BeautifulSoup
import urllib.parse

def get_roblox_avatar_url(id):
    url = f"https://www.roblox.com/avatar-thumbnails?params=%5B%7BuserId:{id}%7D%5D"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if "thumbnailUrl" in data[0]:
                return data[0]["thumbnailUrl"].replace("AvatarHeadshot", "Avatar").replace("/60/60/", "/420/420/")
            else:
                print("Usuário não encontrado.")
        else:
            print(f"Erro ao obter ID do usuário: {response.status_code}")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

def get_user_id_from_username(username: str):
    url = f"https://www.roblox.com/users/profile?username={username}"
    response = requests.get(url)
    user_id = re.search(r'\d+', response.url).group()
    return user_id

def get_badge_icon_url(badge_id):
    url = f"https://www.roblox.com/badges/{badge_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        icon_element = soup.find('img', class_='badge-icon-image')

        if icon_element:
            icon_url = icon_element['src']
            # A URL retornada é relativa, então precisamos convertê-la para uma URL absoluta
            icon_url = urllib.parse.urljoin(url, icon_url)
            return icon_url
        else:
            print("Ícone da badge não encontrado.")
    else:
        print("Não foi possível acessar a página da badge.")
