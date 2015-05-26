{conf} = require '../web/lib/conf'
redis = require 'redis'
moment = require 'moment'
uid = require '../web/lib/uidGenerator'

chai = require 'chai'
sinon = require 'sinon'
expect = chai.expect
should = chai.should()

Shortener = require '../web/lib/shortener'

Redis = redis.createClient conf.get('redis:port'), conf.get('redis:host')

describe 'Shortener', ->
  it 'creates a new uid', (done) ->
    new Shortener 'http://google.com', (err, resp) ->
      expect(resp).to.exist
      done()

  it 'retrieves a url given a uid', (done) ->
    new Shortener 'http://google.com', (err, resp) ->
      Redis.get resp, (err, resp) ->
        expect(resp).to.exist
        expect(resp).to.equal 'http://google.com'
        done()
