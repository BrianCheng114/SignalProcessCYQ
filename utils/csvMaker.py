from scipy.io import loadmat
import os
import pandas as pd

'''
http://csegroups.case.edu/bearingdatacenter/download-data-file
数据预处理: mat文件必须在文件夹matFigure下, 输入其母文件夹(如.../48k/), 在母文件夹下创建新的子文件夹csvFigure
N - Normal Baseline Data
IR - Inner Race
B - Ball
OR - Outer Race
    OR3 - Orthogonal(3:00)
    OR6 - Centered(6:00)
    OR12 - Opposite(12:00)

DE - drive end accelerometer data
FE - fan end accelerometer data
BA - base accelerometer data
time - time series data
RPM - rpm during testing
'''

def mat_to_csv(PATH):
    MAT_PATH = PATH + 'matFigure/'
    filenames = os.listdir(MAT_PATH)

    for filename in filenames:
        data = loadmat(MAT_PATH + filename, mat_dtype = True)
        for item in data.items():
            if item[0][:2] != '__':
                # 读入mat文件时前两项不需要
                # 执行这一代码，相当于创建以变量名为名称的变量
                # exec(filename[:-7] + item[0][4:7] + "=item[1]")
                df = pd.DataFrame(item[1])
                df.to_csv(PATH + 'csvFigure/' + filename[:-7] + item[0][4:7] + '.csv', 
                        index=False)
            
if __name__ == '__main__':
    PATH = './Data/Case/48k/'
    mat_to_csv(PATH)

