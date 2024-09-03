import os

def get_playlist(file_name: str):
    try:
        with open(f'data/music/playlists/{file_name}.txt', 'r') as arquivo:
            conteudo = arquivo.read()
            print(f"playlist of {file_name}: {conteudo}")
            return conteudo.split("\n")
    except FileNotFoundError:
        print(f"playlist of {file_name} not found.")
        return None
    except:
        return None
    
def update_playlist(file_name: str, new_music: str):
    conteudo = get_playlist(file_name)
    conteudo_str = ""
    if conteudo is not None:
        for cont in conteudo:
            if cont != "":
                conteudo_str = conteudo_str + cont + "\n"
    with open(f'data/music/playlists/{file_name}.txt', 'w') as file:
        if conteudo is not None:
            file.write(conteudo_str + new_music + "\n")
        else:
            file.write(new_music + "\n")
