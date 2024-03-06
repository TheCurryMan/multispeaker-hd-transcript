from apis.oai import openai_model
import json


class Transcript:
    def __init__(self, word_transcript, formatted_transcript=None):
        self.word_transcript = word_transcript
        self.paragraph_transcript = self.get_paragraph_transcript()
        self.formatted_transcript = formatted_transcript

    def get_paragraph_transcript(self):
        paragraphs = []
        cp = {
            "start": None,
            "paragraph": "",
            "speaker": None,
        }
        for word in self.word_transcript:
            if cp["speaker"] == None or word["speaker"] == cp["speaker"]:
                cp["paragraph"] += " " + word["word"]
                if cp["start"] == None:
                    cp["start"] = word["start"]
                    cp["speaker"] = word["speaker"]
            else:
                paragraphs.append(cp)
                cp = {
                    "start": word["start"],
                    "paragraph": word["word"],
                    "speaker": word["speaker"],
                }
        return paragraphs

    def convert_seconds(self, total_seconds):
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    def pp_markdown(self, speakers=None):
        with open("transcript.md", "w") as f:
            for p in self.formatted_transcript:
                para = str(p["paragraph"]).replace("\n\n", "<br/>")
                para = para.replace("\n", "<br/>")
                if para[0] and para[-1] == '"':
                    para = para[1:-1]
                speaker_index = ["A", "B", "C"].index(p["speaker"].strip())
                if speaker_index != -1:
                    line = f"**{speakers[speaker_index]}** *{self.convert_seconds(p['start'])}* <br/>{para}<br/>"
                    f.write(line)
                    print(line)
                else:
                    print("ERROR")
                    break

    def format_paragraphs(self):
        pt = self.paragraph_transcript
        for cp in self.paragraph_transcript:
            up = openai_model.fix_transcript(cp["paragraph"])
            up_link = openai_model.add_links(up)
            cp["paragraph"] = up_link
            print(self.paragraph_transcript[0])
        self.formatted_transcript = self.paragraph_transcript
        with open("formatted_paragraph_transcript.json", "w") as f:
            json.dump(pt, f)
