from google import genai
from google.genai import types
from dotenv import load_dotenv
from .prompt import GREEK_AGENT_PROMPT
import os
import json

from google import genai
from pydantic import BaseModel

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')


class ExplanationModel(BaseModel):
    word: str
    declension: str
    grammar_role: str
    translation_rationale: str
    without_jargon: str
    context: str
    
    
def call_llm(api_key: str, system_prompt: str, message: str) -> ExplanationModel:
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type='application/json',
        response_schema=ExplanationModel
    )
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=message,
        config=config
    )
    return response.parsed

test_input = json.dumps({
    "title": "The Epistle of Paul to the Ephesians",
    "chapterNum": 6,
    "verseNum": 22,
    "english": "Him I have sent to you for this very thing, that you may know the things concerning us and that he may comfort your hearts.",
    "greek": "ὃν ἔπεμψα πρὸς ὑμᾶς εἰς αὐτὸ τοῦτο, ἵνα γνῶτε τὰ περὶ ἡμῶν καὶ παρακαλέσῃ τὰς καρδίας ὑμῶν.",
    "highlightedWord": "παρακαλέσῃ"
}, ensure_ascii=False)

# data = call_llm(api_key=gemini_api_key, system_prompt=GREEK_AGENT_PROMPT, message=test_input)
# print(data.word)
# print(data.declension)
# print(data.grammar_role)
# print(data.translation_rationale)
# print(data.without_jargon)
# print(data.context)