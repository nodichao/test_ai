from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_ollama import ChatOllama
import requests
import httpx
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="AI Text Summarizer Interview")

# TODO 0:
# Initialize the Ollama language model using llama3.2:3b
# and configure the temperature .

llm = "llama3.2:3b"


class SummaryRequest(BaseModel):
    text: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/summarize")
async def summarize(data: SummaryRequest):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # TODO 1: Create a prompt asking the AI to summarize data.text
    prompt = f"""
            Vous etes un expert en resume de textes, reformulations et vous savez faire
            des  explications claires.
            Resumez le texte {data.text} en 1 ou 2 phrases
            """

    # TODO 2: Send the prompt to Ollama 
    # Extract the generated text from the response.
    async with httpx.AsyncClient() as client :
        summary = await client.post(url='http://localhost:11434/api/generate', data={
            'model': llm,
            'prompt': prompt
            })


        if summary is None:
                raise HTTPException(
                    status_code=501,
                    detail="Complete TODO 1 and TODO 2 in app.py",
                )
        response = summary.json()
        print(response)

        # TODO 3: Return the summary as JSON
        return response


# Keep the frontend mount after the API routes.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    print("Open http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
