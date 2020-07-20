import os
import requests
import wget
import hashlib
import tarfile

def has_new_ver(ver_fname, ver_url):
    '用于判断是否有新版本, 有新版本返回Ture'
    # 如果本地没有版本文件, 则有新版本; 本地和远程版本不一样,有新版本
    if not os.path.isfile(ver_fname):
        return True

    # 取出远程版本号
    r = requests.get(ver_url)

    # 远程版本和本地版本比较
    with open(ver_fname) as fobj:
        local_ver = fobj.read()

    if local_ver != r.text:
        return True
    else:
        return False


def check_app(md5_url, app_fanem):
    '用于校验软件包是否完好, 完好返回True'

    # 计算本地md5值
    m = hashlib.md5()
    with open(app_fanem, 'rb') as fobj:
        while 1:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)

    # 取出网上公布的md5值
    r = requests.get(md5_url)

    # 判断两个值是否相等
    if m.hexdigest() == r.text.strip():
        return True
    else:
        return False

def deploy(app_fanem, deploy_dir):
    '部署软件包到web服务器'

    # 解压到部署目录
    tar = tarfile.open(app_fanem)
    tar.extractall(path=deploy_dir)
    tar.close()

    # 拼接出解压目录的绝对路径
    dest = app_fanem.split('/')[-1]
    dest = dest.replace('.tar.gz', '')
    dest = os.path.join(deploy_dir, dest)

    # 创建链接
    link = '/var/www/html/new_version'
    if os.path.exists(link):    # 如果链接文件已存在,先删除,否则会失败
        os.remove(link)
    os.symlink(dest, link)

if __name__ == '__main__':
    # 判断有没有新版本, 没有则退出
    ver_fname = '/var/www/deploy/new_ver'
    ver_url = 'http://192.168.1.7/deploy/new_ver'
    if not has_new_ver(ver_fname, ver_url):
        print('未发现新版本')
        exit(1)
    # 下载新版本软件包
    r = requests.get(ver_url)
    ver = r.text.strip()    # 去除文件结尾的\n
    app_url = 'http://192.168.1.7/deploy/pkgs/website-%s.tar.gz' % ver
    download_dir = '/var/www/download'
    wget.download(app_url,download_dir)

    # 校验软件包是否完好, 如果软件包损坏,则删除损坏的包,并退出
    md5_url = app_url + '.md5'
    app_fanem = app_url.split('/')[-1]
    app_fanem = os.path.join(download_dir, app_fanem)
    if not check_app(md5_url, app_fanem):
        os.remove(app_fanem)
        print('文件已损坏')
        exit(2)

    # 部署软件包
    deploy_dir = '/var/www/deploy'
    deploy(app_fanem, deploy_dir)

    # 更新本地软件版本文件
    if os.path.exists(ver_fname):
        os.remove(ver_fname)
    wget.download(ver_url, ver_fname)



