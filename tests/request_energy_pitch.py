import requests

url = 'http://localhost:8000/analyze_audio'
file_path = "/home/lettuce/Code/Work/DM1/Teste/audios/2f7fce26-d339-4868-a22c-3fa7afed7f37_0000.wav"

# Open the file in binary mode
with open(file_path, 'rb') as file:
    files = {'audio_file': ("filename.wav", file, 'audio/mpeg')}
    
    # Make the POST request
    response = requests.post(url, files=files)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Assuming the response is an image (as per your code), save the image
        with open('analysis_result.png', 'wb') as out_file:
            out_file.write(response.content)
        print("Analysis complete, result saved as 'analysis_result.png'.")
    else:
        print("Failed to analyze audio. Status code:", response.status_code)