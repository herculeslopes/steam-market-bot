import requests, bs4
from os import system, mkdir
from time import sleep

system('color')

skin_name = input('Enter a skin: \033[36m')
print('\033[m', end='')

url = f'https://steamcommunity.com/market/search?q={"+".join(skin_name.split())}#p1_price_asc'
print(f'Steam url: {url}')

print()


try:
    mkdir('price_log')
    print('Folder /price_log created')
except FileExistsError:
    print('Folder log: /price_log')

searches = 0
while True:
    if searches != 0:
        print('\033[33m')
        for i in range(0, 10):
            print(f'{i + 1} ', end='', flush=True)
            # print('█', end='', flush=True)
            sleep(2)
        print('\033[m\n')

    res_obj = requests.get(url)

    soup = bs4.BeautifulSoup(res_obj.text, 'lxml')

    elements = soup.find("div", {"id": "searchResultsRows"})
    skin_urls = elements.find_all('a', {'class': 'market_listing_row_link'})

    if len(skin_urls) == 0: 
        print(f'\033[31mSkin not found\033[m')
        break

    skin_names = elements.find_all('span', {'class': 'market_listing_item_name'})
    skin_prices = elements.find_all('span', {'class': 'normal_price'})

    if searches == 0: best_option = []

    for i in range(len(skin_urls)):
        link = skin_urls[i]['href']
        skin = skin_names[i].text
        price = [p for p in skin_prices[i].text.split() if p.startswith('$')][0]

        print(f'Link: \033[34m{link}\033[m')
        print(f'Skin: \033[36m{skin}\033[m')
        print(f'Price: \033[31m{price}\033[m')

        if i == 0 and searches == 0: best_option = [link, skin, price]
        elif float(price[1:]) < float(best_option[2][1:]): 
            best_option = [link, skin, price]



    with open(f'price_log/best_price_{"_".join(skin_name.split())}.txt', 'wt') as file:
        file.write(f'Link: {best_option[0]}\n')
        file.write(f'Skin: {best_option[1]}\n')
        file.write(f'Price: {best_option[2]}\n')

    searches += 1

    print()
    print('Best option:')
    print(f'Link: {best_option[0]}')
    print(f'Skin: {best_option[1]}')
    print(f'Price: \033[32m{best_option[2]}\033[m')

print()
print('Script terminated')
