
import numpy as np

def bpsk(cpp, fs, A, fc, phase_code):
    Ts = 1 / fs
    t = np.arange(0, cpp / fc, Ts)
    s = np.zeros(len(phase_code) * len(t), dtype=complex)
    
    for k, phase in enumerate(phase_code):
        s[k * len(t):(k + 1) * len(t)] = A * np.exp(1j * (2 * np.pi * fc * t + phase))
    
    return s

def type_barker(cpp, fs, A, fc, code):
    Ts = 1 / fs                 
    Tc = cpp / fc               
    t = np.arange(0, Tc, Ts)    

    modulated_signal = np.array([])
    for bit in code:
        phase = 0 if bit == 1 else np.pi
        symbol = A * np.exp(1j * (2 * np.pi * fc * t + phase))
        modulated_signal = np.concatenate((modulated_signal, symbol))
    
    return modulated_signal

def type_costas(N, fs, A, fc, Lc):
    t = np.linspace(0, N/fs, N)
    hop_indices = np.random.permutation(np.arange(Lc))
    hop_freqs = hop_indices * (fs / (2 * Lc))           
    signal = np.zeros(N)
    hop_length = N // Lc
    for i in range(Lc):
        start_idx = i * hop_length
        end_idx = (i + 1) * hop_length
        signal[start_idx:end_idx] = A * np.cos(2 * np.pi * (fc + hop_freqs[i]) * t[start_idx:end_idx])
    return signal


def type_frank(cpp, fs, A, fc, M):
    phaseCode = np.zeros((M, M))
    for ii in range(M):
        for jj in range(M):
            phaseCode[ii, jj] = 2 * np.pi / M * ii * jj
    phaseCode = phaseCode.flatten()
    
    s = bpsk(cpp, fs, A, fc, phaseCode)
    return s

def type_lfm(num_samples, fs, A, fc, Df, updown):
    pw = num_samples / fs
    t = np.arange(1, num_samples + 1) / fs
    phi0 = 2 * np.pi * np.random.rand() - np.pi

    if updown.lower() == "up":
        f = fc + Df / pw * t
    elif updown.lower() == "down":
        f = fc - Df / pw * t
    else:
        print('Default up direction!')
        f = fc + Df / pw * t

    s = A * np.exp(1j * (2 * np.pi * f * t + phi0))
    return s

def type_P1(cpp, fs, A, fc, M):
    phase_code = np.zeros((M, M))
    
    for ii in range(M):
        for jj in range(M):
            phase_code[ii, jj] = -np.pi / M * ((M - (2 * jj + 1)) * ((jj) * M + (ii)))
    
    phase_code = phase_code.flatten()
    s = bpsk(cpp, fs, A, fc, phase_code)
    return s

def type_P2(cpp, fs, A, fc, M):
    phase_code = np.zeros((M, M))
    
    for ii in range(M):
        for jj in range(M):
            phase_code[ii, jj] = -np.pi / (2 * M) * (2 * ii - 1 - M) * (2 * jj - 1 - M)
    
    phase_code = phase_code.flatten()
    s = bpsk(cpp, fs, A, fc, phase_code)
    return s

def type_P3(cpp, fs, A, fc, p):
    phase_code = np.zeros(p)
    
    for ii in range(p):
        phase_code[ii] = np.pi / p * (ii ** 2)
    
    s = bpsk(cpp, fs, A, fc, phase_code)
    return s

def type_P4(cpp, fs, A, fc, p):
    phase_code = np.zeros(p)
    
    for ii in range(p):
        phase_code[ii] = np.pi / p * (ii ** 2) - np.pi * (ii)
    
    s = bpsk(cpp, fs, A, fc, phase_code)
    return s

def type_T1(fs, A, fc, Nps, Ng):
    """
    - fs: 샘플링 주파수
    - A: 진폭
    - fc: 반송파 주파수
    - Nps: 패턴의 샘플 수
    - Ng: 패턴의 길이
    """
    Ts = 1 / fs
    Tc = 1 / fc
    t = np.arange(0, Tc, Ts)
    pw = Tc * Ng

    phase_code = np.zeros((Ng - 1, len(t)))
    for jj in range(Ng - 1):
        phase_code[jj, :] = np.mod(2 * np.pi / Nps * np.floor((Ng * t - jj * pw) * jj * Nps / pw), 2 * np.pi)

    phase_code = phase_code.T.flatten()
    s = bpsk(2, fs, A, fc, phase_code)
    return s

def type_T2(fs, A, fc, Nps, Ng):
    Ts = 1 / fs
    Tc = 1 / fc
    t = np.arange(0, Tc, Ts)
    pw = Tc * Ng
    
    phase_code = np.zeros((Ng - 1, len(t)))
    for jj in range(Ng - 1):
        phase_code[jj, :] = np.mod(2 * np.pi / Nps * np.floor((Ng * t - jj * pw) * (2 * jj - Ng + 1) / pw * Nps / 2), 2 * np.pi)

    phase_code = phase_code.T.flatten()
    s = bpsk(2, fs, A, fc, phase_code)
    return s

def type_T3(NumberSamples, fs, A, fc, Nps, B):
    Ts = 1 / fs
    pw = NumberSamples / fs
    t = np.arange(0, pw, Ts)

    phase_code = np.mod(2 * np.pi / Nps * np.floor(Nps * B * t ** 2 / (2 * pw)), 2 * np.pi)
    s = A * np.exp(1j * (2 * np.pi * fc * t + phase_code))
    return s

def type_T4(NumberSamples, fs, A, fc, Nps, B):
    Ts = 1 / fs
    pw = NumberSamples / fs
    t = np.arange(0, pw, Ts)

    phase_code = np.mod(2 * np.pi / Nps * np.floor(Nps * B * t ** 2 / (2 * pw) - Nps * B * t / 2), 2 * np.pi)
    s = A * np.exp(1j * (2 * np.pi * fc * t + phase_code))
    return s