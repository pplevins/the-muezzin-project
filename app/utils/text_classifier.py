import os

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

from .words_decryptor import WordsDecryptor


class TextClassifier:
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

    def _clean_and_remove_stopwords(self, text):
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text.lower())
        return " ".join([word for word in tokens if word not in stop_words])

    def _calculate_term_frequency(self, text):
        danger_score = 0
        words_count = len(text.split(" "))
        for word in self._non_hostile_words:
            danger_score += (text.count(word) / words_count)
        for word in self._hostile_words:
            danger_score += (text.count(word) / words_count) * 2

        return danger_score

    def _is_score_bds(self, score, threshold=0.2):
        return True if score > threshold else False

    def _classify_score_threat_level(self, score, threshold=0.2, high_threshold=0.4):
        return "none" if score < threshold else "high" if score > high_threshold else "medium"

    def classify_text(self, text):
        cleaned_text = self._clean_and_remove_stopwords(text)
        score = self._calculate_term_frequency(cleaned_text)
        return {
            "bds_precent": score,
            "is_bds": self._is_score_bds(score),
            "bds_threat_level": self._classify_score_threat_level(score)
        }
