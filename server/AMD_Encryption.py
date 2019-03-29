import pickle
from Crypto.PublicKey import RSA
from Crypto.Util import randpool
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    """Symmetric Encryption class uses AES cipher."""
    def __init__(self, key):
        self.bs = 16
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        """The function encrypt the data with te AES key."""
        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(message))

    def decrypt(self, enc):
        """The function decrypt the data with te AES key."""
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class RSACipher:
    """Asymmetric  Encryption class uses AES cipher."""
    def __init__(self):
        """The function create random and private key to the RSACipher object."""
        random = randpool.RandomPool()
        self.private_key = RSA.generate(1024, random.get_bytes)
        self.public_key = ""

    def get_public_key(self):
        """The function create RSA public key to the RSACipher object."""
        self.public_key = self.private_key.publickey()

    def encrypt(self, message, public_key):
        """The function gets data and public key, and encrypt it with the public key."""
        pack_data = self.pack(message)
        return public_key.encrypt(pack_data, 32)[0]

    def decrypt(self, encrypted_message):
        """The function gets encrypted data and decrypt it with the private key."""
        decrypt_data = self.private_key.decrypt(encrypted_message)
        return self.unpack(decrypt_data)

    @staticmethod
    def pack(data):
        """The function pad the data with base64 and make it pickle object."""
        return pickle.dumps(data).encode('base64')

    @staticmethod
    def unpack(data):
        """The function unpad the data with base64 and load it to string."""
        return pickle.loads(data.decode('base64'))
