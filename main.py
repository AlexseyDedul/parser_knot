import hashlib
import os

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import aiofiles
import lxml


main_url = 'https://www.theknot.com'


colors_dict = {
    'Blue': 'blue',
    'Pink': 'pink',
    'Red': 'berry',
    'White': 'white',
    'Purple': 'purple',
    'Brown': 'copper',
    'Black': 'BLK',
    'Green': 'GRN',
    'Orange': 'ORG',
    'Teal': 'TEA',
    'Grey': 'GRY',
    'Cream': 'CRM',
    'Multi-Color': 'MUL',
    'Burgundy': 'BUR',
    'Gold': 'GLD',
    'Yellow': 'YEL',
    'Lavender': 'LAV',
}

colors_dict2 = {
    'Blue': 'BLU',
    'Burgundy': 'BUR',
    'Purple': 'PUR',
    'Yellow': 'YEL',
    'White': 'WHT',
    'Black': 'BLK',
    'Navy': 'NVY',
    'Gold': 'GLD',
    'Pink': 'PNK',
    'Grey': 'GRY',
    'Green': 'GRN',
    'Red': 'RED',
    'Teal': 'TEA',
    'Brown': 'BRN',
    'Lavender': 'LAV',
    'Multi-Color': 'MUL',
    'Orange': 'ORG',
    'Cream': 'CRM'
}


urls_data = [
    {
        'url': "/paper/invitations",
        'param': '?pageNumber=',
        'page_count': 80
    },
    {
        'url': "/paper/ceremony-reception",
        'param': '?pageNumber=',
        'page_count': 118
    },
    {
        'url': "/fashion/engagement-rings",
        'param': '?page=',
        'page_count': 11
    },
    {
        'url': "/fashion/wedding-dresses",
        'param': '?page=',
        'page_count': 94
    },
    {
        'url': "/fashion/tuxedos",
        'param': '?page=',
        'page_count': 3
    },
    {
        'url': "/fashion/bridesmaid-dresses",
        'param': '?page=',
        'page_count': 20
    },
    {
        'url': "/fashion/mother-of-the-bride-dresses",
        'param': '?page=',
        'page_count': 4
    },
    {
        'url': "/fashion/flower-girl-dresses",
        'param': '?page=',
        'page_count': 1
    },
    {
        'url': "/fashion/wedding-rings",
        'param': '?page=',
        'page_count': 3
    },
    {
        'url': "/fashion/wedding-jewelry",
        'param': '?page=',
        'page_count': 4
    },
    {
        'url': "/fashion/wedding-accessories",
        'param': '?page=',
        'page_count': 5
    },
    {
        'url': "/fashion/short-wedding-dresses",
        'param': '?page=',
        'page_count': 1
    },
    {
        'url': "/fashion/wedding-hair-pins-combs-clips",
        'param': '?page=',
        'page_count': 1
    },
    {
        'url': "/fashion/wedding-shoes",
        'param': '?page=',
        'page_count': 2
    },
]


