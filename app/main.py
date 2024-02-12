from fastapi import FastAPI, HTTPException, File, UploadFile, Response
from pydantic import BaseModel
from matplotlib.figure import Figure
from io import BytesIO
from typing import List
import shutil
import os
import uvicorn
from utils.mark_preprocessing import MarkPreprocessing
from utils.pitch_energy import analyze_audio

PATH = os.path.dirname(os.path.abspath(__file__))

class AudioData(BaseModel):
    transcription: str
    duration: float

class WPMProcessor:
    @staticmethod
    def calculate_wpm(transcription: str, duration: float) -> float:
        norm_transcription = MarkPreprocessing.normalize(transcription)
        words = len(norm_transcription.split())
        return words / duration * 60

app = FastAPI(title="Speech Analysis API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Welcome to the WPM API"}

@app.post("/word_per_minute")
async def wpm(audio_data: List[AudioData]):
    if not audio_data or len(audio_data) != 1 or not isinstance(audio_data[0].transcription, str) or not isinstance(audio_data[0].duration, (int, float)):
        raise HTTPException(status_code=400, detail="Invalid audio data. Please provide a list with transcription and duration.")

    result = WPMProcessor.calculate_wpm(audio_data[0].transcription, audio_data[0].duration)
    return {"wpm": result}

@app.post("/analyze_audio")
async def analyze_audio_endpoint(audio_file: UploadFile = File(...)):
    save_path = f"{PATH}/temp_audio/{audio_file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)

    analysis_results = analyze_audio(save_path)
    os.remove(save_path)

    # Generate plots
    fig = Figure(figsize=(10, 8))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    ax1.plot(analysis_results["t_frame"], analysis_results["pitch"], label='Pitch')
    ax1.set_title('Pitch over Time')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Pitch (Hz)')
    
    ax2.plot(analysis_results["time"], analysis_results["energy"], label='Energy', color='red')
    ax2.set_title('Energy over Time')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Energy')
    
    ax3.plot(analysis_results["t_frame"], analysis_results["frame_based_energy"], label='Frame-based Energy', color='green')
    ax3.set_title('Frame-based Energy over Time')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Frame-based Energy')

    # Save the figure to a BytesIO object
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Return the plot as a response
    return Response(content=buf.getvalue(), media_type="image/png")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)