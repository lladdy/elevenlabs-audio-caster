import configparser

from cast_audio_generator import AudioCaster

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config.get('elevenlabs', 'ApiKey')

caster = AudioCaster(api_key=API_KEY)

# Start the caster background process
caster.start()

caster.cast("Be sure to send whole sentences in each text item!")
caster.cast("If you split up the text")
caster.cast("into multiple items it will sound weird")

# Optional: call stop() to wait for the audio to finish playing
# Alternatively, ending the current process will instantly cleanup background jobs e.g. audio playing
caster.stop()