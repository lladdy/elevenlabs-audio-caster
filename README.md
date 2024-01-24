# ElevenLabs - Python - Audio Caster
This repo demonstrates use of the ElevenLabs api for streaming AI generated audio in threads.

## Installation
Install the requirements with:
```
pip install -r requirements.txt
```

For streaming the audio, you need to install https://mpv.io/installation/

For Linux Debian, it should be as simple as:
```
sudo apt update && sudo apt install mpv
```

## Usage
```
# create our caster instance - background processes are implicitly started here
caster = AudioCaster(api_key=ELEVEN_LABS_API_KEY)

# cast some text
# these calls won't block, and will be both generated and played in the background asynchronously
caster.cast("I'm a little teapot, short and stout.")
caster.cast("Here is my handle, here is my spout.")

# Optional: call stop() to block while we wait for the audio to finish playing
# Alternatively, ending the current process will instantly cleanup background jobs e.g. audio playing
caster.stop()
```
