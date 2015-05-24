Hapi = require 'hapi'
Shortener = require './lib/shortener'

server = new Hapi.Server()
server.connection port: Number process.env.PORT or 5000

server.start ->
  console.log "Web running at: #{server.info.uri}"

server.views
  engines: {html: require('handlebars')},
  path: __dirname + '/templates'

server.route
  method: 'GET'
  path: '/'
  handler: (request, reply) ->
    reply.view 'index.html'

server.route
  method: 'POST'
  path: '/'
  handler: (request, reply) ->

    new Shortener request.payload.url, (err, uid) ->
      if err
        reply {err}
      else
        # todo: get uid to the template
        reply.view 'shorten.html'
