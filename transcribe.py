import os
import json

import assemblyai as aai

from dotenv import  load_dotenv
from datetime import datetime

load_dotenv()

api_key = os.environ.get('ASSEMBLY_AI_API_KEY')

aai.settings.api_key = api_key

audio_file = "audio/spraak_1.m4a"

config = aai.TranscriptionConfig(
  speech_model=aai.SpeechModel.universal,
  speaker_labels=True,
  language_code='nl',
  speakers_expected=3
)

transcript = aai.Transcriber(config=config).transcribe(audio_file)


if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

audio_file_name = audio_file.split('/')[-1].split('.')[0].replace(' ', '_')
dt_string = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

dst_dir = "transcription/"

# create srt file
srt = transcript.export_subtitles_srt(chars_per_caption=32)

utterances = [
  {
    "speaker": utterance.speaker,
    "start": utterance.start,
    "end": utterance.end,
    "text": utterance.text,
    "words": [
      {
        "confidence": word.confidence,
        "start": word.start,
        "end": word.end,
        "text": word.text,
        "speaker": word.speaker,
      } for word in utterance.words
    ],
    "confidence": utterance.confidence,
  } for utterance in transcript.utterances
]


with open(f"{dst_dir}/{audio_file_name}_{dt_string}.srt", "w") as srt_file:
  srt_file.write(srt)


# create txt file with format:
with open(f"{dst_dir}/{audio_file_name}_{dt_string}.json", 'w+') as json_file:
  json_file.write(json.dumps(utterances))

