import configparser
import time

from cast_audio_generator import CastAudioGenerator

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config.get('elevenlabs', 'ApiKey')

caster = CastAudioGenerator(api_key=API_KEY)

caster.start()

caster.cast("Cast whole sentences in each text item!")
caster.cast("If you split up the text")
caster.cast("into multiple items it will sound weird")

time.sleep(10)  # wait for audio to finish playing

# Ending the current process will instantly kill background jobs e.g. audio playing