async def get_page_data_fashion(current_url, param, session, page):
    URL = main_url + current_url + param + str(page)
    if not os.path.exists('./resourse/'):
        os.makedirs('./resourse/')
    folder = f'./resourse{current_url}'
    if not os.path.exists(folder):
        os.makedirs(folder)

    async with session.get(url=URL) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        main_div = soup.find('div', attrs={'class': "row mobile-grid-cards"})
        subdiv_list = [a for a in main_div.findAll('div', attrs={'role': "listitem"}) if main_div is not None]

        for subdiv in subdiv_list:
            d_tag = subdiv.find('div', attrs={'class': "product-card-heading panel-heading"})
            a_tag = d_tag.find('a') if d_tag is not None else None

            if a_tag is None:
                break

            card_url = main_url + a_tag['href']

            async with session.get(url=card_url) as response_card:
                soup_card = BeautifulSoup(await response_card.text(), 'lxml')
                main_tag = soup_card.find('main')
                id = main_tag.findChild('span') if main_tag is not None else None

                if id is not None:
                    try:
                        get_attr = f'data-{id["id"]}'
                        id_attr = id[f'{get_attr}']
                    except KeyError:
                        pass

                    # print(id_attr)
                    current_folder = f'{folder}/{id_attr}'
                    if not os.path.exists(current_folder):
                        os.makedirs(current_folder)

                print(f'{current_url}: {page}')
                ul_tag = main_tag.findChild('ul', attrs={'class': "carousel-hero-list list-unstyled"}) if main_tag is not None else None
                if ul_tag is not None:
                    li_tags_list = ul_tag.findChildren('li')

                    if li_tags_list is not None:
                        for li in li_tags_list:
                            img = li.find('img')
                            try:
                                img_link = img['src']
                            except:
                                img_link = img['data-src']
                            filename = f"{img_link.replace(' ', '_').replace('/', '_').replace('.', '_').replace(':', '_') + '.jpg'}"
                            sv_path = f'{current_folder}/{filename}'
                            await save_img_to_folder(sv_path, img_link, session)


async def get_page_data_paper(current_url, param, session, page):
    URL = main_url + current_url + param + str(page)
    if not os.path.exists('./resourse/'):
        os.makedirs('./resourse/')
    folder = f'./resourse{current_url}'
    if not os.path.exists(folder):
        os.makedirs(folder)

    async with session.get(url=URL) as response:
        print(response)
        soup = BeautifulSoup(await response.text(), 'lxml')
        div = soup.find('div', attrs={'class': "catalogGrid--cd4cd"})
        tag_a = div.find_all('a') if div is not None else None

        if tag_a is not None:
            listA = []
            for i in tag_a:
                listA.append(i['href'])

            setA = set(listA)
            for i in setA:
                cur_url = main_url + i
                async with session.get(url=cur_url) as response2:
                    if response2.status == 200:
                        soup2 = BeautifulSoup(await response2.text(), 'lxml')

                        h1 = soup2.find('div', {'data-testid': 'ProductDetailHeader'}).find('h1').text
                        id = hashlib.md5(h1.encode()).hexdigest()
                        current_folder = f'{folder}/{id}'
                        if not os.path.exists(current_folder):
                            os.makedirs(current_folder)
                        try:
                            colors_list = [x['value'] for x in
                                           soup2.find('div', {'data-testid': 'ProductDetailColors'}).find_all('input')]
                            main_color = colors_list[0]
                        except:
                            pass
                        ulTag = soup2.find('ul', attrs={'role': 'list', 'class': 'slidesList--d2312'})
                        liTag = ulTag.find_all('li') if ulTag is not None else None
                        if liTag is not None:
                            list_img = []
                            for li in liTag:
                                img = li.find('img')['src']

                                for color in colors_list:
                                    list_img.append(img.replace(colors_dict[main_color], colors_dict[color]))

                            print(f'{id}:{list_img}')
                            for cur_img in list_img:
                                filename = f"{cur_img.replace(' ', '_').replace('/', '_').replace('.', '_').replace(':', '_') + '.jpg'}"
                                sv_path = f'{current_folder}/{filename}'
                                await save_img_to_folder(sv_path, cur_img, session)


async def save_img_to_folder(sv_path, cur_img, session):
    async with session.get(cur_img) as res:
        if res.status == 200:
            f = await aiofiles.open(sv_path, mode='wb')
            await f.write(await res.read())
            await f.close()


async def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls_data:
            current_url = url['url']
            param = url['param']
            pages_count = url['page_count']

            for page in range(1, pages_count + 1): # pages_count + 1
                # print(f'{current_url}: {page}')
                if current_url.find("fashion") == 1:
                    task = asyncio.create_task(get_page_data_fashion(current_url, param, session, page))
                else:
                    task = asyncio.create_task(get_page_data_paper(current_url, param, session, page))
                await asyncio.sleep(.8)
                tasks.append(task)

        await asyncio.gather(*tasks)


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_data())


if __name__ == '__main__':
    run()
