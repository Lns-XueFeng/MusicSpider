# -*- coding: utf-8 -*-
"""
Created on 2022-02-22 22:23:00
---------
@summary:
---------
@author: xuefeng
"""

import feapder
import random
import sqlite3


def inert_data(data):
    # 连接数据库(如果不存在则创建)
    conn = sqlite3.connect('Newkuwo_SongUrls.db')
    # 创建游标
    cursor = conn.cursor()
    # 插入数据 e2
    sql = "INSERT INTO songUrls(name, songName, songUrl) VALUES(?, ?, ?)"
    cursor.execute(sql, data)
    # 提交事物
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()


class KuWoSpider(feapder.AirSpider):
    pages = 1

    def start_requests(self):
        for i in range(1,177): # 歌手页
            params = {
                "category": "0", # 0是全部，1是华语男，2是华语女，以此类推
                "prefix": "",
                "pn": i, # 翻页
                "rn": "102",
                "httpsStatus": "1",
                "reqId": "888fc650-96ba-11ec-a249-1b3d13c1e635"
            }
            yield feapder.Request("http://www.kuwo.cn/api/www/artist/artistInfo?",params=params)

    def gain_csrf(self):
        """
        伪造csrf加密参数
        :return:
        """
        e = 'abcdefghizklmnopqrstuvwxyz1234567890'
        eList = []
        for i in e.upper():
            eList.append(i)

        csrf = ''
        for i in range(11):
            csrf = csrf + random.choice(eList)

        return csrf

    def download_midware(self, request):

        csrf = self.gain_csrf()
        # print(csrf)
        request.headers = {
            'user-agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          f'Chrome/86.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36',
            'Referer': 'http://www.kuwo.cn/',
            'Cookie': '_ga=GA1.2.391452555.1639527875; _gid=GA1.2.248719171.1640241599; _gat=1; '
                      'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1639544812,1639550600,1640241599,1640241611; '
                      'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1640241611; kw_token={}'.format(csrf),
            'csrf': csrf,
        }
        return request

    def parse(self, request, response):
        # print(response.json)
        results = response.json['data']['artistList']
        for result in results:
            id = str(result['id'])  # 每一位歌手的唯一id
            name = str(result['name'])
            print(name) #在这里输出歌手名字包含下面循环他的歌曲页，包含

            musicnum = int(result['musicNum'])
            pages = int(musicnum/30) + 1

            for i in range(1,pages+1):
                # 歌曲详情页http://www.kuwo.cn/singer_detail/336
                url = ' http://www.kuwo.cn/api/www/artist/artistMusic?'
                params = {
                    "artistid": id,
                    "pn": i, #翻页
                    "rn": "30",
                    "httpsStatus": "1",
                    "reqId": "b23fbe00-9909-11ec-a249-1b3d13c1e635"
                }
                yield feapder.Request(url,params=params,callback=self.parse_ajax, name=name)

    def parse_ajax(self, request, response):
        name = request.name

        results = response.json['data']['list']
        for result in results:
            rid = str(result['rid'])
            songname = str(result['name'])
            songurl = 'https://link.hhtjim.com/kw/{}.mp3'.format(rid)
            print(songname +':'+ songurl)
            # 入库
            data = (name, songname, songurl)
            inert_data(data)


if __name__ == "__main__":
    KuWoSpider().start()
