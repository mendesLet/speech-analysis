import requests
from typing import List
from pydantic import BaseModel

class AudioData(BaseModel):
    transcription: str
    duration: float

audio_data_list = [
    AudioData(transcription="Hello world", duration=10.0),
]

url = "http://localhost:8000/word_per_minute"  

audio_data_dict_list = [ad.dict() for ad in audio_data_list]

response = requests.post(url, json=audio_data_dict_list)

if response.status_code == 200:
    result = response.json()
    print(f"Word per minute: {result}")
else:
    print(f"Error: {response.status_code}, {response.text}")
