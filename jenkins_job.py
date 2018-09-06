#!/usr/bin/python3
# Author zhaohaihua
# required pip install jenkinsapi

from django.shortcuts import render_to_response
from django.shortcuts import render,redirect
from jenkinsapi.jenkins import Jenkins
import os,sys,platform

if platform.system() == 'Windows':
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(BASE_DIR)

class JenkinsJob(object):
    def __init__(self):
        self.jenkins_server_url = 'http://k8s.jci.beisencorp.com/'
        self.user_id = 'admin'
        self.api_token = '24c74daa99963167395b57eb9d93cd15'
        self.server = Jenkins(self.jenkins_server_url, username=self.user_id, password=self.api_token)

    #create build images job
    def buildJob(self,job_name,app_name,git_url):
        JobName = job_name
        AppName = app_name
        GitURL = git_url
        with open(BASE_DIR + '/templates/build_config.xml') as files:
            config_xml_tempate = files.read()
        config_xml = config_xml_tempate.replace('GitURL',GitURL).replace('AppName',AppName)
        self.server.create_job(JobName,config_xml)

    #create deploy job
    def deployJob(self,job_name,app_name):
        JobName = job_name
        AppName = app_name
        with open(BASE_DIR + '/templates/deploy_config.xml') as files:
            config_xml_tempate = files.read()
        config_xml = config_xml_tempate.replace('AppName',AppName)
        self.server.create_job(JobName,config_xml)

def createjob(req):
        if req.method == "GET":
            return render_to_response(BASE_DIR + '/templates/microsvc_cjob.html')
        elif req.method == "POST":
            job = JenkinsJob()
            image_job_name = req.POST.get("image_jobname",None)
            deploy_job_name = req.POST.get("deploy_jobname",None)
            appname = req.POST.get("appname",None)
            giturl = req.POST.get("giturl",None)
            try:
                job.buildJob(job_name=image_job_name, app_name=appname, git_url=giturl)
                job.deployJob(job_name=deploy_job_name, app_name=appname)
            except:
                print('Create jenkins job faild!!!')
            redirect("http://k8s.jenkins.beisencorp.com")


if __name__ == '__main__':
    jobname = 'Test_Image_Build'
    giturl = 'http://gitlab.beisencorp.com/DevOps/BeiSen.NetCore.DistributedTransactionControl.git'
    appname = 'Beisen.DTC.WebApi'
    job = JenkinsJob()
    job.buildJob(job_name=jobname,app_name=appname,git_url=giturl)