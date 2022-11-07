from array import array
import json

class Rotor:
  def __init__(self, key: array, start: array):
    self.key: array = key
    self.start: int = key.index(start)
    self.curr: int = self.start
    
  def rotate(self):
    self.curr = (self.curr + 1) % len(self.key)
    
  def getCharByIndex(self, index: int):
    return self.key[(self.curr + index) % len(self.key)]
  
  def getIndexByChar(self, char: array):
    return (- self.curr + self.key.index(char)) % len(self.key)
    
class Reflector:
  def __init__(self, key: array):
    self.key: array = key

class Enigma:
  def __init__(self):
    file = open('settings.json', 'r')
    settings = json.load(file)
    file.close()
    self.rotor1: Rotor = Rotor(settings['rotor1']['key'], settings['rotor1']['start'])
    self.rotor2: Rotor = Rotor(settings['rotor1']['key'], settings['rotor1']['start'])
    self.rotor3: Rotor = Rotor(settings['rotor1']['key'], settings['rotor1']['start'])
    
    self.reflector: Reflector = Reflector(settings['reflector']['key'])

  def encode(self, inputPath):
    inputFile = open(inputPath, 'rb')
    if inputPath.startswith('encoded__'): outputPath = 'decoded__' + inputPath[9:]
    else: outputPath = 'encoded__' + inputPath
    outputFile = open(outputPath, 'wb')
    while 1:
      byte = inputFile.read(1)
      if byte == b"":
        break
      char: int = int.from_bytes(byte, byteorder="big", signed=False)
      charEncoded = self.__encodeChar(char)
      # print(char, '->', charEncoded)
      outputFile.write(charEncoded.to_bytes(1, byteorder='big', signed=False))

    inputFile.close()
    outputFile.close()
  
  def __encodeChar(self, char):
    #  прямой ход
    char = self.rotor1.getCharByIndex(char)
    char = self.rotor2.getCharByIndex(char)
    char = self.rotor3.getCharByIndex(char)
    
    char = self.reflector.key[char]
    
    # обратный ход
    char = self.rotor3.getIndexByChar(char)
    char = self.rotor2.getIndexByChar(char)
    char = self.rotor1.getIndexByChar(char)

    # проворачиваем роторы
    self.rotor3.rotate()
    if (self.rotor3.curr == self.rotor3.start):
      self.rotor2.rotate()
      if (self.rotor2.curr == self.rotor2.start):
        self.rotor1.rotate()

    return char
  
enigma = Enigma()
enigma.encode('data.txt')
enigma.encode('data.png')
enigma.encode('data.pdf')
enigma.encode('data.zip')

enigma = Enigma()
enigma.encode('encoded__data.txt')
enigma.encode('encoded__data.png')
enigma.encode('encoded__data.pdf')
enigma.encode('encoded__data.zip')