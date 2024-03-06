import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


class OpenAIModel:
    def __init__(self, model_type="gpt-4"):
        self.model_type = model_type

    def execute_prompt(self, chat_prompt):
        response = openai.ChatCompletion.create(
            model=self.model_type,
            messages=[
                {"role": "user", "content": chat_prompt},
            ],
            temperature=0.1,
        )
        response_msg = response["choices"][0]["message"]
        return response_msg["content"]

    def fix_transcript(self, transcript):
        prompt = f"""Given the following paragraph transcript, apply the following changes if needed. Remove filler words. Examples: I think, I guess, yeah, you know, like. Remove repetitions and touch up phrases and sentences that look weird in writing. Improve the flow but try to use the same words spoken by the speaker wherever possible. Add quotation marks when the speaker is referring to what someone else might say. Split text into paragraphs. Please check your work. 
\n\nTranscript: {transcript} \n\n Formatted transcript:"""
        fixed_transcript = self.execute_prompt(prompt)
        return fixed_transcript

    def add_links(self, transcript):
        prompt = f"""Given the following paragraph transcript, add any wikipedia links in Markdown if needed. Using the formatting of [TEXT](LINK) in markdown. Only add links to relevant terms / company names / etc. Return back the original transcript with links added if needed. 
        \n\n Transcript: {transcript} \n\n Transcript with links:"""
        linked_transcript = self.execute_prompt(prompt)
        return linked_transcript


openai_model = OpenAIModel()
