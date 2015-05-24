redis = require 'redis'
moment = require 'moment'
{conf} = require './conf'
uid = require './uidGenerator'

Redis = redis.createClient conf.get('redis:port'), conf.get('redis:host')

module.exports = class Shortener

  constructor: (@url, callback) ->
    if @url?
      @uid = uid.generate(7)
      Redis.set @uid, @url, (err, resp) =>
        if err?
          callback err
        else
          # set expiration two weeks from now
          expiration = Math.floor(new Date() / 1000) + 1209600
          Redis.expireat @uid, expiration
          callback null, @uid
