#encoding=utf-8
import subprocess
import time
import signal
"""
#父进程等待子进程完成,退出之后会返回0（成功）
return_code=subprocess.call("top")
print return_code

#退出之后返回非0
return_code=subprocess.call(["ifconfig", "eth999"])
print "the return code is %s" % return_code


#自动判断完成状态,可以使用try except进行处理
try:
    subprocess.check_call(["ifconfig", "eth999"])
except subprocess.CalledProcessError as e:
    print e.message,


#返回时执行输出结果
try:
    output=subprocess.check_output(["ifconfig","ens33"])
except subprocess.CalledProcessError as e:
    print "错误处理"
    print e.args
else:
    print "output is \n %s" % output


#Popen函数，父进程不会主动等待子进程
subprocess.Popen('ping 114.215.154.24',shell=True)
print 'parent proess'


#Popen，父进程等待子进程结束
p=subprocess.Popen('ping -c 10 114.215.154.24',shell=True)
p.wait()
print "parent process"

#和子进程交互
p=subprocess.Popen('sar -u 1 10',shell=True)
time.sleep(1)
print p.returncode
time.sleep(1)
print "the pid is %s" % (p.pid)
time.sleep(1)
#传入信号软终止子进程
#p.send_signal(signal.SIGTERM)

time.sleep(3)
p.terminate()

#通过管道，将多个子进程的输入输出连接
p1=subprocess.Popen("cat /etc/passwd ",shell=True,stdout=subprocess.PIPE)
#print p1.stdout.read()
p2=subprocess.Popen("grep root",shell=True,stdin=p1.stdout)


#使用管道执行cat /etc/passwd |awk -F ':' '{print $1}',communicate函数向子进程的
#stdin发送数据，在创建Popen对象时stdin必须设置为PIPE
p1=subprocess.Popen("cat /etc/passwd", shell=True,stdout=subprocess.PIPE)
p2=subprocess.Popen("awk -F ':' '{print $1}'",shell=True,stdin=p1.stdout,stdout=subprocess.PIPE)
(out,ret)=p2.communicate()
print out


#获取进程的输出
p=subprocess.Popen("cat /etc/passwd",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(stdoutput,stderr)=p.communicate()
print stdoutput,stderr
"""

#传入内容给stdin
p=subprocess.Popen("cat test.py",shell=True,stdout=subprocess.PIPE)
while True:
    buff=p.stdout.readline()
    if buff == '' and p.poll()!=None:
        break
    else:
        print buff.strip()+'tag'
























