from app.utils import WordsDecryptor


class DataClassifier:
    def __init__(self):
        self._hostile_words = (WordsDecryptor
                               .decrypt_str_base64(
            "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT")
                               .lower()
                               .split(","))
        self._non_hostile_words = (WordsDecryptor
                                   .decrypt_str_base64(
            "RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ==")
                                   .lower().split(","))
