#encoding:utf-8
from jenkinsapi.jenkins import Jenkins
import time
def get_server_instance():
    jenkins_url='http://192.168.50.171:8080'
    server=Jenkins(jenkins_url,username='wangxuemin',password='wangxuemin')
    return server

def get_job_details():
    server=get_server_instance()
    for j in server.get_jobs():
        #使用一个job的名称去初始化一个job对象
        job_instance=server.get_job(j[0])
        print 'Job Name:%s' %(job_instance.name)
        print 'Job Description:%s' %(job_instance.get_description())
        print 'Is Job running:%s' %(job_instance.is_running())
        print 'Is Job enabled:%s' %(job_instance.is_enabled())

def disable_job():
    server=get_server_instance()
    job_name='flashraid'
    if (server.has_job(job_name)):
        job_instance=server.get_job(job_name)
        job_instance.disable()
        print 'Name:%s,Is Job Enabled ?:%s' %(job_name,job_instance.is_enabled())

def enable_job():
    server=get_server_instance()
    job_name='flashraid'
    if (server.has_job(job_name)):
        job_instance=server.get_job(job_name)
        job_instance.enable()
        print 'Name:%s,Is Job Enabled ?:%s' %(job_name,job_instance.is_enabled())

def get_plugin_details():
    server=get_server_instance()
    for plugin in server.get_plugins().values():
        print "Short Name:%s" %(plugin.shortName)
        print "Long Name:%s" %(plugin.longName)
        print "Version:%s" %(plugin.version)
        print "URL:%s" %(plugin.url)
        print "Active:%s" %(plugin.active)
        print "Enabled:%s" %(plugin.enabled)
def getSCMInfroFromLatestGoodBuild():
    server=get_server_instance()
    job=server['menghe_test']
    print job
    lgb=job.get_last_good_build()
    return lgb.get_revision()

def get_build_console():
    #创建一个build，并返回build结果
    server=get_server_instance()
    #获取下一个build_num
    job=server['menghe_test']
    num=job.get_next_build_number()
    #调用menghe_test中的一个build,传入两个参数
    server.build_job('menghe_test',{'location':'git@114.215.154.24:~/menghe.git','branch_name':'a_branch'})
    time.sleep(10)
    #获取build，并等待build结束
    a_build=job.get_build(num)
    a_build.block()
    #返回build执行的console结果
    return a_build.get_console()



if __name__=='__main__':
    #print get_server_instance().version
    #get_job_details()
    #disable_job()
    #enable_job()
    #get_job_details()
    #get_plugin_details()
    #print getSCMInfroFromLatestGoodBuild()
    print get_build_console()
