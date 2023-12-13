# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 12:58:54 2023

@author: rabia
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, filtfilt, butter


df = pd.read_csv(r"C:\\Users\\Admin\Desktop\\yedinci dönem\\biyomedikal sinyal analizi\\mimic_perform_af_016_data.csv")


ppg_signal = df["PPG"].to_numpy()
time = df["Time"].to_numpy()

fs = 125
window_size = fs *5
start_index = 0
end_index = start_index + window_size

while end_index < len(ppg_signal):
    
    window_ppg = ppg_signal[start_index:end_index]
    
    window_time = time[start_index:end_index]
    
    pwe, _ = find_peaks(-window_ppg, distance=60)
    
    pwsp, _ = find_peaks(window_ppg, distance=fs/2)
    
    peaks , _= find_peaks(window_ppg)
    
    pwdp=[]
    s_points = []
    for r in pwsp:
        right_segment = window_ppg[r:] 
        
        PWDP, _ = find_peaks(right_segment, width=5) 
        if PWDP.size > 0:
            if PWDP[0] < r + 1:
                pwdp.append(PWDP[0] + r)
            else:
                continue
            
        s, _ = find_peaks(-right_segment, distance=3
                          ) 
        if s.size > 0:
            s_points.append(s[0] + r)
            
    #times  
    pwd = np.diff(window_time[pwe])
    min_length = min(len(pwe), len(peaks))

    systolic_phase = np.diff(window_time[pwe[:min_length]]- window_time[peaks[:min_length]])
    diastolic_phase = np.diff(-(window_time[pwe]-window_time[pwe[:min_length]] - window_time[peaks[:min_length]]))
    
    min_length = min(len(pwdp), len(pwsp))
    ppt = abs(np.diff(window_time[pwsp[:min_length]] - window_time[pwdp[:min_length]]))
    
    #amplitudes
    pwa_values = window_ppg[pwe]
    dicrotic_notch_values = window_ppg[pwdp] if len(pwdp) > 0 else None
    pwsp_values = window_ppg[pwsp]
    pwdp_values = window_ppg[pwdp] if len(pwdp) > 0 else None
    
    #Features heart rate
    heart_rate = 60 / np.mean(pwd)
    
    print(f"PWD: {pwd}")
    print(f"Systolic Phase Duration: {systolic_phase}")
    print(f"Diastolic Phase Duration: {diastolic_phase}")
    print(f"PPT : {ppt}")
    
    print(f"Pulse Wave Amplitude (PWA): {pwa_values}")
    print(f"Dicrotic Notch Amplitudes: {dicrotic_notch_values}")
    print(f"Pulse Wave Systolic Peak (PWSP) Amplitudes: {pwsp_values}")
    print(f"Pulse Wave Diastolic Peak (PWDP) Amplitudes: {pwdp_values}")
    print(f"Heart Rate: {heart_rate} bpm")


    plt.figure(figsize=(10, 4))
    plt.plot(window_time, window_ppg, label='PPG Signal')
    plt.plot(window_time[pwe], window_ppg[pwe], 'ro', label='(PWB)')
    plt.plot(window_time[pwsp], window_ppg[pwsp], 'bo', label='(PWSP)')
    plt.plot(window_time[pwdp], window_ppg[pwdp], 'o', color="black", label='(PWDP)')
    plt.plot(window_time[s_points], window_ppg[s_points], 'o', color="purple", label='(Disrotic)')

    plt.title('PPG Signal Analysis')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    input("Press Enter to slide the window...")
    start_index += window_size
    end_index += window_size
