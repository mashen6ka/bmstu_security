import json
import os

ENCODE = 0
DECODE = 1

DATA_FOLDER = '../data/'

class DES:
  def __init__(self):
    file = open('settings.json', 'r')
    settings = json.load(file)
    self.key = settings["key"]
    self.initialPermutation = settings["initialPermutation"]
    self.expansion = settings["expansion"]
    self.sboxes = settings["sboxes"]
    self.eachRoundPermutation = settings["eachRoundPermutation"]
    self.finalPermutation = settings["finalPermutation"]
    
    file.close()
  
  # PKCS5 standard
  def __addPadding(self, data):
    paddingLength = 8 - (len(data) % 8)
    if (paddingLength == 0):
      paddingLength = 8
    data += [paddingLength] * paddingLength
    return data
  
  def __removePadding(self, data):
    paddingLength = data[-1]
    return data[:-paddingLength]
    
  def __nSplit(self, list, n):
    return [ list[i : i + n] for i in range(0, len(list), n)]

  def __xor(self, list1, list2):
    return [element1 ^ element2 for element1, element2 in zip(list1,list2)]

  def __binValue(self, val, bitSize):
    binVal = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]

    while len(binVal) < bitSize:
      binVal = "0" + binVal
    return binVal
  
  def __stringToBitArray(self, text):
    bitArray = []
    for letter in text:
      binVal = self.__binValue(letter, 8)
      binValArr = [int(x) for x in list(binVal)]
      bitArray += binValArr
    return bitArray
  
  def __byteArrayToBitArray(self, array):
    bitArray = []
    for byte in array:
      bitStr = str.zfill(bin(byte)[2:], 8)
      for bit in bitStr:
        bitArray.append(int(bit))
    return bitArray
    
  def __bitArrayToByteArray(self, array):
    byteChunks = self.__nSplit(array, 8)
    bytesList = []
    for byte in byteChunks:
      bitsList = []
      for bit in byte:
        bitsList += str(bit)
      bytesList.append(int(''.join(bitsList), 2))
    return bytesList
  
  def __expand(self, array, table):
    return [array[element - 1] for element in table]

  def __leftShift(self, list1, list2, n):
    return list1[n:] + list1[:n], list2[n:] + list2[:n]
  
  def __permute(self, array, table):
    return [array[element - 1] for element in table]
  
  def __generateKeys(self):
    keys = []
    key = self.__stringToBitArray(self.key["value"])
    key = self.__permute(key, self.key["permutation1"])
    leftBlock, rightBlock = self.__nSplit(key, 28)

    for i in range(16):
      leftBlock, rightBlock = self.__leftShift(leftBlock, rightBlock, self.key["shift"][i])
      temp = leftBlock + rightBlock
      keys.append(self.__permute(temp, self.key["permutation2"]))
    return keys
  
  def __sboxSubstitute(self, bitArray):
    blocks = self.__nSplit(bitArray, 6)
    result = []

    for i in range(len(blocks)):
        block = blocks[i]

        row = int( str(block[0]) + str(block[5]), 2 )
        column = int(''.join([str(x) for x in block[1:-1]]), 2)

        sboxValue = self.sboxes[i][row][column]
        binVal = self.__binValue(sboxValue, 4)
        result += [int(bit) for bit in binVal]
    return result
  
  def __DES(self, text, mode):
    keys = self.__generateKeys()
    
    text8byteBlocks = self.__nSplit(text, 8)
    result = []
    
    for block in text8byteBlocks:
      block = self.__byteArrayToBitArray(block)
      block = self.__permute(block, self.initialPermutation)
      leftBlock, rightBlock = self.__nSplit(block, 32)
      
      temp = None
      for i in range(16):
        expandedRightBlock = self.__expand(rightBlock, self.expansion)

        if mode == ENCODE:
          temp = self.__xor(keys[i], expandedRightBlock)
        elif mode == DECODE:
          temp = self.__xor(keys[15 - i], expandedRightBlock)
        
        temp = self.__sboxSubstitute(temp)
        temp = self.__permute(temp, self.eachRoundPermutation)
        temp = self.__xor(leftBlock, temp)
        
        leftBlock = rightBlock
        rightBlock = temp
        
      result += self.__permute(rightBlock + leftBlock, self.finalPermutation)
  
    finalResult = self.__bitArrayToByteArray(result)
    return finalResult

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
    byteArray = self.__addPadding(byteArray)
    encodedByteArray = self.__DES(byteArray, ENCODE)
    
    self.__writeByteArray(outputPath, encodedByteArray)
    
  
  def decode(self, inputPath):
    filePath, fileName = os.path.split(inputPath)
    outputPath = os.path.join(filePath, 'decoded__' + fileName[9:])

    byteArray = self.__readByteArray(inputPath)
    decodedByteArray = self.__DES(byteArray, DECODE)
    decodedByteArray = self.__removePadding(decodedByteArray)
    
    self.__writeByteArray(outputPath, decodedByteArray)


des = DES()
des.encode(DATA_FOLDER + 'data.txt')
des.encode(DATA_FOLDER + 'data.png')
des.encode(DATA_FOLDER + 'data.pdf')
des.encode(DATA_FOLDER + 'data.zip')

des.decode(DATA_FOLDER + 'encoded__data.txt')
des.decode(DATA_FOLDER + 'encoded__data.png')
des.decode(DATA_FOLDER + 'encoded__data.pdf')
des.decode(DATA_FOLDER + 'encoded__data.zip')