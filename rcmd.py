import getpass
import paramiko
import os
import threading
import sys

def rcmd(host, user='root', passwd=None, port=22, commands=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=passwd, port=port)
    stdin, stdout, stderr = ssh.exec_command(commands)

    out = stdout.read()
    err = stderr.read()

    if out:
        print('[\033[32;1m%s\033[0m] out:\n%s' % (host, out.decode()))
    if err:
        print('[\033[32;1m%s\033[0m] err:\n%s' % (host, err.decode()))

    ssh.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('用法: %s IP文件 "命令"' % sys.argv[0])
        exit(1)

    # 地址文件必须存在
    if not os.path.isfile(sys.argv[1]):
        print('没有这样的文件 ')
        exit(2)

    ipfile = sys.argv[1]
    commands = sys.argv[2]
    password = getpass.getpass()

    # 打开文件, 读取地址, 执行命令
    with open(ipfile) as fobj:
        for i in fobj:
            ip = i.strip()  # 支除行尾的加车才是IP地址
            t = threading.Thread(
                target=rcmd, args=(ip,),
                kwargs={'passwd': password, 'commands': commands}
            )
            t.start()   # 相当于执行rcmd(*agrs, **kwargs)