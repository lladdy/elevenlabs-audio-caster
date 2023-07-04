import continuous_threading
from elevenlabs import generate, stream

# Change threading._shutdown() to automatically call Thread.allow_shutdown()
continuous_threading.set_allow_shutdown(True)
continuous_threading.set_shutdown_timeout(0)  # Default 1


class AudioPlayerThread(continuous_threading.ContinuousThread):
    def __init__(self, audio_streams_to_cast):
        super().__init__(args=(audio_streams_to_cast,))
        
    def _run(self, audio_streams_to_cast):
        for audio_stream in audio_streams_to_cast:
            stream(audio_stream)


class CastAudioGenerator(object):

    def __init__(self, api_key: str = None):
        self._api_key = api_key

        # todo: add more elevenlabs params - voice etc.

        self._audio_streams_to_cast = []

    def cast(self, text: str):
        self._text_to_audio_stream(text)

    def _text_to_audio_stream(self, text: str):
        self._audio_streams_to_cast.append(generate(
            text=text,
            stream=True,
            api_key=self._api_key
        ))

    def start(self):
        """Starts another thread which will continuously play the audio streams"""
        self._audio_player_thread = AudioPlayerThread(self._audio_streams_to_cast)
        self._audio_player_thread.start()

    def stop(self):
        """Immediately shuts down any running threads"""
        continuous_threading.shutdown(0)