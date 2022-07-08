import requests
from pprint import pprint
from tqdm import tqdm
import time


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
        new_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": path_folder}
        res = requests.put(new_folder_url, headers=headers, params=params).status_code
        if res == 202 or res == 201:
            pprint(f'ПАПКА: {path_folder},СОЗДАНА ДЛЯ ЗАПИСИ ФОТО НА ЯНДЕКС ДИСК СОЗДАНА!!!')
        else:

            text = res
            return text

    # Сохр 1 фото в папку
    def save_foto(self, name_foto: str, url_foto: str, folder: str):
        save_foto_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': str(folder) + '/' + str(name_foto),
                  'url': url_foto
                  }
        res = requests.post(save_foto_url, headers=headers, params=params)
        if res.status_code == 202 or res.status_code == 201:
            pbar = tqdm(total=100)
            for i in range(10):
                time.sleep(0.1)
                pbar.update(10)
            pbar.close()
        else:
            return res

    # Сохр всех фото в папку
    def save_dict_foto(self, dict_foto: dict, name_folder: str):
        n = 1
        text = self.new_folder(name_folder)
        if text == 201 or text == 202 or not text:
            for foto_name, foto_url in dict_foto.items():
                pprint(f'На Яндекс диск в папку: {name_folder} копируется: {n} фото')
                t = self.save_foto(foto_name, foto_url, name_folder)
                if t:
                    pprint(f'{n} фото не скопировалось в папку: {name_folder}, ошибка: {t.status_code}')
                n += 1
        else:
            pprint(f'произошла ошибка при создании папки:  {text}')
            return
        pprint(f'ПРОЦЕСС ЗАПИСИ ЗАВЕРШЕН!')
