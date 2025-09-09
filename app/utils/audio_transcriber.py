from faster_whisper import WhisperModel


class AudioTranscriber:
    @staticmethod
    def transcribe_audio(file_path, model_size="small", device="cpu", compute_type="float32"):
        # Initialize the Whisper model
        model = WhisperModel(model_size, device=device, compute_type=compute_type)

        # Transcribe the audio file
        segments, info = model.transcribe(file_path)
        return segments, info
