import requests
from pprint import pprint


class FotoVk:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, vers, idd):
        self.params = {
            'access_token': token,
            'owner_id': idd,
            'v': vers
        }

    # Создание словаря, с именем и url фотографий для копирования
    def get_foto(self, number=5):
        url_photo_get = self.url + 'photos.get'
        params_photo_get = {
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': number
        }
        new_dict = {}
        new_list = []
        res = requests.get(url_photo_get, params={**self.params, **params_photo_get}).json()
        if 'error' in res:
            pprint(res['error']['error_msg'])
            ret = 0
        else:

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
        return ret
