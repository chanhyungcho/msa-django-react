import csv
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup
from selenium.webdriver.chrome import webdriver

from webcrawler.models import ScrapVO


class ScrapService(ScrapVO):
    def __init__(self):
        global driverpath, naver_url, savepath, encoding
        driverpath = r'C:\Users\AIA\MsaProject\DjangoProject\webcrawler\chromedriver.exe'
        savepath = r'C:\Users\AIA\MsaProject\DjangoProject\webcrawler\save'
        naver_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.naver'
        encoding = 'UTF-8'

    def bugs_music(self,arg): # BeautifulSoup 기본 크롤링
        soup = BeautifulSoup(urlopen(arg.domain + arg.query_string), 'lxml')
        title = {"class": arg.class_names[0]}
        artist = {"class": arg.class_names[1]}
        titles = soup.find_all(name=arg.tag_name, attrs=title)
        titles = [i.find('a').text for i in titles]
        artists = soup.find_all(name=arg.tag_name, attrs=artist)
        artists = [i.find('a').text for i in artists]
        [print(f"{i}위 {j} : {k}")  # 디버깅
         for i, j, k in zip(range(1, len(titles)), titles, artists)]
        diction = {}  # dict 로 변환
        for i, j in enumerate(titles):
            diction[j] = artists[i]
        arg.diction = diction
        arg.dict_to_dataframe()
        arg.dataframe_to_csv()  # csv파일로 저장

    def melon_music(self,arg): # BeautifulSoup 기본 크롤링
        soup = BeautifulSoup(
            urlopen(urllib.request.Request(arg.domain + arg.query_string, headers={'User-Agent': "Mozilla/5.0"})),
            "lxml")
        title = {"class": arg.class_names[0]}
        artist = {"class": arg.class_names[1]}
        titles = soup.find_all(name=arg.tag_name, attrs=title)
        titles = [i.find('a').text for i in titles]
        artists = soup.find_all(name=arg.tag_name, attrs=artist)
        artists = [i.find('a').text for i in artists]
        [print(f"{i}위 {j} : {k}")  # 디버깅
         for i, j, k in zip(range(1, len(titles)), titles, artists)]
        diction = {}  # dict 로 변환
        for i, j in enumerate(titles):
            diction[j] = artists[i]
        arg.diction = diction
        arg.dict_to_dataframe()
        arg.dataframe_to_csv()  # csv파일로 저장

    def naver_movie_review(self):
        driver = webdriver.Chrome(f"{driverpath}\\chromedriver")
        driver.get(naver_url)
        soup = BeautifulSoup(driver.page.source, 'html.parser')
        all_divs = soup.find_all('div',attrs={'class', 'tit3'})
        products = [[div.a.string for div in all_divs]]
        with open(savepath, 'w', newline='', encoding=encoding) as f:
            wr = csv.writer(f)
            wr.writerows(products)
        driver.close()