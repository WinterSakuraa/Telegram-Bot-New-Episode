import json
import requests
from bs4 import BeautifulSoup
from os import path


def hero_shield():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'
    }

    url = 'https://animego.org/anime/voshozhdenie-geroya-schita-2-1993'
    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    episodes = soup.find_all(class_="col-12 released-episodes-item")

    def isPosted(status):
        if status == None:
            return False
        else:
            return True

    if not path.exists('hero_shield.json'):
        episodes_dict = {}
        for item in episodes[-5:]:
            item_num = item.find('span').text

            if item_num in episodes_dict:
                continue
            else:
                item_title = item.find(
                    class_="col-5 col-sm-5 col-md-5 col-lg-5 text-truncate font-weight-bold d-none d-sm-block").text.strip()
                item_date = item.find(
                    class_="col-6 col-sm-3 col-md-3 col-lg-3 text-right text-truncate").find('span').text.strip()
                item_status = item.find(
                    class_="col-3 col-sm-2 col-md-2 col-lg-2 text-center").find('use')

                episodes_dict[item_num] = {
                    'episode_num': item_num,
                    'episode_title': item_title,
                    'episode_date': item_date,
                    'isPosted': isPosted(item_status)
                }

        with open('hero_shield.json', 'w') as file:
            json.dump(episodes_dict, file, indent=4, ensure_ascii=False)

        return {}
    else:
        with open("hero_shield.json") as file:
            episodes_dict = json.load(file)

        new_episodes_dict = {}
        for item in episodes[-5:]:
            item_num = item.find('span').text

            if item_num in episodes_dict:
                continue
            else:
                item_title = item.find(
                    class_="col-5 col-sm-5 col-md-5 col-lg-5 text-truncate font-weight-bold d-none d-sm-block").text.strip()
                item_date = item.find(
                    class_="col-6 col-sm-3 col-md-3 col-lg-3 text-right text-truncate").find('span').text.strip()
                item_status = item.find(
                    class_="col-3 col-sm-2 col-md-2 col-lg-2 text-center").find('use')

                episodes_dict[item_num] = {
                    'episode_num': item_num,
                    'episode_title': item_title,
                    'episode_date': item_date,
                    'isPosted': isPosted(item_status)
                }

                new_episodes_dict[item_num] = {
                    'episode_num': item_num,
                    'episode_title': item_title,
                    'episode_date': item_date,
                    'isPosted': isPosted(item_status)
                }

        with open('hero_shield.json', 'w') as file:
            json.dump(episodes_dict, file, indent=4, ensure_ascii=False)

        return new_episodes_dict


def boruto():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'
    }

    url = 'https://jut.su/naruuto/season-3/'
    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    episodes = soup.find_all(class_="short-btn green video the_hildi")

    if not path.exists('boruto.json'):
        episodes_dict = {}
        for item in episodes[-5:]:
            id = str(int(''.join(filter(str.isdigit, item.text[-9:]))))

            if id in episodes_dict:
                continue
            else:
                title = item.get('title')
                number = f"{id} серия"
                link = item.get('href')

                episodes_dict[id] = {
                    'episode_num': number,
                    'episode_title': title,
                    'episode_link': link,
                }

        with open('boruto.json', 'w') as file:
            json.dump(episodes_dict, file, indent=4, ensure_ascii=False)

        return {}
    else:
        with open("boruto.json") as file:
            episodes_dict = json.load(file)

        new_episodes_dict = {}
        for item in episodes[-5:]:
            id = str(int(''.join(filter(str.isdigit, item.text[-9:]))))

            if id in episodes_dict:
                continue
            else:
                title = item.get('title')
                number = f"{id} серия"
                link = item.get('href')

                episodes_dict[id] = {
                    'episode_num': number,
                    'episode_title': title,
                    'episode_link': link,
                }

                episodes_dict = dict(list(episodes_dict.items())[-5:])

                new_episodes_dict[id] = {
                    'episode_num': number,
                    'episode_title': title,
                    'episode_link': link,
                }

        with open('boruto.json', 'w') as file:
            json.dump(episodes_dict, file, indent=4, ensure_ascii=False)

        return new_episodes_dict


def main():
    hero_shield()
    boruto()


if __name__ == '__main__':
    main()
