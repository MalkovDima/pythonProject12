from pprint import pprint
import json
import time
import vk
import YandexDisk


if __name__ == '__main__':
    you_token_ya = input('Введите токен от Яндекс диска: ')
    with open("Token.txt", 'r') as f:
        you_token_vk = f.read()
    version = '5.131'
    id_vk = input('Введите id в VK, чьи фото будем копировать: ')
    pf = vk.FotoVk(you_token_vk, version, id_vk)
    list_foto = pf.get_foto()
    if list_foto != 0:
        sec = time.time()
        struct = time.localtime(sec)
        name_folder = str(time.strftime('%d.%m.%Y %H-%M-%S', struct))
        with open("json_foto.json", 'w') as f:
            json.dump(list_foto[1], f, indent=2)
        uploader = YandexDisk.YaUploader(you_token_ya)
        uploader.save_dict_foto(list_foto[0], name_folder)
    else:
        pprint('Модуль VK, читайте ошибку строкой выше')