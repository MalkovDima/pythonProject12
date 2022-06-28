import requests
from pprint import pprint
from datetime import date


class FotoVk:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, vers):
        self.params = {
            'access_token': token,
            'v': vers
        }

    # Создание словаря, с именем и url фотографий для копирования
    def get_foto(self, number='5'):
        url_photo_get = self.url + 'photos.get'
        params_photo_get = {
            'owner_id': '263903',
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': number
        }
        new_dict = {}
        res = requests.get(url_photo_get, params={**self.params, **params_photo_get}).json()
        for n in res['response']['items']:
            if not n['likes']['count'] in new_dict:
                new_dict[n['likes']['count']] = n['sizes'][len(n['sizes']) - 1]['url']
            else:
                new_dict[str(n['likes']['count']) + '-' + str(n['date'])] = n['sizes'][len(n['sizes']) - 1]['url']
        pprint(f'выбрано {number} фотографий для резервного копирования!')
        return new_dict


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    # Создание папки на яндекс диске
    def new_folder(self, folder_path):
        new_foldee_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": folder_path}
        requests.put(new_foldee_url, headers=headers, params=params)
        pprint(f'Папка: {folder_path}, для записи фото на Яндекс диск создана!!!')

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
        n = 0
        self.new_folder(name_folder)
        for foto_name, foto_url in dict_foto.items():
            n += 1
            self.save_foto(foto_name, foto_url, name_folder)
            pprint(f'На Яндекс диск в папку: {name_folder} скопорировано: {n} фото')
        pprint('Запись завершена!')


if __name__ == '__main__':
    you_token_vk = 'vk1.a.VP07pMoVEp8JfVIGqYHFCtHHFvhJVmRERRdrFnyzvtVkH-N2oDBA_L1XtYlQ65jrAR9_OCJZFgZ-SO3kiK' \
                   '-OUfrSgAfc5ioMTR7ujzV9503bWwOqbPqEJVEdUljlCAv7dGmei5wXGhzzhIaYOtzij2t2irvAC2KHvAY0KfYfMTCuVd-z_' \
                   '-fgrrDWtyp3avyL '
    version = '5.131'
    pf = FotoVk(you_token_vk, version)
    dict_foto = pf.get_foto()
    name_folder = str(date.today())
    you_token_ya = 'AQAAAABiV6hBAADLW0MczaVdtUkUvEAkcVVYNj8'
    uploader = YaUploader(you_token_ya)
    uploader.save_dict_foto(dict_foto, name_folder)
