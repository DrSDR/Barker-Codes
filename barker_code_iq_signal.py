import numpy as np

def generate_barker_radar_signal(filename="barker13_radar.iq"):
    # --- Given Parameters ---
    sample_rate = 5e6          # 5 MHz
    chip_time = 10e-6          # 10 microseconds
    pri_time = 300e-6          # 300 microseconds Pulse Repetition Interval
    num_pri = 4096             # Total number of pulses
    freq_offset = 4000.0       # 4 kHz frequency offset
    
    # Amplitude parameter in dB (UPDATED to -1 dB)
    amplitude_db = -1.0        
    
    # --- Convert dB to Linear Voltage Amplitude ---
    # -1 dB translates to roughly 0.89125 peak linear scale
    amplitude_linear = 10 ** (amplitude_db / 20.0)
    
    # --- Derived Dimensions ---
    samples_per_chip = int(round(sample_rate * chip_time))  # 50 samples
    samples_per_pulse = 13 * samples_per_chip              # 650 samples
    samples_per_pri = int(round(sample_rate * pri_time))    # 1,500 samples
    
    if samples_per_pulse > samples_per_pri:
        raise ValueError("Pulse width exceeds the PRI duration! Check your parameters.")

    print(f"Signal Amplitude (dB): {amplitude_db} dB")
    print(f"Signal Amplitude (Linear): {amplitude_linear:.5f}")
    print(f"Samples per chip: {samples_per_chip}")
    print(f"Pulse duration: {samples_per_pulse} samples ({13 * chip_time * 1e6:.1f} µs)")
    print(f"Total samples per PRI: {samples_per_pri}")
    
    # 1. Define the 13:1 Barker code and apply the linear amplitude scaling
    barker_13 = np.array([1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1], dtype=np.float32)
    barker_13_scaled = barker_13 * amplitude_linear
    
    # 2. Oversample the Barker code chips
    pulse_signal = np.repeat(barker_13_scaled, samples_per_chip)
    
    # 3. Create a single PRI period (Pulse + Zero Padding/Listening Time)
    pri_signal = np.zeros(samples_per_pri, dtype=np.complex64)
    pri_signal[:samples_per_pulse] = pulse_signal  # Inject the Barker pulse at the start
    
    # 4. Replicate across all 4,096 PRIs
    total_signal = np.tile(pri_signal, num_pri)
    
    # 5. Apply the 4 kHz frequency offset continuously across time
    total_samples = len(total_signal)
    t = np.arange(total_samples, dtype=np.float64) / sample_rate
    
    # Complex exponential frequency shift
    phase_rotation = np.exp(1j * 2 * np.pi * freq_offset * t).astype(np.complex64)
    total_signal *= phase_rotation
    
    # 6. Interleave into float32 IQ array [I0, Q0, I1, Q1...]
    interleaved_iq = np.empty(2 * total_samples, dtype=np.float32)
    interleaved_iq[0::2] = np.real(total_signal)
    interleaved_iq[1::2] = np.imag(total_signal)
    
    # 7. Write to binary file
    interleaved_iq.tofile(filename)
    
    file_size_mb = interleaved_iq.nbytes / (1024 * 1024)
    print(f"\nSuccessfully generated: '{filename}'")
    print(f"Total Complex Samples: {total_samples:,}")
    print(f"Output File Size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    generate_barker_radar_signal()

