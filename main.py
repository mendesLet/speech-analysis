from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from utils.mark_preprocessing import MarkPreprocessing

class AudioData(BaseModel):
    transcription: str
    duration: float

class WPMProcessor:
    @staticmethod
    def calculate_wpm(transcription: str, duration: float) -> float:
        norm_transcription = MarkPreprocessing.normalize(transcription)
        words = len(norm_transcription.split())
        return words / duration * 60

app = FastAPI(title="WPM API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Welcome to the WPM API"}

@app.post("/word_per_minute")
async def wpm(audio_data: List[AudioData]):
    if not audio_data or len(audio_data) != 1 or not isinstance(audio_data[0].transcription, str) or not isinstance(audio_data[0].duration, (int, float)):
        raise HTTPException(status_code=400, detail="Invalid audio data. Please provide a list with transcription and duration.")

    result = WPMProcessor.calculate_wpm(audio_data[0].transcription, audio_data[0].duration)
    return {"wpm": result}
