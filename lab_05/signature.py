from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

DATA_FOLDER = '../data/'
PUBLIC_KEY_PATH = './publicKey.pem'
SIGNATURE_PATH = './signature.sig'

class Signature:
  def __init__(self):
    self.publicKeyPath = PUBLIC_KEY_PATH
    self.signaturePath = SIGNATURE_PATH
    pass
  
  def __writePublicKey(self, publicKey):
    file = open(self.publicKeyPath, 'wb')
    file.write(publicKey)
    file.close()
  
  def __readPublicKey(self):
    file = open(self.publicKeyPath, 'rb')
    publicKey = file.read()
    file.close()
    return publicKey
  
  def __writeSignature(self, signature):
    file = open(self.signaturePath, 'wb')
    file.write(signature)
    file.close()
    
  def __readSignature(self):
    file = open(self.signaturePath, 'rb')
    signature = file.read()
    file.close()
    return signature
  
  def __hash(self, data):
    return SHA256.new(data)
  
  def create(self, filePath):
    file = open(filePath, 'rb')
    hash = self.__hash(file.read())
    file.close()
    
    keys = RSA.generate(2048)
    privateKey, publicKey = keys, keys.publickey()
    signature = pkcs1_15.new(privateKey).sign(hash)
    
    self.__writePublicKey(publicKey.exportKey())
    self.__writeSignature(signature)
    
  def verify(self, filePath):
    file = open(filePath, 'rb')
    hash = self.__hash(file.read())
    file.close()
    
    publicKey = RSA.importKey(self.__readPublicKey())
    signature = self.__readSignature()
    
    try:
      pkcs1_15.new(publicKey).verify(hash, signature)
      return True
    except (ValueError, TypeError):
      return False

sign = Signature()
sign.create(DATA_FOLDER + 'data.txt')
result = sign.verify(DATA_FOLDER + 'data.txt')
print(result)


