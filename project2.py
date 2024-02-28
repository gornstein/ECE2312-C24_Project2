import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import librosa
import soundfile as sf
import sounddevice as sd
from scipy.signal import butter,filtfilt

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

def gen_tone(freq,dur):
    t = np.linspace(0,dur,sr * dur, endpoint=False)
    tone = np.sin(2 * np.pi * freq * t)
    return tone

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
# are for B4f,C5,G4#,G3#,Ef4
notes = [466.2,523,415.3,207.7,311.1]

# Generate the 5 tones
note1 = gen_tone(notes[0],1)
note2 = gen_tone(notes[1],1)
note3 = gen_tone(notes[2],1)
note4 = gen_tone(notes[3],1)
note5 = gen_tone(notes[4],2)

# Put them together
cetk = np.concatenate([note1,note2,note3,note4,note5])

sf.write("teamOrnstein-cetk.wav",cetk,sr)
create_spectrogram(cetk,2000,"CETK Chord Progression")

## Combining Sound Files
quickfox, sr = sf.read("quickfox.wav")
quickfox_5000 = quickfox + sinetone[0:192000,] # My quickfox is only 4s

sf.write("teamOrnstein-speechchirp.wav",quickfox_5000,sr)
create_spectrogram(quickfox_5000,8000,"Quickfox + 5000Hz Sine Tone")

## Speech and audio filtering
# Create a butterworth lowpass filter
# order=5, cutoff=4000Hz
b,a = butter(5,(4000/(sr*0.5)),btype='low',analog=False)

# Filter the quickfox+sinewave
filtered_quickfox_5000 = filtfilt(b,a,quickfox_5000)

sf.write("teamOrnstein-filteredspeechsine.wav",filtered_quickfox_5000,sr)
create_spectrogram(filtered_quickfox_5000,8000,"Quickfox + 5000Hz Sine + 4000Hz Lowpass")

## Stereo Fun
# Combine the two signals to stereo
stereo_fun = np.asarray([quickfox,quickfox_5000]).T
# Spectrograms are already generated for each for report

sf.write("teamOrnstein-stereospeechsine.wav",stereo_fun,sr)