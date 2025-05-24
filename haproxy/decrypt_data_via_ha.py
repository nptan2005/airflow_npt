from Crypto.Cipher import AES
import base64

# Cấu hình AES (key và IV)
AES_KEY = b"your_16_24_32_byte_key"
AES_IV = b"your_16_byte_iv"


def encrypt_aes(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    padded_data = data + (16 - len(data) % 16) * "\0"
    encrypted = cipher.encrypt(padded_data.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt_aes(encrypted_data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_data))
    return decrypted.decode("utf-8").rstrip("\0")
