import requests
from pprint import pprint
# from datetime import date
import json
from tqdm import tqdm
import time


class FotoVk:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, vers):
        self.params = {
            'access_token': token,
            'v': vers
        }

    # Создание словаря, с именем и url фотографий для копирования
    def get_foto(self, number=5):
        url_photo_get = self.url + 'photos.get'
        params_photo_get = {
            'owner_id': '263903',
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': number
        }
        new_dict = {}
        new_list = []
        res = requests.get(url_photo_get, params={**self.params, **params_photo_get}).json()
        for n in res['response']['items']:
            new_dict_for_json = {}
            if not n['likes']['count'] in new_dict:
                new_dict[n['likes']['count']] = n['sizes'][len(n['sizes']) - 1]['url']
                new_dict_for_json['file_name'] = str(n['likes']['count'])
                new_dict_for_json['size'] = str(n['sizes'][len(n['sizes']) - 1]['type'])
            else:
                new_dict[str(n['likes']['count']) + '-' + str(n['date'])] = n['sizes'][len(n['sizes']) - 1]['url']
                new_dict_for_json['file_name'] = str(n['likes']['count']) + '-' + str(n['date'])
                new_dict_for_json['size'] = str(n['sizes'][len(n['sizes']) - 1]['type'])
            new_list.append(new_dict_for_json)
        ret = [new_dict, new_list]
        pprint(f'выбрано {number} фотографий для резервного копирования!')
        return ret


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    # Создание папки на яндекс диске
    def new_folder(self, path_folder):
        new_foldee_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": name_folder}
        requests.put(new_foldee_url, headers=headers, params=params)
        pprint(f'ПАПКА: {path_folder},СОЗДАНА ДЛЯ ЗАПИСИ ФОТО НА ЯНДЕКС ДИСК СОЗДАНА!!!')

    # Сохр 1 фото в папку
    def save_foto(self, name_foto: str, url_foto: str, folder: str):
        save_foto_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': str(folder) + '/' + str(name_foto),
                  'url': url_foto
                  }
        requests.post(save_foto_url, headers=headers, params=params)

    # Сохр всех фото в папку
    def save_dict_foto(self, dict_foto: dict, name_folder: str):
        n = 1
        self.new_folder(name_folder)
        for foto_name, foto_url in dict_foto.items():
            pprint(f'На Яндекс диск в папку: {name_folder} копируется: {n} фото')
            n += 1
            self.save_foto(foto_name, foto_url, name_folder)
            pbar = tqdm(total=100)
            for i in range(10):
                time.sleep(0.1)
                pbar.update(10)
            pbar.close()
        pprint('ЗАПИСЬ ЗАВЕРШЕНА!')


if __name__ == '__main__':
    you_token_ya = input('Введите токен от Яндекс диска: ')
    with open("Token.txt", 'r') as f:
        you_token_vk = f.read()
    version = '5.131'
    pf = FotoVk(you_token_vk, version)
    n = input('введите количестово копируемых фото: ')
    list_foto = pf.get_foto(n)
    sec = time.time()
    struct = time.localtime(sec)
    name_folder = str(time.strftime('%d.%m.%Y %H-%M-%S', struct))
    with open("json_foto.json", 'w') as f:
        json.dump(list_foto[1], f, indent=2)
    uploader = YaUploader(you_token_ya)
    uploader.save_dict_foto(list_foto[0], name_folder)
