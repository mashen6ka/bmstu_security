from array import array
import json
import os

DATA_FOLDER = '../data/'

class Rotor:
  def __init__(self, key: array, start: array):
    self.key: array = key
    self.start: int = key.index(start)
    self.curr: int = self.start
    
  def rotate(self):
    self.curr = (self.curr + 1) % len(self.key)
    
  def getByteByIndex(self, index: int):
    return self.key[(self.curr + index) % len(self.key)]
  
  def getIndexByByte(self, byte: array):
    return (- self.curr + self.key.index(byte)) % len(self.key)
    
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

  def __readByteArray(self, filePath):
    file = open(filePath, 'rb')
    byteArray = []
    while 1:
      byte = file.read(1)
      if byte == b"":
        break
      byteArray.append(int.from_bytes(byte, byteorder="big", signed=False))
    file.close()
    return byteArray
    
  def __writeByteArray(self, filePath, array):
    file = open(filePath, 'wb')
    for byte in array:
      file.write(byte.to_bytes(1, byteorder='big', signed=False))
    file.close()

  def encode(self, inputPath):
    filePath, fileName = os.path.split(inputPath)
    outputPath = os.path.join(filePath, 'encoded__' + fileName)
    
    byteArray = self.__readByteArray(inputPath)
    encodedByteArray = self.__Enigma(byteArray)
    self.__writeByteArray(outputPath, encodedByteArray)
  
  def decode(self, inputPath):
    filePath, fileName = os.path.split(inputPath)
    outputPath = os.path.join(filePath, 'decoded__' + fileName[9:])
    
    byteArray = self.__readByteArray(inputPath)
    decodedByteArray = self.__Enigma(byteArray)
    self.__writeByteArray(outputPath, decodedByteArray)
  
  def __Enigma(self, data):
    result = []
    for byte in data:
      #  прямой ход
      byte = self.rotor1.getByteByIndex(byte)
      byte = self.rotor2.getByteByIndex(byte)
      byte = self.rotor3.getByteByIndex(byte)
      
      byte = self.reflector.key[byte]
      
      # обратный ход
      byte = self.rotor3.getIndexByByte(byte)
      byte = self.rotor2.getIndexByByte(byte)
      byte = self.rotor1.getIndexByByte(byte)

      # проворачиваем роторы
      self.rotor3.rotate()
      if (self.rotor3.curr == self.rotor3.start):
        self.rotor2.rotate()
        if (self.rotor2.curr == self.rotor2.start):
          self.rotor1.rotate()
      
      result.append(byte)

    return result
  
enigma = Enigma()
enigma.encode(DATA_FOLDER + 'data.txt')
enigma.encode(DATA_FOLDER + 'data.png')
enigma.encode(DATA_FOLDER + 'data.pdf')
enigma.encode(DATA_FOLDER + 'data.zip')

enigma = Enigma()
enigma.decode(DATA_FOLDER + 'encoded__data.txt')
enigma.decode(DATA_FOLDER + 'encoded__data.png')
enigma.decode(DATA_FOLDER + 'encoded__data.pdf')
enigma.decode(DATA_FOLDER + 'encoded__data.zip')