redis = require 'redis'
moment = require 'moment'
{conf} = require './conf'
uid = require './uidGenerator'

Redis = redis.createClient conf.get('redis:port'), conf.get('redis:host')

module.exports = class Shortener

  constructor: (@url, callback) ->
    uid = uid.generate(7)
    Redis.set uid, @url, (err, resp) ->
      if err?
        callback err
      else
        callback null, uid
