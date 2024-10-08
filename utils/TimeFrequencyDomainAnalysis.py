import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import pywt


# 短时傅里叶变换 STFT

class ShortTimeFourierTransform:
    def __init__(self, fs, fig, 
                 nperseg = 256,
                 overlap = 0.5):
        # 输入参数: 窗长与重叠率
        signal = np.squeeze(np.array(fig))
        signal = signal - np.mean(signal) # 去直流分量
        
        noverlap = int(nperseg*overlap)
        
        (self.Frequency, 
         self.Time, 
         self.STFTvalue) = sig.stft(signal, fs, nperseg=nperseg, noverlap=noverlap)

    def plot(self):
        plt.pcolormesh(self.Time, self.Frequency, np.abs(self.STFTvalue))
        plt.colorbar()
        plt.ylabel('Frequency/Hz')
        plt.xlabel('Time/s')
        plt.title('Short Time Fourier Transform')
        plt.show()
        
# 小波分析

# 展示不同小波的波形
def WaveletShow(*wavelets):
    N = len(wavelets)
    rows = int(np.ceil(np.sqrt(N)))
    cols = int(np.ceil(N/rows))
    for i in range(N):
        [psi, x] = pywt.ContinuousWavelet(wavelets[i]).wavefun(10)
        
        plt.subplot(rows, cols, i+1)
        plt.plot(x, np.real(psi), label="real")
        
        if np.max(np.abs(np.imag(psi))) > 1e-3:
            plt.plot(x, np.imag(psi), label="imag")
        
        plt.suptitle('Wavelets Demostarion')
        plt.xlim([-5, 5])
        # plt.ylim([-0.8, 1])
        plt.legend()
        plt.title(wavelets[i])
    
    plt.tight_layout()
    plt.show()
    
# 多分辨分析   
class MultiResolutionAnalysis:
    def __init__(self, fs, fig, wavelet='bior1.1'):
        signal = np.squeeze(np.array(fig))
        self.Multi = pywt.mra(signal, wavelet = wavelet)
        self.level = len(self.Multi)
        self.fs = fs
        
    def plot(self, Show = True):
        Time = np.arange(0, len(self.Multi[0]))/self.fs
        for i in range(self.level):            
            plt.subplot(self.level, 1, i+1)
            plt.plot(Time, self.Multi[i])    
        
        plt.suptitle('Multi-Resolution Analysis')
        plt.tight_layout()
        if Show: plt.show()
        
# 连续小波变换
class ContinuousWaveletTransform:
    def __init__(self, fs, fig, wavelet='cmor1.5-1.0', freqNum = 100):
        '''
        fs: 信号频率
        fig: 原始信号
        wavelet: 连续小波种类
        freqNum: 频率域细分点个数
        '''
        signal = np.squeeze(np.array(fig))
        signal = signal - np.mean(signal) # 去直流分量
        
        widths = np.geomspace(1, 1024, num = freqNum)
        self.time = np.arange(0, len(signal))/fs

        self.cwtmatr, self.freqs = pywt.cwt(signal, widths, wavelet, sampling_period=1/fs)
        self.cwtmatr = np.abs(self.cwtmatr[:-1, :-1]) # cwt结果为复数，要取模

    def plot(self, logspace = True):
        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.time, self.freqs, self.cwtmatr)
        
        if logspace:
            axs.set_yscale("log")
        else:
            axs.set_yscale("linear")
        
        axs.set_xlabel("Time (s)")
        axs.set_ylabel("Frequency (Hz)")
        axs.set_title("Continuous Wavelet Transform (Scaleogram)")
        fig.colorbar(pcm, ax=axs)
        plt.show()