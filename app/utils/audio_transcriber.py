from faster_whisper import WhisperModel


class AudioTranscriber:
    """The audio transcriber utility class."""

    def __init__(self, model_size="small", device="cpu", compute_type="float32"):
        """Initialize the audio transcriber model."""
        self._model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe_audio(self, file_path):
        """
        Transcribe audio from given file path

        :return: tuple of with result of transcription as segments generator, and info object with useful information about the audio.
        """
        segments, info = self._model.transcribe(file_path)
        return segments, info
