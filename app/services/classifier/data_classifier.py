import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from app.utils import WordsDecryptor


class DataClassifier:
    def __init__(self):
        nltk_dir = "/tmp/nltk_data"
        os.makedirs(nltk_dir, exist_ok=True)
        nltk.data.path.append(nltk_dir)
        nltk.download('stopwords', download_dir=nltk_dir, quiet=True)
        nltk.download('punkt', download_dir=nltk_dir, quiet=True)
        nltk.download('punkt_tab', download_dir=nltk_dir, quiet=True)
        self._hostile_words = (WordsDecryptor
                               .decrypt_str_base64(
            "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT")
                               .lower()
                               .split(","))
        self._hostile_words_count = len(self._hostile_words)
        self._non_hostile_words = (WordsDecryptor
                                   .decrypt_str_base64(
            "RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ==")
                                   .lower().split(","))
        self._non_hostile_words_count = len(self._non_hostile_words)

    def _remove_stopwords(self, text):
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text)
        return " ".join([word for word in tokens if word not in stop_words])

    def _calculate_term_frequency(self, text):
        clean_text = self._remove_stopwords(text.lower())
        danger_score = 0
        words_in_text = clean_text.split(" ")
        words_count = len(words_in_text)
        print(clean_text)
        for word in self._non_hostile_words:
            danger_score += (clean_text.count(word) / words_count)
        for word in self._hostile_words:
            danger_score += (clean_text.count(word) / words_count) * 2

        return danger_score

    def _classify_score(self, score):
        is_bds = True if score > 0.2 else False
        bds_threat_level = "none" if score < 0.2 else "high" if score > 0.4 else "medium"
        return is_bds, bds_threat_level
