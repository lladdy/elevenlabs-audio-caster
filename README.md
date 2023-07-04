# ElevenLabs - Python - Audio Caster
This repo demonstrates use of the ElevenLabs api for streaming generated audio in threads.

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
caster.cast("Some text")

# Optional: call stop() to wait for the audio to finish playing
# Alternatively, ending the current process will instantly cleanup background jobs e.g. audio playing
caster.stop()
```