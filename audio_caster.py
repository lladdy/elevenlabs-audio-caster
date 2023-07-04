import time
from typing import List

import continuous_threading
from elevenlabs import generate, stream

# Change threading._shutdown() to automatically call Thread.allow_shutdown()
continuous_threading.set_allow_shutdown(True)
continuous_threading.set_shutdown_timeout(0)  # Default 1


class AudioPlayerThread(continuous_threading.ContinuousThread):
    """Thread which continuously plays audio streams generated by TextToAudioStreamGenerator objects"""

    def __init__(self, audio_generators):
        super().__init__(args=(audio_generators,))

    def _run(self, audio_generators):
        while audio_generators:
            audio_stream_generator = audio_generators.pop(0)
            stream(audio_stream_generator.get_stream())


class TextToAudioStreamGeneratorFactory(object):
    """Factory for creating TextToAudioStreamGenerator objects"""
    def __init__(self, api_key: str = None):
        self._api_key = api_key

    def get_generator(self, text: str):
        return TextToAudioStreamGenerator(text, api_key=self._api_key)


class TextToAudioStreamGenerator(continuous_threading.Thread):
    """Thread which generates an audio stream from text"""
    def __init__(self, text, api_key=None):
        super().__init__(target=self._text_to_audio_stream, args=(text,))
        self._api_key = api_key

        self._stream = None

    def get_stream(self):
        self.join()  # wait for the thread to complete

        assert self._stream is not None, 'Stream not generated'

        return self._stream

    def _text_to_audio_stream(self, text: str):
        self._stream = generate(
            text=text,
            stream=True,
            api_key=self._api_key
        )


class AudioCaster(object):
    """Casts audio from text using the ElevenLabs API"""

    def __init__(self, api_key: str = None, auto_start: bool = True):
        self.t2asg_factory = TextToAudioStreamGeneratorFactory(api_key=api_key)

        # todo: add more elevenlabs params - voice etc.

        self._audio_generators_to_cast: List[TextToAudioStreamGenerator] = []

        if auto_start:
            self.start()

    def cast(self, text: str):
        """Adds text to the queue to be casted"""
        if not self.is_started:
            raise RuntimeError('Caster not started')

        generator = self.t2asg_factory.get_generator(text)
        generator.start()
        self._audio_generators_to_cast.append(generator)

    def _start_audio_player(self):
        """Starts another thread which will continuously play the audio streams"""
        self._audio_player_thread = AudioPlayerThread(self._audio_generators_to_cast)
        self._audio_player_thread.start()

    def stop(self):
        """Waits for all audio to be casted"""
        self._audio_player_thread.join()
        del self._audio_player_thread

    def start(self):
        # only start once
        if self.is_started:
            raise RuntimeError('Caster already started')
        self._start_audio_player()

    @property
    def is_started(self):
        return hasattr(self, '_audio_player_thread')
