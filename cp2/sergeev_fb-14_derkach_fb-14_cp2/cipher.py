#!/usr/bin/env python3

from random import choice
from string import ascii_lowercase
from orig import lorem


def index_of_coincidence(text: str, alphabet: str) -> float:
  length = len(text)
  ioc = 0
  for i in alphabet:
    num = text.count(i)
    ioc += num*(num-1) / (length*(length-1))
  return ioc


def vigenere(text: str, key: str) -> str:
  print('-'*50)
  print(f'KEY: {key}')
  enc = []
  for i, char in enumerate(text):
    enc_char = char
    if char in ascii_lowercase:
      enc_char = ascii_lowercase[((ord(char)-ord('a'))+ord(key[i%len(key)])-ord('a')) % len(ascii_lowercase)]
    enc.append(enc_char)
  return ''.join(enc)


## generate random keys
def _gen_keys():
  print('keys=[', end='')
  for i in range(2,7):
    if i != 6:
      print('"'+''.join([choice(ascii_lowercase) for _ in range(i)])+'"', end=',')
      continue
    print('"'+''.join([choice(ascii_lowercase) for _ in range(15)])+'"', end=',')
    print(']')


def main():
#  _gen_keys()
  global lorem
  keys = ["we","lhq","aums","byfvd","eoqshozdnxddxhj",]
  temp = []
  for char in lorem:
    if char.lower() in ascii_lowercase:
      temp.append(char.lower())
  lorem = ''.join(temp)
  for key in keys:
    encrypted = vigenere(lorem, key)
    print(encrypted)
    print(index_of_coincidence(encrypted, ascii_lowercase))
  print('-'*50)
  print('Cleartext (eng)')
  print(index_of_coincidence(lorem, ascii_lowercase))


if __name__ == '__main__':
  main()
