import os
import numpy as np

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def multipath_channel(signal, fs, delay_set, gain_set, doppler_shift_range=(10, 1000)):
    """
    다중 경로 채널을 시뮬레이션
    - signal: 입력 신호
    - fs: 샘플링 주파수
    - delay_set: 가능한 지연 값 배열 (초 단위)
    - gain_set: 가능한 경로 감쇠 값 배열 (dB)
    - doppler_shift_range: 도플러 주파수 범위 (Hz)
    """
    
    selected_delays = [0] + list(np.random.choice(delay_set, 5, replace=False))
    selected_gains = [0] + list(np.random.choice(gain_set, 5, replace=False))

    doppler_shift = np.random.randint(doppler_shift_range[0], doppler_shift_range[1])

    filtered_signal = np.zeros_like(signal)
    
    
    for delay, gain in zip(selected_delays, selected_gains):
        sample_delay = int(delay * fs)
        
        delayed_signal = np.zeros_like(signal)
        if sample_delay < len(signal):
            delayed_signal[sample_delay:] = signal[:len(signal) - sample_delay]
        
        # dB 단위의 이득을 선형 이득으로 변환
        linear_gain = 10 ** (gain / 20.0)
        
        filtered_signal += linear_gain * delayed_signal
    
    # 도플러 효과는 여기서는 생략했지만 필요 시 추가하면 됨

    return filtered_signal


def add_awgn(signal, snr_db):
    signal_power = np.mean(np.abs(signal) ** 2)
    snr_linear = 10 ** (snr_db / 10.0)
    noise_power = signal_power / snr_linear
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(signal)) + 1j * np.random.randn(len(signal)))
    return signal + noise, noise

fs = 100e6
def deployment(wav, snr, waveform, fps_idx):
    attenuationset = np.arange(-20, 2, 2)
    delayset = np.arange(1, 1001, 50) * 1e-9
    
    delays = np.random.choice(delayset, 5, replace=False)
    gains = np.random.choice(attenuationset, 5, replace=False)
    
    signal = multipath_channel(wav, fs, delays, gains)
    noisy_signal, noise = add_awgn(signal, snr)
    pnorm_signal = signal / (np.sqrt(np.sum(signal ** 2)) + 1e-6)
    pnorm_signal, _ = add_awgn(pnorm_signal, snr)
    
    dir = '/data/kiwan/LPI_KIWAN'
    waveform_folder = os.path.join(dir, waveform)
    np.save(os.path.join(waveform_folder, f'{waveform}_snr{snr}_Signal_{fps_idx}.npy'), wav)
    np.save(os.path.join(waveform_folder, f'{waveform}_snr{snr}_Noise_{fps_idx}.npy'), noise)
    np.save(os.path.join(waveform_folder, f'{waveform}_snr{snr}_Noisy_{fps_idx}.npy'), noisy_signal)
    np.save(os.path.join(waveform_folder, f'{waveform}_snr{snr}_pwnNoisy_{fps_idx}.npy'), pnorm_signal)