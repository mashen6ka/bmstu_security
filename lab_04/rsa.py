import json
from random import choice, randrange
import os

ENCODE = 0
DECODE = 1

DATA_FOLDER = '../data/'

class RSA:
  def __init__(self, generate = True):
    file = open('settings.json', 'r')
    settings = json.load(file)

    if (generate):
      keyLengthTmp = int(settings["keyLength"])
      self.__keyLength = self.__adjustKeyLength(keyLengthTmp)
      self.__generateKeys()
    else:
      self.__keyLength = int(settings["default"]["keyLength"])
      self.__n = int(settings["default"]["n"])
      self.__d = int(settings["default"]["d"])
      self.__e = int(settings["default"]["e"])
    file.close()
  
  def __adjustKeyLength(self, keyLength):
    r = keyLength % 8
    if (r >= 4): return keyLength + (8 - r)
    elif (r < 4): return keyLength - r
    
  def __gcd(self, num1, num2):
    if num2 == 0: return num1
    else: return self.__gcd(num2, num1 % num2)
  
  def __gcdExtended(self, num1, num2, u1 = 1, v1 = 0,
                                      u2 = 0, v2 = 1):
    if (num2 == 0): return abs(num1), 1, 0
   
    q = num1 // num2
    r = num1 % num2
    
    u1_, v1_ = u2, v2
    u2_, v2_ = u1 - q * u2, v1 - q * v2 
    return (abs(num2), u2, v2) if (r == 0) else self.__gcdExtended(num2, r, u1_, v1_, u2_, v2_)
  
  def __primeEratosthenes(self, bottom, top):
    nonPrimeList = []
    primeList = []
    for i in range(2, top + 1):
      if i not in nonPrimeList:
        primeList.append(i)
        for j in range(i*i, top + 1, i):
          nonPrimeList.append(j)
    return [num for num in primeList if num >= bottom]

  def __coprimeEuclid(self, phi):
    e = randrange(1, phi)
    while self.__gcd(e, phi) != 1:
      e = randrange(1, phi)
    return e
  
  def __modInverseExtendedEuclid(self, e, phi):
    _, _, v = self.__gcdExtended(phi, e)
    return v % phi

  def __generateKeys(self):
    length = int(self.__keyLength / 2)
    top = 2**(length) - 1
    bottom = 2**(length - 1) + 1

    primeList = self.__primeEratosthenes(bottom, top)
    p = choice(primeList)
    primeList.remove(p)
    q = choice(primeList)
    
    self.__n = p * q
    
    phi = (p - 1) * (q - 1)

    self.__e = self.__coprimeEuclid(phi)
    self.__d = self.__modInverseExtendedEuclid(self.__e, phi)
        
  def __RSA(self, array, mode):    
    if (mode == ENCODE): result = [pow(byte, self.__e, self.__n) for byte in array]
    elif (mode == DECODE): result = [pow(byte, self.__d, self.__n) for byte in array]
    
    return result
  
  def __numArrayToByteArray(self, numArray, bytesInNum):
    byteArray = []
    for num in numArray:
      for i in range(bytesInNum):
        byteArray.append(num % 256)
        num //= 256
    return byteArray
        
  def __byteArrayToNumArray(self, byteArray, bytesInNum):
    numArray = []
    for i in range(0, len(byteArray) - bytesInNum + 1, bytesInNum):
      num = 0
      for j in range(bytesInNum - 1, -1, -1):
        num = num * 256 + byteArray[i + j]
      numArray.append(num) 
    return numArray    
      
  def __writeByteArray(self, filePath, array):
    file = open(filePath, 'wb')
    for byte in array:
      file.write(byte.to_bytes(1, byteorder='big', signed=False))
    file.close()
    
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
  
  def encode(self, inputPath):
    filePath, fileName = os.path.split(inputPath)
    outputPath = os.path.join(filePath, 'encoded__' + fileName)
    
    byteArray = self.__readByteArray(inputPath)
    encodedNumArray = self.__RSA(byteArray, ENCODE)
    encodedByteArray = self.__numArrayToByteArray(encodedNumArray, int(self.__keyLength / 8))
    self.__writeByteArray(outputPath, encodedByteArray)
    
  def decode(self, inputPath):
    filePath, fileName = os.path.split(inputPath)
    outputPath = os.path.join(filePath, 'decoded__' + fileName[9:])

    byteArray = self.__readByteArray(inputPath)
    numArray = self.__byteArrayToNumArray(byteArray, int(self.__keyLength / 8))
    decodedByteArray = self.__RSA(numArray, DECODE)
    
    self.__writeByteArray(outputPath, decodedByteArray)
  
  def privateKey(self):
    return (self.__d, self.__n)
  
  def publicKey(self):
    return (self.__e, self.__n)


rsa = RSA()
rsa.encode(DATA_FOLDER + 'data.txt')
rsa.encode(DATA_FOLDER + 'data.png')
rsa.encode(DATA_FOLDER + 'data.pdf')
rsa.encode(DATA_FOLDER + 'data.zip')

rsa.decode(DATA_FOLDER + 'encoded__data.txt')
rsa.decode(DATA_FOLDER + 'encoded__data.png')
rsa.decode(DATA_FOLDER + 'encoded__data.pdf')
rsa.decode(DATA_FOLDER + 'encoded__data.zip')
