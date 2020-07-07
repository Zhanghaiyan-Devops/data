import wget
import os
import re
from urllib import error

def get_url(fname, patt, encoding=None):
    url_list = []
    cpatt = re.compile(patt)
    with open(fname, encoding=encoding)as fobj:
        for line in fobj:
            m = cpatt.search(line)
            if m:
                url_list.append(m.group())

    return url_list

if __name__ == '__main__':
    img_dir = '/mnt/163'
    url163 = 'http://www.163.com'
    fname163 = '/mnt/163/163.html'
    # 如果目录和首页文件不存在,先创建目录并下载首页文件
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    if not os.path.exists(fname163):
        wget.download(url163, fname163)

    # 获取首页上的所有图片
    patt = '(http|https)://[/\w.-]+\.png'
    img_list = get_url(fname163, patt, 'gbk')
    # print(img_list)
    # 下载图片
    for url in img_list:
        try:
            wget.download(url,img_dir)
        except error.HTTPError:
            pass
