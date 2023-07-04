import time

import continuous_threading
from elevenlabs import generate, stream

# Change threading._shutdown() to automatically call Thread.allow_shutdown()
continuous_threading.set_allow_shutdown(True)
continuous_threading.set_shutdown_timeout(0)  # Default 1


class CastAudioGenerator(object):

    def __init__(self, api_key: str = None):
        self._api_key = api_key

        # todo: add more elevenlabs params - voice etc.

        self._audio_streams_to_cast = []

    def _play_streams(self):
        while True:
            for audio_stream in self._audio_streams_to_cast:
                stream(audio_stream)

            time.sleep(0.1)

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
        self._audio_player_thread = continuous_threading.Thread(target=CastAudioGenerator._play_streams, args=(self,))
        self._audio_player_thread.start()  # continuous_threading will auto stop when requested by process shutdown

    def stop(self):
        """Immediately shuts down any running threads"""
        continuous_threading.shutdown(0)