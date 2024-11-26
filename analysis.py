import numpy as np
import matplotlib.pyplot as plt
# Parameters for message signal

tot = 1
td = 0.002
t = np.arange(0, tot, td)
x = np.sin(2 * np.pi * t) - np.sin(6 * np.pi * t)
plt.figure()
plt.plot(t, x, linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Input Message Signal')
plt.grid(True)
plt.show()
# Spectrum of the message signal
L = len(x)
Lfft = 2 ** int(np.ceil(np.log2(L)))
fmax = 1 / (2 * td)
Faxis = np.linspace(-fmax, fmax, Lfft)
Xfft = np.fft.fftshift(np.fft.fft(x, Lfft))
plt.figure()
plt.plot(Faxis, np.abs(Xfft))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
5
plt.title('Spectrum of Input Message Signal')
plt.grid(True)
plt.show()
# Sampling
ts = 0.02
n = np.arange(0, tot, ts)
x_sampled = np.sin(2 * np.pi * n) - np.sin(6 * np.pi * n)
plt.figure()
plt.stem(n, x_sampled, basefmt=" ")  # use_line_collection=True
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Sampled Signal')
plt.grid(True)
plt.show()
# Reconstruction
Nfactor = int(ts / td)
xsmu = np.zeros(len(t))
xsmu[::Nfactor] = x_sampled
Lffu = 2 ** int(np.ceil(np.log2(len(xsmu))))
fmaxu = 1 / (2 * td)
Faxisu = np.linspace(-fmaxu, fmaxu, Lffu)
Xfftu = np.fft.fftshift(np.fft.fft(xsmu, Lffu))
BW = 10
H_lpf = np.zeros(Lffu)
H_lpf[Lffu // 2 - BW:Lffu // 2 + BW] = 1
x_recv = Nfactor * Xfftu * H_lpf
x_recv_time = np.real(np.fft.ifft(np.fft.fftshift(x_recv)))
plt.figure()
plt.plot(t, x, 'r', t, x_recv_time[:len(t)], 'b--', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Original vs. Reconstructed Signal')
plt.grid(True)
plt.show()


# Define quantization levels
levels = 16
x_min = np.min(x_sampled)
x_max = np.max(x_sampled)
step = (x_max - x_min) / levels
# Quantize the sampled signal
x_quantized = step * np.round((x_sampled - x_min) / step) + x_min
# Plot quantized vs. sampled signal
plt.figure()
plt.stem(n, x_sampled, 'r', markerfmt='ro', basefmt=" ",label='Sampled Signal') #  use_line_collection=True, 
plt.stem(n, x_quantized, 'b--', markerfmt='bo', basefmt=" ",label='Quantized Signal') # use_line_collection=True, 
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Sampled Signal vs. Quantized Signal')
plt.legend()
plt.grid(True)
plt.show()
# Quantization error
quantization_error = x_sampled - x_quantized
plt.figure()
plt.stem(n, quantization_error, basefmt=" ") # use_line_collection=True
plt.xlabel('Time (s)')
plt.ylabel('Error')
plt.title('Quantization Error')
plt.grid(True)
plt.show()
