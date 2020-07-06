import subprocess
import os

def ping(host):
    result = subprocess.run('ping -c2 %s &> /dev/null' % host, shell=True)
    if result.returncode == 0:
        print('%s:up' % host)
    else:
        print('%s:down' % host)


if __name__ == '__main__':
    ips = ('192.168.4.%s' %i  for i in range(1,255))

    for i in ips:
        retval = os.fork()
        if not retval:
            ping(i)
            exit()
    # for i in ips:
    #     ping(i)
    #     retval = os.fork()
    #     if not retval:
    #         print(i)
    #         exit()
