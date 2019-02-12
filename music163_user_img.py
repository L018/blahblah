#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# author: zero
# Date: 2018/12/14 20:17

'''
云音乐新歌榜 100 首 首页评论用户头像、昵称demo
'''
import requests
from lxml import etree
import copy
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

headers = {
    "Connection": "keep-alive",
    'Referer': 'https://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}
base_url = 'https://music.163.com'


def start():
    '提取100首歌曲地址'
    url = "https://music.163.com/discover/toplist?id=3779629"
    req = requests.get(url, headers=headers)
    songs = etree.HTML(req.text).xpath('//ul[@class="f-hide"]/li/a/@href')
    return songs


def parse_comment(songs=None):
    for song in songs:
        s = requests.Session()
        req = s.get(base_url + song, headers=headers)  # 愣是没找到set-cookies
        # print(s.cookies)
        # cid = etree.HTML(req.text).xpath("//div[@id='comment-box']/@data-tid")[0]
        song_id = song.split("=")[-1]
        comment_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)
        hed = copy.copy(headers)
        hed['Referer'] = base_url + song
        cookies = {
            '_ntes_nuid': '27450949fb265ca46f2c6871c9f234cc'  # 基本不会过期，100年
        }
        params, encSecKey = gendata(song_id, 1)  # 这里暂时只下载第一页
        data = {
            "params": params,
            "encSecKey": encSecKey
        }
        req = s.post(comment_url, headers=hed, data=data, cookies=cookies)
        for comment in req.json()['comments']:
            url = comment['user']['avatarUrl'] + '?param=180y180'
            file_name = comment['user']['nickname'] +'@@'+ url.split('/')[-1].split('?')[0]
            with open('m163img/'+file_name, 'wb') as f:
                f.write(requests.get(url, headers=hed).content)
                print(url)


"""
var bMi1x = window.asrsea(JSON.stringify(i7b), bvL5Q(["流泪", "强"]), bvL5Q(VK4O.md), bvL5Q(["爱心", "女孩", "惊恐", "大笑"]));
    e7d.data = k7d.cB8t({
        params: bMi1x.encText,
        encSecKey: bMi1x.encSecKey
    })
"""


def gendata(song_id, page):
    "根据歌曲id 以及对应评论的页数，生成请求 data 参数"
    random_s = "BXMHdNVYjA9XGc07"  # 随机生成的字符串，这里就直接指定了
    params = '{"rid":"R_SO_4_%s","offset":"%d","total":"false","limit":"20","csrf_token":""}'%(song_id, (page-1)*20)
    # "{"rid":"R_SO_4_1334647784","offset":"0","total":"true","limit":"20","csrf_token":""}"
    # print(params)
    # 三个固定值，js版本发生变化，则其有可能会发生变化
    e = "010001"
    f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    g = "0CoJUm6Qyw8W8jud"
    encText = AES_(params, g)
    encText = AES_(encText, random_s)
    encSecKey = RSA_(random_s, e, f)
    return (encText, encSecKey)


def AES_(text, key):
    "使用 key 对 text 进行加密，返回字符串形式加密数据"
    iv = b"0102030405060708"
    padder = padding.PKCS7(128).padder()  # 补位数cha(N)填充
    padded_data = padder.update(text.encode())
    padded_data += padder.finalize()
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key.encode()), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(ct).decode()


def RSA_(s, e, f):
    "返回加密后的字符串"
    # 虽然没看懂，但是s, e, f 固定，那么encSecKey 就固定啊，
    random_s = "BXMHdNVYjA9XGc07"
    return "bb140b15f180e1e9ca3807b56f7c8d0db859a93aeec7a81bda90f0fefaf94f86f31ff78bb51551b54f7d008ffd3a28eb464bbb998b801922abf5906b62bffdf93c17d78493c56eac4119b3553cc196c717a21b2c001888a54ef75ff5515c4256c54d2e146e22124322211b2bcc9189d17bae75bc65f3004772ed9709dec53f1c"


if __name__ == "__main__":
    songs = start()
    parse_comment(songs)
