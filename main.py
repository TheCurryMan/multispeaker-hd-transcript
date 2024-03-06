from apis.assembly import AssemblyAIModel
from apis.oai import OpenAIModel
from models.transcript import Transcript
import json


def load_temp_files():
    with open("transcript.json", "r") as f:
        word_transcript = json.load(f)
    with open("formatted_paragraph_transcript.json", "r") as f:
        paragraph_transcript = json.load(f)
    return word_transcript, paragraph_transcript


if __name__ == "__main__":
    assembly = AssemblyAIModel()
    # Load temp files for testing
    # word_transcript, paragraph_transcript = load_temp_files()
    word_transcript = assembly.transcribe_audio("./demo.mp3")
    transcript = Transcript(word_transcript, formatted_transcript=None)
    transcript.format_paragraphs()
    transcript.pp_markdown(speakers=["Patrick", "Dwarkesh"])
