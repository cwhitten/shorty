
numbers = '0123456789'
lowerCase = 'abcdefghijklmnopqrstuvwxyz'
upperCase = lowerCase.toUpperCase()
corpus = numbers + lowerCase + upperCase

exports.generate = (length) ->
  string = ''
  i = 0
  while i < length
    randomNumber = Math.floor(Math.random() * corpus.length)
    string += corpus.substring(randomNumber, randomNumber + 1)
    i++
  string
