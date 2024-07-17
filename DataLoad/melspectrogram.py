import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.ticker as ticker
import os
#这是一个画图函数，方便后续作图
def __init__(self,n):
    self.fileName = n
def personal_plot(x,y):
    plt.figure(dpi=200,figsize=(12,6))
    rcParams['font.family']='Comic Sans MS'
    plt.plot(x,y)
    plt.xlim(x[0],x[-1])
    plt.xlabel('time/s',fontsize=20)
    plt.ylabel('Amplitude',fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid()
def DrawMelSpectrogram(fileName):
    #注意如果文件名不加路径，则文件必须存在于python的工作目录中
    #fileName = 'E:\XJTLU\SURF20240268\DataLoad\CtrSVDD_0058_T_0066698.flac'
    y,sr = librosa.load(fileName,sr=None)
    tmax = librosa.get_duration(y=y,sr=sr)
    tmax = int(tmax)
    if tmax == 0:
        return
    #这里只获取0-20秒的部分，这里也可以在上一步的load函数中令duration=20来实现
    tmin = 0
    t = np.linspace(tmin,tmax,(tmax-tmin)*sr)
    #personal_plot(t,y[tmin*sr:tmax*sr])
    alpha = 0.97        #FACTOR
    emphasized_y = np.append(y[tmin*sr],y[tmin*sr+1:tmax*sr]-alpha*y[tmin*sr:tmax*sr-1])
    n = int((tmax-tmin)*sr) #信号一共的sample数量

    # #未经过预加重的信号频谱
    # plt.figure(dpi=300,figsize=(7,4))
    # freq = sr/n*np.linspace(0,n/2,int(n/2)+1)
    # plt.plot(freq,np.absolute(np.fft.rfft(y[tmin*sr:tmax*sr],n)**2)/n)
    # plt.xlim(0,5000)
    # plt.xlabel('Frequency/Hz',fontsize=14)
    # #预加重之后的信号频谱
    # plt.figure(dpi=300,figsize=(7,4))
    # plt.plot(freq,np.absolute(np.fft.rfft(emphasized_y,n)**2)/n)
    # plt.xlim(0,5000)
    # plt.xlabel('Frequency/Hz',fontsize=14)
    frame_size, frame_stride = 0.025,0.01
    frame_length, frame_step = int(round(sr*frame_size)),int(round(sr*frame_stride))
    signal_length = (tmax-tmin)*sr
    frame_num = int(np.ceil((signal_length-frame_length)/frame_step))+1 #向上舍入
    pad_frame = (frame_num-1)*frame_step+frame_length-signal_length #不足的部分补零
    pad_y = np.append(emphasized_y,np.zeros(pad_frame))
    signal_len = signal_length+pad_frame
    indices = np.tile(np.arange(0, frame_length), (frame_num, 1)) + np.tile(
        np.arange(0, frame_num * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_y[indices] #frame的每一行代表每一帧的sample值
    frames *= np.hamming(frame_length) #加hamming window 注意这里不是矩阵乘法
    NFFT = 1024 #frame_length=1102，所以用1024足够了
    mag_frames = np.absolute(np.fft.rfft(frames,NFFT))
    pow_frames = mag_frames**2/NFFT

    # plt.figure(dpi=300,figsize=(12,6))
    # plt.imshow(20*np.log10(pow_frames[40:].T),cmap=plt.cm.jet,aspect='auto')
    # plt.yticks([0,128,256,384,512],np.array([0,128,256,384,512])*sr/NFFT)
    #下面定义mel filter
    mel_N = 40 #滤波器数量,这个数字若要提高，则NFFT也要相应提高
    mel_low, mel_high = 0, (2595*np.log10(1+(sr/2)/700))
    mel_freq = np.linspace(mel_low,mel_high,mel_N+2)
    hz_freq = (700 * (10**(mel_freq / 2595) - 1))
    bins = np.floor((NFFT)*hz_freq/sr) #将频率转换成对应的sample位置
    fbank = np.zeros((mel_N,int(NFFT/2+1))) #每一行储存一个梅尔滤波器的数据
    for m in range(1, mel_N + 1):
        f_m_minus = int(bins[m - 1])   # left
        f_m = int(bins[m])             # center
        f_m_plus = int(bins[m + 1])    # right
        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
    filter_banks = np.matmul(pow_frames, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # np.finfo(float)是最小正值
    filter_banks = 20 * np.log10(filter_banks)  # dB
    filter_banks -= (np.mean(filter_banks, axis=0) + 1e-8)
    #filter_banks -= np.mean(filter_banks,axis=1).reshape(-1,1)
    plt.figure(dpi=16,figsize=(16,16))
    plt.imshow(filter_banks[40:].T, cmap=plt.cm.jet,aspect='auto')
    #plt.yticks([0,10,20,30,39],[0,1200,3800,9900,22000])
    SavedFileName = fileName.rsplit('\\',1)
    SavedFileName = SavedFileName[1]
    SavedFileName = SavedFileName.rsplit('.',1)
    SavedFileName = SavedFileName[0]
    plt.savefig(f"D:\EdgeDownload\Sampled\DevSet\-bonafide\{SavedFileName}")
    plt.close()

def get_files():
    NameList = []
    for filepath,dirnames,filenames in os.walk(r'D:\EdgeDownload\dev_set\dev_set\\-bonafide'):    #Path here
        for filename in filenames:
            temp = os.path.join(filepath,filename)
            NameList.append(f'{temp}')
    return NameList
# def getfiles():
#     NameList = []
#     filenames=os.listdir(r'E:\XJTLU\SURFData\Trial\OriHere')    #Path here
#     print(filenames)
#     return NameList

NameList = get_files()
for FilePaths in NameList:
    DrawMelSpectrogram(FilePaths)