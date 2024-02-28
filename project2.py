import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import librosa
import soundfile as sf
import sounddevice as sd

duration = 5
fs = sr = 48000
sd.default.device = 0

# Create and format spectrogram
def create_spectrogram(audio,maxfreq,plotname):
    freq = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
    librosa.display.specshow(freq,sr=sr, x_axis='time', y_axis='linear')
    plt.ylim([0,maxfreq])
    plt.title('Spectrogram - '+plotname)
    plt.savefig(plotname+"-SG.png")
    plt.show()

# Generate time axis (for all problems)
x = np.linspace(0, duration, sr * duration, endpoint=False)

## Sine Tone Generation:
freq1 = x * 5000
sinetone = np.sin((2 * np.pi) * freq1)

# Write sinetone to file
sf.write("teamOrnstein-sinetone.wav",sinetone,sr)

create_spectrogram(sinetone,6000,"5000Hz Sinetone")

## Chirp Signal Generation
freq_step = (8000 / (sr * duration)) / 2
freq2 = x
freq_count = 0
   
# Multiply elements by their new frequency
for i in range(len(freq2)):
    freq2[i] = x[i]*freq_count
    # Increment frequency
    freq_count = freq_count + freq_step

chirp = np.sin((2*np.pi)*freq2)
sf.write("teamOrnstein-chirp.wav",chirp,sr)
create_spectrogram(chirp,9000,"0-8000Hz Chirp Signal")

## Some Fun with Sine Tone
# Someone commented what the likely notes are in the YT video so these freqs
# are for B4f,C4,G4#,G3#,Ef4
notes = [466.2,261.6,415.3,207.7,311.1]
secondspernote = [0.4,0.6,0.85,0.6,1.57]
samples = secondspernote * (sr*duration/5)

freq3 = x

i_l = 0
i_u = samples[0]
current_note = 0
# Multiply samples by their new frequencies
for i in range(len(freq3)):
    if i_l <= i < i_u:
        freq3[i] = x[i]*notes[current_note]
    else:
        # Next note
        current_note = current_note + 1
        # For no note:
        if current_note > len(seconds)-1:
            freq3[i] = x[i]*0
            continue
        else:
            i_l = i_u
            i_u = i_u + samples[current_note]
                
sinetonefun = np.sin((2*np.pi)*freq3)
sf.write("teamOrnstein-cetk.wav")
create_spectrogram(sinetonefun,2000,"CETK Chord Progression")