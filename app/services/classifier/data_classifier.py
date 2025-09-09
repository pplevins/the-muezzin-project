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

    def _calculate_term_frequency(self, text):
        danger_score = 0
        words_in_text = text.split(" ")
        for word in self._non_hostile_words:
            danger_score += (text.lower().count(word) / len(words_in_text))
        for word in self._hostile_words:
            danger_score += (text.lower().count(word) / len(words_in_text)) * 2
        return danger_score


print(DataClassifier()._calculate_term_frequency(
    " The displacement today is not new, it echoes the Nakba, families torn from their homes generation after generation. Exactly. Refugees in camps across the region still carry the keys to houses they can't return to. And each new massacre adds to that history of exile. That's why protests matter. They link past and present, showing the occupation isn't temporary, it's systemic, and movements like BDS remind the world that apartheid has no place in the modern era. Liberation means return, justice, and an end to endless displacement."))
