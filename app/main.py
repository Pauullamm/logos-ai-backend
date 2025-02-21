import uvicorn
import sys
from .agent.agent import call_llm, ExplanationModel
from .agent.prompt import GREEK_AGENT_PROMPT
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader


api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

app = FastAPI(docs_url="/docs", openapi_url="/openapi.json")  # By default, docs are enabled

class AnalysisRequest(BaseModel):
    bookTitle: str
    chapterNum: int
    verseNum: int
    english: str
    greek: str
    highlightedWord: str
    
@app.post("/analyse")
async def analyse_greek(payload: AnalysisRequest, api_key: str = Security(api_key_header)):
    """
    Analyzes a highlighted Greek word and provides an explanation of its usage and translation.

    This endpoint takes in a Greek word with its surrounding context and provides an AI-generated 
    explanation, including grammatical details, translation rationale, and more.

    **Parameters:**
    - `payload` (AnalysisRequest): A JSON object containing the following:
        - `bookTitle` (str): The title of the book in which the word appears.
        - `chapterNum` (int): The chapter number where the word appears.
        - `verseNum` (int): The verse number where the word appears.
        - `english` (str): The English translation of the verse containing the word.
        - `greek` (str): The Greek text of the verse containing the word.
        - `highlightedWord` (str): The Greek word that needs to be analyzed.

    - `api_key` (str): The authorization key sent via the `Authorization` header to authenticate the request.

    **Returns:**
    - `ai_explanation` (ExplanationModel): A structured explanation of the Greek word's usage, declension, grammatical role, and context in both Greek and English.

    **Example Request:**
    ```json
    {
        "bookTitle": "The Epistle of Paul to the Ephesians",
        "chapterNum": 6,
        "verseNum": 22,
        "english": "Him I have sent to you for this very thing, that you may know the things concerning us and that he may comfort your hearts.",
        "greek": "ὃν ἔπεμψα πρὸς ὑμᾶς εἰς αὐτὸ τοῦτο, ἵνα γνῶτε τὰ περὶ ἡμῶν καὶ παρακαλέσῃ τὰς καρδίας ὑμῶν.",
        "highlightedWord": "παρακαλέσῃ"
    }
    ```

    **Example Response:**
    ```json
    {
        "word": "παρακαλέσῃ",
        "declension": "Aorist Subjunctive",
        "grammar_role": "Verb",
        "translation_rationale": "The verb 'παρακαλέσῃ' is translated as 'comfort' in this context, as it carries the meaning of providing encouragement or solace.",
        "without_jargon": "In simpler terms, the word means 'to comfort' or 'to encourage'.",
        "context": "In this verse, the word 'παρακαλέσῃ' is used to describe the action of offering comfort to others."
    }
    ```
    
    **Errors:**
    - `400 Bad Request`: If the required parameters are missing in the request body.
    - `401 Unauthorized`: If the API key is missing or invalid.
    - `500 Internal Server Error`: If there is an unexpected error during processing.

    """

    try:
        if not api_key:
            raise HTTPException(status_code=401, detail="Gemini API Key not provided")

        if not payload:
            raise HTTPException(status_code=400, detail="Missing 'message' in request body")

        ai_explanation: ExplanationModel = call_llm(api_key=api_key, 
                                                    system_prompt=GREEK_AGENT_PROMPT, 
                                                    message=str(payload.model_dump())
                                                    )
        return ai_explanation
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    if "uvicorn" not in sys.argv[0]:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
        