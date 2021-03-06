from bs4 import BeautifulSoup
import requests
import pandas as pd


class BugsMusic(object):

    url = 'https://music.bugs.co.kr/chart/track/realtime/total'
    headers = {'User-Agent': 'Mozilla/5.0'}
    soup = BeautifulSoup()
    class_name = ['title', 'artist']
    title_ls = []
    artist_ls = []
    dict = {}
    df = pd.DataFrame()

    def set_url(self, detail):
        self.url = requests.get(f'{self.url}{detail}', headers=self.headers).text
        self.soup = BeautifulSoup(self.url, 'lxml')
        ls1 = self.soup.find_all(name='p', attrs=({"class": self.class_name[0]}))
        ls2 = self.soup.find_all(name='p', attrs=({"class": self.class_name[1]}))
        for i in ls1:
            self.title_ls.append(i.find("a").text)
        for j in ls2:
            self.artist_ls.append(j.find("a").text)

    def get_ranking(self):
        print('------- 제목 --------')
        print(self.title_ls)
        print('------ 가수 --------')
        print(self.artist_ls)

    def insert_dict(self):
        print('------- {\'제목\': \'가수\'} --------')
        # 1
        # for i in range(0, len(self.title_ls)):
        #     self.dict[self.title_ls[i]] = self.artist_ls[i]
        # 2
        for i, j in zip(self.title_ls, self.artist_ls):
            self.dict[i] = j
        # 3
        # for i, j in enumerate(self.title_ls):
        #     self.dict[j] = self.artist_ls[i]
        print(self.dict)
        for i, j in enumerate(self.dict.keys()):
            print(f'{i}\' {j} - {self.dict[j]}')

    def dict_to_df(self):
        for i, j in zip(self.title_ls, self.artist_ls):
            self.dict[i] = j
        index_no = [i for i, j in enumerate(self.dict.keys())]
        # 1
        # zp = zip(self.dict.keys(), self.dict.values())
        # self.df = pd.DataFrame(zp, index=index_no, columns=['artists', 'titles'])

        # 2
        dt_values = [self.dict.keys(), self.dict.values()]
        print(dt_values)
        dt_keys = ['titles', 'artists']
        n_dt = {}
        # n_dt[dt_keys[0]] = dt_values[0]
        # print(len(dt_keys))
        for i in range(len(dt_keys)):
            n_dt[dt_keys[i]] = dt_values[i]
        self.df = pd.DataFrame(n_dt, index=index_no, columns=dt_keys)
        return self.df

        # dt = self.dict
        # print(dt)
        # self.df = pd.DataFrame.from_dict(dt, orient='index')
        # return self.df
    
    def dict_to_dataframe(self):
        dt = self.dict

    def df_to_csv(self):
        path = './data/bugs1.csv'
        self.df.to_csv(path, sep=',', na_rep='NaN', mode='w', encoding='utf-8-sig')

    @staticmethod
    def main():
        bg = BugsMusic()
        while 1:
            menu = input('0-exit, '
                         '1-input time, 2-output, 3-dict, 4-dataframe ')
            if menu == '0':
                break
            elif menu == '1':
                bg.set_url(input('상세정보 입력'))  # wl_ref=M_contents_03_01
            elif menu == '2':
                bg.get_ranking()
            elif menu == '3':
                bg.insert_dict()
            elif menu == '4':
                print(bg.dict_to_df())
            elif menu == '5':
                bg.df_to_csv()
            else:
                print('Wrong Number')
                continue


BugsMusic.main()