#!/usr/bin/env python3

from encrypted import enc, theory_freq
from cipher import index_of_coincidence


def find_blocks(text: str, block: int) -> list:
  blocks = [''] * block
  for i, c in enumerate(text):
    blocks[i % block] += c
  return blocks


def block_index_of_coincidence(text: str, alphabet: str|dict, block: int) -> float:
  iocs = []
  blocks = find_blocks(text, block)
  for block in blocks:
    iocs.append(index_of_coincidence(block, alphabet))
  return sum(iocs)/len(iocs)


def find_key_len(theory_index: float=0.0553) -> int:
  res_i = None
  for i in range(1, 30):
    ioc = block_index_of_coincidence(enc, theory_freq, i)
    print(f'[*] Index of coincidence {ioc} of key length {i}')
    if abs(theory_index - ioc) < 0.01:
      res_i = i
      break
  if res_i is not None:
    return res_i
  raise Exception('Key length is not found')


def find_letter_key(block: str, alph: str) -> str:
  freq = {}
  for i in block:
    if i not in freq:
      freq[i] = block.count(i)/len(block)
  freq = sorted(freq.items(), key=lambda item: item[1])[-1][0]
  letter = alph[(alph.index(freq) - alph.index('о'))%len(alph)]
  return letter


def find_key(enc: str, alph: str) -> list:
  key_len = find_key_len()
  print(f'[*] Guessed key len: {key_len}')
  blocks = find_blocks(enc, key_len)
  keys = []
  for _, block in enumerate(blocks):
    keys.append(find_letter_key(block, alph))
  return keys


def dec(enc: str, alph: str='абвгдежзийклмнопрстуфхцчшщъыьэюя') -> tuple:
  key = find_key(enc, alph)
  # shinanigans
  key[4] = 'а'
  key[5] = 'я'
  key[-2] = 'к'
  key[1] = 'к'
  key = ''.join(key)
  cleartext = ''
  for i, c in enumerate(enc):
    cleartext += alph[ord(c) - ord(key[i%len(key)])]

  return (cleartext, key)


def main():

  text = dec(enc)
  print(f'[*] Ciphered text: {enc}')
  print(f'[*] Found key: {text[1]}')
  print(f'[*] Deciphered text: {text[0]}')


if __name__ == '__main__':
  main()
