from fabric.api import *

env.hosts = ['bozka@s7.wservices.ch']

def deploy():
   local('git push')
   run('cd ~/herbalist; git pull')
   run('export DJANGO_SETTINGS_MODULE=herbalist.settings_deployment')
   run('./manage.py migrate herbapp')
   run('./manage.py collectstatic')
   run('~/init/herbalist restart')

def restart():
   run('~/init/herbalist restart')

def stop():
   run('~/init/herbalist stop')

def start():
   run('~/init/herbalist start')
