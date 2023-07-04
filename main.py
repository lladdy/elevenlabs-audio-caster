import configparser
import time

from cast_audio_generator import AudioCaster

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config.get('elevenlabs', 'ApiKey')

caster = AudioCaster(api_key=API_KEY)

caster.cast("Cast whole sentences in each text item!")
caster.cast("If you split up the text")
caster.cast("into multiple items it will sound weird")

# Ending the current process will instantly kill background jobs e.g. audio playing
time.sleep(10)  # wait for audio to finish playing
