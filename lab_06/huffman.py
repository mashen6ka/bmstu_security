import heapq
import os

DATA_FOLDER = '../data/'

class Node:
  def __init__(self, byte, freq):
    self.byte = byte
    self.freq = freq
    self.left = None
    self.right = None

  def __lt__(self, other):
    return self.freq < other.freq

  def __eq__(self, other):
    if (other == None):
      return False
    return self.freq == other.freq

class Huffman:
  def __init__(self):
    self.heap = []
    self.codes = {}
    self.frequency = {}
    
  def __reset(self):
    self.heap = []
    self.codes = {}
    self.frequency = {}
    
  def __countFrequency(self, byteArray):
    self.frequency = {}
    for byte in byteArray:
      if not byte in self.frequency:
        self.frequency[byte] = 0
      self.frequency[byte] += 1
    
  def __makeHeap(self):
    self.heap = []
    for key in self.frequency:
      node = Node(key, self.frequency[key])
      heapq.heappush(self.heap, node)

  def __mergeNodes(self):
    while(len(self.heap)>1):
      node1 = heapq.heappop(self.heap)
      node2 = heapq.heappop(self.heap)

      merged = Node(None, node1.freq + node2.freq)
      merged.left = node1
      merged.right = node2

      heapq.heappush(self.heap, merged)

  def __makeCodesHelper(self, root, currentCode):
    if (root == None): return
    if (root.byte != None):
      self.codes[root.byte] = currentCode
      return

    self.__makeCodesHelper(root.left, currentCode + "0")
    self.__makeCodesHelper(root.right, currentCode + "1")
  
  def __makeCodes(self):
    root = self.heap[0]
    currentCode = ""
    self.__makeCodesHelper(root, currentCode)
  
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
    
  def __addPadding(self, bitStr):
    paddingLength = 8 - (len(bitStr) % 8)
    bitStr += '0' * paddingLength
    paddingInfo = "{0:08b}".format(paddingLength)
    return paddingInfo + bitStr
  
  def __removePadding(self, bitStr):
    paddingInfo = bitStr[:8]
    paddingLength = int(paddingInfo, 2)
    return bitStr[8:-paddingLength]
  
  def __encodeByteArray(self, byteArray):
    encodedData = ""
    for byte in byteArray:
      encodedData += self.codes[byte]
    return encodedData
  
  def __decodeBitStr(self, bitStr):
    decodedData = []

    root = self.heap[0]
    currNode = root
    for bit in bitStr:
      if (bit == "0"):
        currNode = currNode.left
      elif (bit == "1"):
        currNode = currNode.right
        
      if (currNode.byte != None):
        decodedData.append(currNode.byte)
        currNode = root
    return decodedData
      
  def __bitStrToByteArray(self, bitStr):
    byteArray = []
    for i in range(0, len(bitStr), 8):
      byte = bitStr[i : i+8]
      byteArray.append(int(byte, 2))
    return byteArray
  
  def __byteArrayToBitStr(self, byteArray):
    bitStr = ""
    for byte in byteArray:
      bitStr += str.zfill(bin(byte)[2:], 8)
    return bitStr
  
  def compress(self, inputPath):
    filePath, fileName = os.path.split(inputPath)
    outputPath = os.path.join(filePath, 'compressed__' + fileName)
    
    byteArray = self.__readByteArray(inputPath)
    
    self.__reset()
    self.__countFrequency(byteArray)
    self.__makeHeap()
    self.__mergeNodes()
    self.__makeCodes()
    compressedBitStr = self.__encodeByteArray(byteArray)
    compressedBitStr = self.__addPadding(compressedBitStr)
    compressedByteArray = self.__bitStrToByteArray(compressedBitStr)
    
    self.__writeByteArray(outputPath, compressedByteArray)
    
  def decompress(self, inputPath):
    filePath, fileName = os.path.split(inputPath)
    outputPath = os.path.join(filePath, 'decompressed__' + fileName[12:])

    byteArray = self.__readByteArray(inputPath)
    
    bitStr = self.__byteArrayToBitStr(byteArray)
    bitStr = self.__removePadding(bitStr)
    decompressedByteArray = self.__decodeBitStr(bitStr)
    
    self.__writeByteArray(outputPath, decompressedByteArray)


huffman = Huffman()
huffman.compress(DATA_FOLDER + 'data.txt')
huffman.decompress(DATA_FOLDER + 'compressed__data.txt')

huffman.compress(DATA_FOLDER + 'data.png')
huffman.decompress(DATA_FOLDER + 'compressed__data.png')

huffman.compress(DATA_FOLDER + 'data.pdf')
huffman.decompress(DATA_FOLDER + 'compressed__data.pdf')

huffman.compress(DATA_FOLDER + 'data.zip')
huffman.decompress(DATA_FOLDER + 'compressed__data.zip')