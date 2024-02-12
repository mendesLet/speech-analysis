import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

def get_energy(y, hop_length):
    energy = np.square(y)
    frame_based_energy = librosa.feature.rms(y=y, hop_length=hop_length)[0]

    return energy, frame_based_energy

def get_pitches(y, sr, hop_length):
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=hop_length)

    pitch = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch.append(pitches[index, t])

    pitch = np.array(pitch)

    return pitch

def analyze_audio(audio_file):
    y, sr = librosa.load(audio_file, mono=True)

    hop_length = 512
    energy, frame_based_energy = get_energy(y, hop_length)
    pitch = get_pitches(y, sr, hop_length)

    # Time vectors for plotting (might not be necessary for API response but kept for completeness)
    time = np.arange(0, len(y)) / sr
    frames = range(len(frame_based_energy))
    t_frame = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)

    # Prepare the results
    results = {
        "energy": energy.tolist(),  # Convert to list for JSON serialization
        "frame_based_energy": frame_based_energy.tolist(),  # Convert to list for JSON serialization
        "pitch": pitch.tolist(),  # Convert to list for JSON serialization
        "time": time.tolist(),  # Time vector for the entire signal
        "t_frame": t_frame.tolist(),  # Time vector for frame-based data
    }

    return results