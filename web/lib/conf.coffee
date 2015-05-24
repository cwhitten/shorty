nconf = require 'nconf'

exports.conf = nconf
  .argv()
  .file('environment', file: "config/environment.json")
