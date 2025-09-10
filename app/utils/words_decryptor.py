import base64


class WordsDecryptor:
    """A decryptor utility class to decrypt dangerous words saved as a encrypted string."""

    @staticmethod
    def decrypt_str_base64(encrypted_str):
        """A base64 decryption function."""
        return base64.b64decode(encrypted_str).decode('utf-8')
