#encoding=utf-8
import fcntl
import os,time
FILE="conter.txt"

if not os.path.exists(FILE):
    #生成一个文件，如果不存在的话
    file = open(FILE,"w")
    file.write("0")
    file.close()

for i in range(20):
    #由于flock生成的是劝告锁，不能阻止进程对文件的操作
    #所以这里可以正常打开文件
    file=open(FILE,"r+")
    print file.fileno()
    fcntl.flock(file.fileno(),fcntl.LOCK_EX)
    print 'acquire a lock...'
    counter=int(file.readline())+1
    file.seek(0)
    file.write(str(counter))
    print os.getpid(),"=>",counter
    time.sleep(2)
    file.close() #释放锁
    print 'release lock....'
    time.sleep(2)

