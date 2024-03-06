import assemblyai as aai
import json
from dotenv import load_dotenv
import os

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected=2)


class AssemblyAIModel:
    def __init__(self):
        pass

    def transcribe_audio(self, file_url):
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(file_url)
        transcribed_results = []
        if transcript.words:
            for word in transcript.words:
                start_s = word.start / 1000
                end_s = word.end / 1000
                transcribed_results.append(
                    {
                        "start": start_s,
                        "end": end_s,
                        "word": word.text,
                        "speaker": word.speaker,
                    }
                )
        with open("transcript.json", "w") as f:
            json.dump(transcribed_results, f)
        return transcribed_results
