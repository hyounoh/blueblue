import time

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from libs.tagger import Tagger
from libs.mysql_controller import MySQLController
from models.petition import *

# tagger setting
tagger = Tagger()

# chrome driver setting
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.implicitly_wait(5)

# dbms setting
db = MySQLController()


def crawling():
    print('crawling...')

    url_head = 'https://www1.president.go.kr/petitions/?c=0&only=0&page='
    page_num = 1
    url_tail = '&order=0'

    has_next_data = True
    while has_next_data:

        # get i-th page
        list_url = url_head + str(page_num) + url_tail

        print('#' + str(page_num) + ' list url: ' + str(list_url))

        # parse current page
        driver.get(list_url)

        sleep(2)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        # 새로운 페이지를 호출했을 때 a.on 개체가 없으면 요청한 페이지가 없어서 강제로 마지막 페이지를 호출한것임
        if soup.select('a.on').__len__() == 1:
            has_next_data = False
            continue

        # handle each document
        petition_list = soup.find('ul', {'class': 'petition_list'})
        for petition in petition_list:

            # handle current document info
            no = petition.find(class_='bl_no').text.split(' ')[1]
            category = petition.find(class_='bl_category ccategory cs wv_category').text.split(' ')[1].replace('/', ',')

            # title text analyzing
            title = petition.find(class_='bl_subject').text.replace('제목 ', '')
            title_pos = tagger.pos(title)
            print(title_pos)

            date_expired = petition.find(class_='bl_date light').text.replace('청원 종료일 ', '')
            n_participants = int(petition.find(class_='bl_agree cs').text.replace('참여인원 ', '').replace('명', '').replace(',',''))

            # for detail
            detail_url = 'https://www1.president.go.kr' + petition.find('a')['href']
            driver.get(detail_url)

            sleep(2)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            date_start = soup.find('ul', class_='petitionsView_info_list').find_all('li')[1].text.replace('청원시작', '')

            # content text analyzing
            content = soup.find('div', class_='View_write').text.replace('\t', '').replace('\n', '')
            content_pos = tagger.pos(content)
            print(content_pos)

            # TODO: store in db
            petition_meta = PetitionMeta(no=no, category=category, n_participants=n_participants,
                                         date_expired=date_expired, date_start=date_start,
                                         detail_url=detail_url, title=title)
            petition_meta_id = db.insert_petition_meta(petition_meta)
            print('petition_meta_id: ', petition_meta_id, 'is inserted')

            petition_content = PetitionContent(petition_id=petition_meta_id, text=content)
            petition_content_id = db.insert_petition_content(petition_content)
            print('petition_content_id: ', petition_content_id, 'is inserted')

            words = []
            nn_pos = ['NNG', 'NNP', 'NNB', 'NNM', 'NP']
            for pos in title_pos:
                if pos[1] in nn_pos:
                    word = Word(text=pos[0], morpheme=pos[1], petition_id=petition_meta_id, position='title')
                    words.append(word.__str__())

            for pos in content_pos:
                if pos[1] in nn_pos:
                    word = Word(text=pos[0], morpheme=pos[1], petition_id=petition_meta_id, position='content')
                    # words.append(word.__str__())

            db.insert_word(words=words)

            time.sleep(0.5)

        # prepare next page
        page_num += 1
