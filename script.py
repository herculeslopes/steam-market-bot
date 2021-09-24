import requests, bs4
from os import system, mkdir
from win10toast import ToastNotifier
from time import sleep

toaster = ToastNotifier()

system('color')

skin_name = input('Enter a skin: \033[36m')
print('\033[m', end='')

print()

print(f''' Quality preferences:
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
| Não preference:  | 0 |
| Battle-Scared:  | 1 |
| Well-Worn:      | 2 |
| Field-Tested:   | 3 |
| Minimal Wear:   | 4 | 
| Factory New:    | 5 |
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
''')

quality = input('Quality preference: ')
notification_price = float(input('Notify on: $'))

if quality == '0':
    url = f'https://steamcommunity.com/market/search?appid=730&q={"+".join(skin_name.split())}#p1_price_asc'
elif quality == '1':
    url = f'https://steamcommunity.com/market/search?appid=730&q={"+".join(skin_name.split())}+battle-scared#p1_price_asc'
elif quality == '2':
    url = f'https://steamcommunity.com/market/search?appid=730&q={"+".join(skin_name.split())}+well-worn#p1_price_asc'
elif quality == '3':
    url = f'https://steamcommunity.com/market/search?appid=730&q={"+".join(skin_name.split())}+field-tested#p1_price_asc'
elif quality == '4':
    url = f'https://steamcommunity.com/market/search?appid=730&q={"+".join(skin_name.split())}+minimal+wear#p1_price_asc'
elif quality == '5':
    url = f'https://steamcommunity.com/market/search?appid=730&q={"+".join(skin_name.split())}+factory-new#p1_price_asc'
else:
    print('Invalid option')
    print('Going with no preference')
    url = f'https://steamcommunity.com/market/search?appid=730&q={"+".join(skin_name.split())}#p1_price_asc'

print(f'Steam url: {url}')

try:
    mkdir('price_log')
    print('Folder /price_log created')
except FileExistsError:
    print('Folder log: /price_log')

print()

searches = 0
while True:
    if searches != 0:
        print()
        print('20sec Timeout: \033[33m', end='')
        for i in range(0, 20):
            print(f'{i + 1} ', end='', flush=True)
            sleep(1)
        print('\033[m\n')

    res_obj = requests.get(url)

    try:
        soup = bs4.BeautifulSoup(res_obj.text, 'lxml')
    except bs4.FeatureNotFound:
        soup = bs4.BeautifulSoup(res_obj.text, 'html.parser')

    elements = soup.find("div", {"id": "searchResultsRows"})
    skin_urls = elements.find_all('a', {'class': 'market_listing_row_link'})

    if len(skin_urls) == 0: 
        print(f'\033[31mSkin not found\033[m')
        break

    skin_names = elements.find_all('span', {'class': 'market_listing_item_name'})
    skin_prices = elements.find_all('span', {'class': 'normal_price'})

    if searches == 0: best_option = {}

    for i in range(len(skin_urls)):
        link = skin_urls[i]['href']
        skin = skin_names[i].text
        price = [p for p in skin_prices[i].text.split() if p.startswith('$')][0]

        print(f'Link: \033[34m{link}\033[m')
        print(f'Skin: \033[36m{skin}\033[m')
        print(f'Price: \033[31m{price}\033[m')

        if i == 0 and searches == 0: best_option = {
            'link': link,
            'skin': skin,
            'price': price
        }

        elif float(price[1:]) < float(best_option["price"][1:]): 
            best_option = {
                'link': link,
                'skin': skin,
                'price': price
            }

    if float(best_option['price'][1:]) <= notification_price:
        toaster.show_toast(best_option['skin'], best_option['price'])
        break;

    with open(f'price_log/best_price_{"_".join(skin_name.split())}.txt', 'wt') as file:
        file.write(f'Link: {best_option["link"]}\n')
        file.write(f'Skin: {best_option["skin"]}\n')
        file.write(f'Price: {best_option["price"]}\n')

    searches += 1

    print()
    print('Best option:')
    print(f'Link: {best_option["link"]}')
    print(f'Skin: {best_option["skin"]}')
    print(f'Price: \033[32m{best_option["price"]}\033[m')

print()
print('Script terminated', end='')
