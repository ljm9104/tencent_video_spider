import time
from lxml import etree

import requests

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "pgv_pvid=4657089591; pgv_pvi=8593980416; RK=gZb5MpdxXL; "
              "ptcz=f3218bf3228ed59c3d94d8f2d6664875abfd4eab333811aadd77553640f0f422; "
              "_ga=GA1.2.1279347936.1521472269; ts_uid=2618968896; pt2gguin=o1037825560; "
              "o_cookie=1037825560; pac_uid=1_1037825560; tvfe_boss_uuid=f7dbecfe1ef0d2f5; "
              "pgv_info=ssid=s7677232720; ts_refer=www.baidu.com/link; "
              "tvfe_search_uid=3788c468-23ac-4cfd-972a-d02d1d8e1018; "
              "qv_als=0TFLqxuipR/lMxKuA11527780401xCyG6Q==; ad_play_index=71; "
              "ts_last=v.qq.com/x/list/movie; ptag=www_baidu_com|x",
    "if-modified-since": "Thu, 31 May 2018 22:40:00 GMT",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/66.0.3359.181 Safari/537.36",
}


def get_name_url(url):
    with requests.get(url, headers=headers) as res:
        if res.status_code == 200:
            html = etree.HTML(res.content)
            names = html.xpath('//li[@class="list_item"]/a/img/@alt')
            urls = html.xpath('//li[@class="list_item"]/a/@href')
            print("%s页面爬取成功" % url)
        else:
            print("连接超时")

    return names, urls


def save_name_url(url):
    names, urls = get_name_url(url)
    with open("urls.txt", "a", encoding="utf-8") as f:
        for name, url in zip(names, urls):
            f.write("\t".join([name, url]) + "\n")


if __name__ == '__main__':
    # TV
    # movie
    # cartoon
    # variety
    # for num in range(0, 3631, 30):
    for num in range(0, 3631, 30):
        url = "http://v.qq.com/x/list/tv?&offset="
        url = url + str(num)
        save_name_url(url)
        time.sleep(3)
