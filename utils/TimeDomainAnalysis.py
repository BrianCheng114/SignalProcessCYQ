import numpy as np
import matplotlib.pyplot as plt

# 时域统计量及部分指标
class TimeDomainFeature:
    def __init__(self, fig):
        signal = np.squeeze(np.array(fig))
        
        # 基本统计量指标
        self.Mean = np.mean(signal)                         # 均值
        self.SquareMean = np.mean(signal**2)                # 均方值
        self.Variance = np.var(signal)                      # 方差
        self.std = signal.std()                             # 标准差

        # 有量纲指标
        self.xr = np.mean(np.sqrt(np.abs(signal)))**2       # 方根幅值
        self.RMS = np.sqrt(self.SquareMean)                 # 有效值
        self.Peak = np.max(np.abs(signal))                  # 峰值
        self.Skewness = np.mean((signal - self.Mean)**3)    # 偏斜度
        self.Kurtosis = np.mean((signal - self.Mean)**4)    # 峭度

        # 无量纲指标
        self.W = self.RMS/self.Mean                         # 波形指标
        self.C = self.Peak/self.RMS                         # 峰值指标
        self.I = self.Peak/self.Mean                        # 脉冲指标
        self.L = self.Peak/self.xr                          # 裕度指标
        self.S = self.Skewness/self.std**3                  # 偏斜度指标
        self.K = self.Kurtosis/self.std**4                  # 峭度指标
        
# 概率密度函数       
class ProbabilityDensity:
    def __init__(self, fig, bins = 20):
        # 概率分布直方图，默认段数为20
        signal = np.squeeze(np.array(fig))
        self.Hist, self.Edges = np.histogram(signal, bins, density = True)
        
    def plot(self):
        # 内置画图函数
        _, ax1 = plt.subplots()
        
        ax1.hist(self.Edges[:-1], self.Edges, weights = self.Hist, facecolor = 'skyblue',
                alpha = 0.7, edgecolor = 'k')
        ax1.set_xlabel('Value')
        ax1.set_ylabel('Probability Density')

        plt.title('Probability Density Function')
        plt.show()
        
      
# 自相关与互相关函数 
'''
注意: numpy中的相关函数计算的是线性相关, 不够长的地方会补零, 
而满足Wiener-Khinchin关系的相关是循环相关, 不够长的部分做周期
延拓, 因此PSD与下面的相关函数不构成Fourier变换对
'''     
class Correlation:
    def __init__(self, fs, *figs):
        
        signals = []
        for fig in figs:
            signal = np.squeeze(np.array(fig))
            signals.append(signal)
        
        self.SigNum = len(signals)
        
        N = len(signals[0])
        self.Time = np.arange(0, N)/fs
        
        if self.SigNum == 1:
            Auto = np.correlate(signals[0], signals[0], mode='full')
            Auto = Auto[N-1:] # 自相关函数计算时存在负项，消除其影响，只取一半
            Auto = Auto/np.arange(N, 0, -1) # 消除时间长度的影响
            self.Auto = Auto/Auto[0] # 归一化
            
        elif self.SigNum == 2:
            # 计算互相关函数，要求两信号长度必须相同
            Cross = np.correlate(signals[0], signals[1], mode='full')
            Cross = Cross[N-1:]
            Cross = Cross/np.arange(N, 0, -1)
            self.Cross = Cross/Cross[0]
        
    def plot(self):
        if self.SigNum == 1:
            plt.plot(self.Time, self.Auto)
            plt.xlabel('Time/s')
            plt.ylabel('Rx')
            plt.title('Auto Correlation Function')
            plt.show()
            
        elif self.SigNum == 2:
            plt.plot(self.Time, self.Cross)
            plt.xlabel('Time/s')
            plt.ylabel('Rxy')
            plt.title('Cross Correlation Function')
            plt.show()