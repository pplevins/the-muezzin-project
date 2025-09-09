from faster_whisper import WhisperModel


class AudioTranscriber:
    def __init__(self, model_size="small", device="cpu", compute_type="float32"):
        self._model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe_audio(self, file_path):
        segments, info = self._model.transcribe(file_path)
        return segments, info
