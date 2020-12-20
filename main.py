from dhooks import Webhook
from requests import get
from bs4 import BeautifulSoup
from googletrans import Translator
from time import sleep
from pandas import DataFrame, read_excel

year = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}
url = "https://www.warmane.com/"
req = get(url)
soup = BeautifulSoup(req.content, 'html.parser')

content = soup.find_all('div', {'class': 'wm-ui-article-content'})
titles = soup.find_all('div', {'class': 'wm-ui-article-title'})

news_list = []
for i in range(len(content)):

    links = ''
    for link in content[i].find_all('a', href=True):
        links += link['href'] + '\n'

    date = titles[i].find_all('p')[1].get_text().replace(',', '').split(' ')
    if len(date) > 3:
        date = [date[0], '0' + date[2], date[3]]

    news_list.append(
        {
            'date': f'{date[2]}.{year[date[0]]}.{date[1]}',
            'title': titles[i].find_all('p')[0].get_text(),
            'article_text': content[i].find('p').get_text(),
            'links': links
        }
    )

last_news = read_excel('last_news.xlsx').to_dict(orient='records')[0]
last_date = int(last_news['date'].replace('.', ''))

hot_news_list = []
one_date_news_list = []
for news in news_list:
    if int(news['date'].replace('.', '')) > last_date:
        hot_news_list.append(news)
    if int(news['date'].replace('.', '')) == last_date:
        one_date_news_list.append(news)

for news in one_date_news_list:
    if news['title'] == last_news['title'] \
            and news['article_text'] == last_news['article_text'] \
            and news['links'] == last_news['links']:
        break
    else:
        hot_news_list.append(news)

if len(hot_news_list) > 0:
    print(f'Найдено {len(hot_news_list)} непубликованных новостей')
    hook = Webhook(f"https://discord.com/api/webhooks/"
                   f"{open('C:/Google Drive/program/matirials_discord_webhook/warmane_news_hook.txt').read()}")
    t_sleep = 10
    for news in reversed(hot_news_list):
        article_text_ru = Translator().translate(news['article_text'], src='en', dest='ru').text
        hook.send(f"-------------------------------------------\n\n"
                  f"> **{news['title']}** \n"
                  f"> `{news['date']}`\n\n"
                  f"*{article_text_ru}*\n\n"
                  f"{news['article_text']}\n"
                  f"{news['links']}")
        print(f'Запись опубликована. Ожидаем {t_sleep} секунд.')
        sleep(t_sleep)

    print('Done!\n')
    DataFrame.from_dict([news]).to_excel('last_news.xlsx', index=False)
    print('Последняя опубликованная новость сохранена в файл last_news.xlsx\n', news)
print('Нечего грузить!\n')

'''discord_pic = File("")
hook.send('asd', file=discord_pic)'''
