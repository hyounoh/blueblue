import time

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from libs.tagger import Tagger
from libs.mysql_controller import MySQLController
from models.petition import *


def crawling():
    # Set dbms
    db = MySQLController()

    # Set tagger module
    tagger = Tagger()

    # Set chrome driver
    driver = set_chrome_driver()
    driver.implicitly_wait(5)

    # Set url
    url_head = 'https://www1.president.go.kr/petitions/?c=0&only=0&page='
    page_num = 1
    url_tail = '&order=0'

    is_first_iter = True
    while True:

        # Generate url of i-th page by using page number
        list_url = url_head + str(page_num) + url_tail
        print(str(page_num) + ' page list: ' + str(list_url))

        # Parse current page
        soup = parse_page(driver, list_url)

        # On a new page, if 'a.on' object doesn't exist then there isn't crawl-able page
        # So, have to quit crawling
        if soup.select('a.on').__len__() == 1:
            break

        # If last crawled petition document id is greater than or equal recent's then quit crawling
        recent_petition_no = list(soup.find('ul', {'class': 'petition_list'}))[0].find('a')['href'].split('/')[2]
        last_crawled_no = db.select_last_petition_id()
        if is_first_iter:
            is_first_iter = False
            if last_crawled_no and int(recent_petition_no) <= last_crawled_no:
                print('Crawling is up-to-date')
                break

        # Handle each document
        petition_list = soup.find('ul', {'class': 'petition_list'})
        for petition in petition_list:

            # Generate url of detail page
            detail_url_head = 'https://www1.president.go.kr'
            detail_url_tail = petition.find('a')['href']
            detail_url = detail_url_head + detail_url_tail

            # Compare this petition's id and last crawled petition's id
            # If current value is less than or equal to last value then quit crawling
            no = detail_url_tail.split('/')[2]
            print('\t' + no + ' petition: ' + detail_url)

            # Extract and analyze title text
            title = petition.find(class_='bl_subject').text.replace('제목 ', '')
            title_pos = tagger.pos(title)
            # print(title_pos)

            # Extract category of this petition
            category = petition.find(class_='bl_category ccategory cs wv_category').text.split(' ')[1].replace('/', ',')

            # Extract a number of participants
            n_participants = int(petition.find(class_='bl_agree cs').text.replace('참여인원 ', '').replace('명', '').replace(',',''))

            # Parse detail page
            soup_detail = parse_page(driver, detail_url)

            # Extract start and expired date
            date_start = soup_detail.find('ul', class_='petitionsView_info_list').find_all('li')[1].text.replace('청원시작', '')
            date_expired = petition.find(class_='bl_date light').text.replace('청원 종료일 ', '')

            # Extract and analyze body text
            body = soup_detail.find('div', class_='View_write').text.replace('\t', '').replace('\n', '')
            body_pos = tagger.pos(body)
            # print(body_pos)

            # Create current petition meta data
            petition_meta = PetitionMeta(no=no, category=category, n_participants=n_participants,
                                         date_expired=date_expired, date_start=date_start,
                                         detail_url=detail_url, title=title)
            petition_meta_id = db.insert_petition_meta(petition_meta)
            # print('petition_meta_id: ', petition_meta_id, 'is inserted')

            # Create current petition body data
            petition_body = PetitionBody(petition_meta_id=petition_meta_id, body=body)
            petition_body_id = db.insert_petition_body(petition_body)
            # print('petition_body_id: ', petition_body_id, 'is inserted')

            # Generate word list of title and body
            # Separate pos tagging result with each word by its morpheme
            words = []
            nn_pos = ['NNG', 'NNP', 'NNB', 'NNM', 'NP']
            for pos in title_pos:
                if pos[1] in nn_pos:
                    word = Word(text=pos[0], morpheme=pos[1], petition_meta_id=petition_meta_id, position='title')
                    words.append(word.__str__())

            for pos in body_pos:
                if pos[1] in nn_pos:
                    word = Word(text=pos[0], morpheme=pos[1], petition_meta_id=petition_meta_id, position='content')
                    words.append(word.__str__())

            db.insert_word(words=words)

            time.sleep(0.5)

        # prepare next page
        page_num += 1

    driver.quit()


def set_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    return webdriver.Chrome('./chromedriver', chrome_options=options)


def parse_page(driver, url):
    driver.get(url)
    sleep(2)
    html = driver.page_source
    return BeautifulSoup(html, 'html.parser')
