def split_max_length(text, max_length=2000):
    parts = []
    current_part = ""

    for word in text.split():
        if len(current_part) + len(word) + 1 <= max_length:  # +1 for space
            if current_part:  # If current part is not empty, add a space before adding the word
                current_part += " "
            current_part += word
        else:
            parts.append(current_part)
            current_part = word

    if current_part:
        parts.append(current_part)

    return parts

def split_number(text, max_length=56):
    parts = []
    current_part = ""

    for char in text:
        current_part += char
        if len(current_part) >= max_length:
            parts.append(current_part)
            current_part = ""

    if current_part:
        parts.append(current_part)

    return parts

def convert_to_elements(string, element_symbols):
    string = string.capitalize()  # Capitalizar a primeira letra para facilitar a correspondência
    result = []
    i = 0
    while i < len(string):
        # Tentar pegar dois caracteres
        if i+1 < len(string) and string[i:i+2] in element_symbols:
            result.append(element_symbols[string[i:i+2]])
            i += 2
        # Se não encontrar, tentar pegar um caractere
        elif string[i] in element_symbols:
            result.append(element_symbols[string[i]])
            i += 1
        else:
            return "Não é possível converter a string completamente."
    return ' '.join(result)