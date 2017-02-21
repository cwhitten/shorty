---

####Technologies used:

- [Lua cosocket api](https://github.com/openresty/lua-nginx-module)
- [Redis](http://redis.io/)
- [Node.js](https://nodejs.org/)
- [Fabric](http://www.fabfile.org/)
- [CoffeeScript](http://coffeescript.org/)
- [Grunt](http://gruntjs.com/)
- [Vagrant](https://www.vagrantup.com/)

![](http://i.imgur.com/1XG2zIm.jpg)

(Note: architecture above is what the service would look like if not deployed on a free, single t2 micro ec2 instance)

---

### Development

- `$ git clone https://github.com/cwhitten/shorty.git`
- `$ fab vagrant build config` (requires vmware_fusion and Vagrant license) from the root directory
- `$ echo "192.168.1.101  local.shorty.com" >> /etc/hosts`
- `$ vagrant ssh`
- `$ cd /var/www/shorty && coffee web/server.coffee`

Visit `local.shorty.com` in your browser to check for a successfully built environment.

### Deployment

(assumes your ssh-agent has the private ec2 key)


If building from a fresh machine:

- `$ fab aws build config deploy restart`

else:

- `$ fab aws deploy restart`

### Tests

- `$ vagrant ssh`
- `$ cd /var/www/shorty && npm test`
