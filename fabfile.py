import json
import os.path

from fabric.api import *
from fabric.contrib.files import append, exists
from fabric.colors import cyan
from wardrobe import *

env.repo_name = 'shorty'
env.app_name = 'shorty'
env.vhost_dir = '/var/www'
env.app_dir = '{0}/{1}'.format(env.vhost_dir, env.app_name)
env.config_dir = './config'
env.template_dir = '{0}/templates/'.format(env.config_dir)

NODE_VER = '0.10.28'
OPENRESTY_VER = '1.5.8.1'
SERVERS = json.load(open('{0}/environment.json'.format(env.config_dir), 'r'))

@task
def vagrant(provider='vmware_fusion'):
  Utilities.print_header('Development Mode')
  local('vagrant up --provider=%s' % provider)
  Vagrant.connect()

@task
def aws():
  Utilities.print_header('AWS Mode')
  env.hosts = SERVERS['aws']['hosts']
  env.user = 'ubuntu'
  env.environment = 'production'
  env.disable_known_hosts = True
  env.forward_agent = True

@task
def build():
  print(cyan('================'))
  print(cyan('* Building'))
  print(cyan('================'))
  System.install()
  Git.install()
  Node.install(NODE_VER)
  Node.npm('grunt-cli', 'bower', 'coffee-script', 'forever')
  Redis.install()
  sudo('mkdir /var/log/nginx')
  Openresty.install(
    options= {
      'version': OPENRESTY_VER, 
      'flags': '--without-lua_resty_memcached --without-lua_resty_mysql --without-http_rds_csv_module --without-lua_resty_upload'
    }
  )

@task
def config(path=env.app_dir):
  print(cyan('================'))
  print(cyan('* Configuring'))
  print(cyan('================'))
  if env.environment == 'production':
    path = '/var/www/shorty/current'
  else:
    path = '/var/www/short'
  with cd(path):
   run('npm install')
  config_redis()
  config_openresty()

@task
@runs_once
def deploy(branch='master'):
  execute(export, branch)
  execute(switch)

@task
def export(branch):
  deployer(branch).run(config)

@task
def switch():
  deployer().choose_current(1)

@task
def rollback(index=None):
  deployer().choose_current(index)
  restart()

def config_redis():
  Redis.config()
  put('config/templates/redis/redis.conf', '/etc/redis/redis_shorty.conf', True)
  Template.jinja('redis/redis.init', '/etc/init/redis-shorty.conf')
  sudo('service redis-shorty restart')

def config_openresty():
  put('config/templates/nginx/shorty.init', '/etc/init/shorty.conf', True)
  put('redirector/base.conf', '/usr/local/openresty/nginx/conf/nginx.conf', True)
  put('redirector/server.conf', '/usr/local/openresty/nginx/conf/shorty.conf', True)
  sudo('service shorty restart')

@task
def restart(argv=''):
  config()
  run('mkdir -p %s/logs' % env.app_dir)
  forever_list = run('forever list', warn_only=True, quiet=True)
  if not 'No forever processes running' in forever_list:
    run('forever stopall')
  with cd('%s/current' % env.app_dir):
    node_env = 'NODE_ENV=%s' % env.environment
    logs = '%s/logs/forever.log' % env.app_dir
    start = 'coffee web/server.coffee'
    run('%s forever --uid sho -l %s -a start -c %s %s' % (node_env, logs, start, argv))

def deployer(branch='master'):
  if not 'deployer' in env:
    env.deployer = Deploy(env.repo_name, branch, env.environment, env.app_dir)
  return env.deployer
