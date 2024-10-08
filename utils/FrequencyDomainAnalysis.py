import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from numpy.fft import fft

# 傅里叶变换
class FourierTransform:
    def __init__(self, fs, fig):
        signal = np.squeeze(np.array(fig))
        signal = signal - np.mean(signal) # 去直流分量
        
        L = len(signal)
        N = np.power(2, np.ceil(np.log2(L)))
        Fourier = fft(signal, int(N))/L*2
        
        Amplitude = np.abs(Fourier) 
        self.Amplitude = Amplitude[range(int(N/2))]             # 幅值谱
        
        Phase = np.unwrap(np.angle(Fourier))
        self.Phase = Phase[range(int(N/2))]                     # 相位谱
        
        self.Freqency = np.arange(0,int(N/2))*fs/N              # 横坐标的频率
    
    def plot(self, ShowFreqency = True, ShowPhase = True, Show = True):
        if ShowFreqency:
            plt.plot(self.Freqency, self.Amplitude)
            plt.xlabel('Freqency/Hz')
            plt.ylabel('Amplitude')
            plt.title('Fourier Amplitude Spectrum')
            plt.tight_layout()
            if Show: plt.show()
        if ShowPhase:
            plt.plot(self.Freqency, self.Phase)
            plt.xlabel('Freqency/Hz')
            plt.ylabel('Phase/rad')
            plt.title('Fourier Phase Spectrum')
            plt.tight_layout()
            if Show: plt.show()

# 自功率谱、互功率谱密度与相干函数
# https://www.osgeo.cn/scipy/reference/signal.html
class PowerSpectralDensity:
    def __init__(self, fs, *figs):
        signals = []
        for fig in figs:
            signal = np.squeeze(np.array(fig))
            signal = signal - np.mean(signal)
            signals.append(signal)
        self.SigNum = len(signals)
        
        if self.SigNum == 1:
            # 默认使用Hanning窗，频率取一半
            self.Frequency, self.Auto = sig.welch(signals[0], fs)
            
        elif self.SigNum == 2:
            self.Frequency, self.Cross = sig.csd(signals[0], signals[1], fs)
            _, self.Coherence = sig.coherence(signals[0], signals[1], fs)
    
    def plot(self):
        if self.SigNum == 1:
            plt.plot(self.Frequency, self.Auto)
            plt.xlabel('Frequency/Hz')
            plt.ylabel('PSD')
            plt.title('Auto Power Spectral Density')
            plt.tight_layout()
            plt.show()
            
        elif self.SigNum == 2:           
            plt.subplot(2,1,1)
            plt.plot(self.Frequency, self.Cross)
            plt.xlabel('Frequency/Hz')
            plt.ylabel('PSD')
            plt.title('Cross Power Spectral Density')
            plt.tight_layout()
            plt.show()
            
            plt.subplot(2,1,2)
            plt.plot(self.Frequency, self.Coherence)
            plt.xlabel('Frequency/Hz')
            plt.title('Coherence Function')
            plt.tight_layout()
            plt.show()
            
# Hilbert包络谱
class EnvelopeSpectrum:
    def __init__(self, fs, fig):
        signal = np.squeeze(np.array(fig))
        # signal = signal - np.mean(signal) # 去直流分量

        Hilbert = sig.hilbert(signal)

        self.InstantAmplitude = np.abs(Hilbert)                         # 瞬时幅值
        self.InstantPhase = np.unwrap(np.angle(Hilbert))                # 瞬时相位
        self.InstantFrequency = np.diff(self.InstantPhase)/(2*np.pi)*fs # 瞬时频率
        

    def plot(self, fs, fig):
        signal = np.squeeze(np.array(fig))
        # signal = signal - np.mean(signal) # 去直流分量
        N = len(signal)
        Time = np.arange(0, N)/fs
        
        plt.plot(Time, signal, 'b-')
        plt.plot(Time, self.InstantAmplitude, 'r')
        plt.title('Modulated Signal and Extracted Envelope')
        plt.xlabel('Time/s')
        plt.ylabel('x(t) and |z(t)|')