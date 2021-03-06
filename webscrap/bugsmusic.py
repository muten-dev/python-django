from bs4 import BeautifulSoup
from urllib.request import urlopen


class BugsMusic(object):
    # __init__이 제거된 것이 아니라 표기가 변경되었을 뿐이다.
    # def __init__(self, url):
    #     self.url = url
    url = ''
    class_name = []

    def __str__(self):
        return self.url

    def scrap(self):
        soup = BeautifulSoup(urlopen(self.url), 'lxml')
        count = 0
        print('=' * 40 + ' < ARTIST > ' + '=' * 40)
        for i in soup.find_all(name='p', attrs=({"class": self.class_name[0]})):
            count += 1
            print(f'{str(count)} {self.class_name[0]} : {i.find("a").text}')

        count = 0
        print('=' * 40 + ' < TITLE > ' + '=' * 40)
        for i in soup.find_all(name='p', attrs=({"class": self.class_name[1]})):
            count += 1
            print(f'{str(count)} {self.class_name[1]} : {i.find("a").text}')

    # https://music.bugs.co.kr/chart/track/realtime/total
    @staticmethod
    def main():
        bugs = BugsMusic()
        while 1:
            print('=' * 10 + ' MENU ' + '=' * 10)
            menu = input('1 INPUT_URL  2 RANK Top100 \n0 EXIT \n>> ')
            if menu == '1':
                # bugs.url = input('input URL')
                bugs.url = 'https://music.bugs.co.kr/chart/track/realtime/total'
            elif menu == '2':
                # print(f'input URL is {bugs}')
                bugs.class_name.append("artist")
                bugs.class_name.append("title")
                bugs.scrap()
            elif menu == '0':
                exit()
            else:
                print('Wrong Number')
                continue


BugsMusic.main()
