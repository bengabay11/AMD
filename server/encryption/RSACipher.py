import pickle
from Cryptodome.PublicKey import RSA


class RSACipher:
    """Asymmetric  Encryption class uses AES cipher."""
    def __init__(self):
        """The function create random and private key to the RSACipher object."""
        self.private_key = RSA.generate(1024)
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
