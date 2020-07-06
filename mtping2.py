import subprocess
import threading

class Ping:
    def __init__(self,host):
        self.host = host

    def __call__(self):
        result = subprocess.run('ping -c2 %s &> /dev/null' % self.host, shell=True)
        if result.returncode == 0:
            print('%s:up' % self.host)
        else:
            print('%s:down' % self.host)


if __name__ == '__main__':
    ips = ('192.168.1.%s' %i  for i in range(1,255))
    for i in ips:
        # 创建线程
        t = threading.Thread(target=Ping(i))
        # 开启线程
        t.start()