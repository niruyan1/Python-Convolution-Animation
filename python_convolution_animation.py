#%%
%clear
%reset -f
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, ellip, filtfilt, freqz, butter, firwin
import time
plt.close("all")

# Step 1: Generate sine function with frequencies of 5 Hz and 10 Hz
fs = 5000  # Sampling frequency
t = np.arange(0, 1, 1/fs)  # Time vector

f0 = 1    # Starting frequency (Hz)
f1 = 50  # Ending frequency (Hz)
t1 = 1     # Time at which f1 is achieved (s)
#signal = np.sin(2*np.pi*5*t) + np.sin(2*np.pi*10*t)
signal = chirp(t, f0, t1, f1, method='linear')

# Step 2: Add Gaussian noise
noise = np.random.normal(0, 0.01, len(t))  # Gaussian noise with mean=0 and std=0.1
noisy_signal = 0.1*signal + noise

# Step 3: Design low-pass filter
cutoff = f1*2  # Cutoff frequency of the low-pass filter
order = 1001  # Filter order
nyquist = 0.5 * fs
cutoff_norm = cutoff / nyquist
# Use Kaiser window with beta=5 to minimize ripple
b = firwin(order, cutoff_norm, window=('kaiser', 5))

# Step 4: Apply low-pass filter to noisy signal
filtered_signal = filtfilt(b, 1, noisy_signal)

# Step 5: Plot time and frequency representations
plt.figure(figsize=(10, 8))

# Original signal
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t, signal, 'b', label='Original Signal')
plt.title('Original  (Linear frequency modulated waveform)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Plot the FFT
fft_result = np.fft.fft(signal)
plt.subplot(2, 1, 2)
plt.xlim(0, cutoff+100)
plt.plot(np.abs(fft_result)/(fs/2))
plt.title('FFT of the Original Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.tight_layout()

# Noisy signal

plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t, noisy_signal, 'r', label='Noisy Signal')
plt.title('Signal with Gaussian Noise')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Plot the FFT of noisy
fft_result = np.fft.fft(noisy_signal)
plt.subplot(2, 1, 2)
plt.xlim(0, f1+100)
plt.plot(np.abs(fft_result)/(fs/2))
plt.title('FFT of the Noisy Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.tight_layout()

# Filter frequency response
plt.figure(figsize=(10, 5))
w, h = freqz(b, worN=8000)
plt.xlim(0, cutoff+100)
plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'g')
plt.title('Frequency Response of Low-pass Filter')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Gain')
plt.grid(True)
plt.tight_layout()

# Filtered signal
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t, filtered_signal, 'm', label='Filtered Signal')
plt.title('Filtered Signal (Low-pass Filtered)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()
# Plot the FFT of filtered
fft_filtered = np.fft.fft(filtered_signal)
plt.subplot(2, 1, 2)
plt.xlim(0, cutoff+100)
plt.plot(np.abs(fft_filtered)/(fs/2))
plt.title('FFT of the Filtered Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.tight_layout()

#%%
t = np.arange(-1.5, 2, 1/fs)

signal=np.append(signal, np.zeros(len(t)-len(signal)))
noisy_signal=np.concatenate((np.zeros(int(abs(min(t))*fs)), noisy_signal))
noisy_signal=np.append(noisy_signal, np.zeros(len(t)-len(noisy_signal)))

match_filter=signal

step=200
conv_result=np.zeros(len(t))
for n in range(0, len(t)):
    conv_result[n]=np.dot(match_filter,noisy_signal)
    match_filter = np.roll(match_filter, 1)
    
    
    if n%step==0:
            
            plt.subplot(2, 1, 1)
            plt.plot(t, noisy_signal, 'r', label='Noisy Signal')
            plt.plot(t, signal, 'b', label='Match Filter')
            plt.title('Convolution Animation')
            plt.xlabel('Time [s]')
            plt.ylabel('Amplitude')
            plt.legend()
            plt.grid(True)
            
            plt.subplot(2, 1, 2)
            plt.plot(t, conv_result, 'r', label='Result')
            plt.title('Convolution Result')
            plt.xlabel('Time [s]')
            plt.ylabel('Amplitude')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            
        
            plt.pause(0.02)
            plt.clf()
            signal = np.roll(signal, step)
    
    
