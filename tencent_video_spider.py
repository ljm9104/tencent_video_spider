# -*- coding:utf-8 -*-
import csv
import logging

import requests
import time
from pymongo import MongoClient

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


def get_info(cid):
    url = "https://node.video.qq.com/x/api/float_vinfo2"
    info = {}
    querystring = {"cid": cid}
    res = requests.get(url, headers=headers, params=querystring)
    res = res.json()
    try:
        # 电影cid, 电影播放页面的url最后的字符串
        info["cid"] = cid
        # 电影标题
        info["title"] = res.get("c", {}).get("title", "")
        # 电影url
        info["url"] = "https://v.qq.com/x/cover/{}.html".format(cid)
        # 电影类型
        # info["typ"] = ",".join(res["typ"][0]) + ",".join(res["typ"][-1])
        info["typ"] = str(res.get("typ", [])).replace("'", "").replace("[", "").replace("]", "")
        # 主演
        info["nam"] = str(res.get("nam", [])).replace("'","").replace("[", "").replace("]", "")
        # 电影亮点
        info["rec"] = res.get("rec", "")
        # 电影video_ids, 有的有上下集,电视剧综艺就是该剧下的分集
        info["video_ids"] = ",".join(res["c"].get("video_ids", ""))
        # 出版年份
        info["year"] = res.get("c", {}).get("year", "")
        # 电影简介
        info["description"] = res.get("c", {}).get("description", "").strip().replace("\n", "").replace("\r", "")
        # 电影vid
        info["vid"] = res.get("c", {}).get("vid", "")
        # 该电影的精彩片段
        info["clips_ids"] = ",".join(res.get("c", {}).get("clips_ids", ""))
        # 电影海报图
        info["pic"] = res.get("c", {}).get("pic", "")
        # 电影评分分类, "cup": 金马奖, "douban": 豆瓣高分, "weibo": 微博高分, 1表示高分，0表示没有该标签
        info["cup"] = res.get("sell", {}).get("cup", "")
        info["douban"] = res.get("sell", {}).get("douban", "")
        info["weibo"] = res.get("sell", {}).get("weibo", "")
        # 最热门的一条影评, 头像，昵称，以及评论
        info["head"] = res.get("comment", {}).get("head", "")
        info["nick"] = res.get("comment", {}).get("nick", "")
        info["comment"] = res.get("comment", {}).get("content", "").replace("\n", "").replace("\r", "")
    except Exception as e:
        print("API数据不标准%s" % e)
    return info


def save_info():
    with open("movie_id.csv", encoding="utf-8") as f, open("sample.csv", "w", encoding="utf-8", newline="") as sample:
        id_list = [line.strip().split("\t")[-1] for line in f.readlines()]
        # print(id_list)
        f.close()
        head = ["title", "url", "cid", "vid", "clips_ids", "year", "typ", "nam", "rec", "video_ids", "pic",
                "description",
                "cup", "douban", "weibo", "head", "nick", "comment"]
        csv_f = csv.DictWriter(sample, fieldnames=head)
        csv_f.writeheader()
        for cid in id_list:
            info = {}
            info = get_info(cid)
            csv_f.writerow(info)
            print("正在保存cid：{}".format(info["cid"]))


def save_mongodb(cid, collection_name="demo"):
    client = MongoClient()
    # 连接test数据库，没有则自动创建
    db = client.tencent
    # 使用collection集合，没有则自动创建
    collection = db[collection_name]
    info = get_info(cid)
    print("正在保存cid：{}".format(info["cid"]))
    collection.insert(info)
    client.close()


def get_cid(file_name):
    with open(file_name, encoding="utf-8") as f:
        for line in f:
            cid = line.strip().split("/cover/")[-1].split(".")[0]
            yield cid


if __name__ == '__main__':
    # save_info()
    # 修改要打开的文件，改下set名字，和之前存的区分开
    cid_gen = get_cid("tv_url.txt")
    for cid in cid_gen:
        save_mongodb(cid, collection_name="tv")
