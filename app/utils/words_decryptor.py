import base64


class WordsDecryptor:
    @staticmethod
    def decrypt_str_base64(encrypted_str):
        return base64.b64decode(encrypted_str).decode('utf-8')
