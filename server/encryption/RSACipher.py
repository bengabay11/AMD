import pickle
from Cryptodome.PublicKey import RSA


class RSACipher:
    def __init__(self):
        self.private_key = RSA.generate(1024)
        self.public_key = ""

    def get_public_key(self):
        self.public_key = self.private_key.publickey()

    def encrypt(self, message, public_key):
        pack_data = self.pack(message)
        return public_key.encrypt(pack_data, 32)[0]

    def decrypt(self, encrypted_message):
        decrypt_data = self.private_key.decrypt(encrypted_message)
        return self.unpack(decrypt_data)

    @staticmethod
    def pack(data):
        return pickle.dumps(data).encode('base64')

    @staticmethod
    def unpack(data):
        return pickle.loads(data.decode('base64'))
