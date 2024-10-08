# 信号处理学习

### 数据格式

文档中只保存了两个数据，来源为
http://csegroups.case.edu/bearingdatacenter/download-data-file

格式如下：
> - N - Normal Baseline Data 正常基线数据
> - IR - Inner Race 内圈故障
> - B - Ball 滚子故障
> - OR - Outer Race 外圈故障
>     - OR3 - Orthogonal(3:00) 三点钟方向故障
>     - OR6 - Centered(6:00) 六点钟方向故障
>     - OR12 - Opposite(12:00) 十二点钟方向故障
> - DE - drive end accelerometer data 驱动端加速度数据
> - FE - fan end accelerometer data 旋转端加速度数据
> - BA - base accelerometer data 基本加速度数据
> - time - time series data 时间序列数据
> - RPM - rpm during testing 测量时的轴承转速

### 文件列表

##### utils

- TimeDomainAnalysis.py
包括了时域统计量（均值、均方值、方差、标准差等指标）、概率密度函数与相关函数计算程序

- FreqencyDomainAnalysis.py
包括了傅里叶变换、自功率谱密度、互功率谱密度、相干函数与HilBert包络谱的计算程序

- TimeFreqencyDomainAnalysis.py
包括了短时傅里叶变换、多分辨分析、绘制小波波形、连续小波变换的程序

##### HHT
源代码来自 https://github.com/chendaichao/Hilbert-Huang-transform.git ，可进行EMD与HHT的计算。