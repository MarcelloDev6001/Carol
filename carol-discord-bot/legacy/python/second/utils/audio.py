from pydub import AudioSegment
from gtts import gTTS
import pyaudio
import numpy as np

def combine_audios(audios_list: list[str], audio_filename: str):
    try:
        combine_audio = None
        for aud in audios_list:
            audio1 = AudioSegment.from_file(f"audios/{aud}.mp3")

            if combine_audio == None:
                combine_audio = audio1
            else:
                combine_audio = combine_audio + audio1
        
        combine_audio.export(f"audios/{audio_filename}.mp3", format="mp3")
        return True
    except:
        return False

def generate_tts_audio(text: str, languague: str, audio_filename: str):
    tts = gTTS(text=text, lang=languague, slow=False)
    tts.save(f"audios/{audio_filename}.mp3")