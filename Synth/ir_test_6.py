import numpy as np
from scipy.signal import fftconvolve
from lib import consts
import IR_Reverb
import soundfile as sf

def run():

    print ("\n\n================IR=TEST=06================")

    # Load the IR file
    ir_file = "ir_demo_1_filtered_white_noise_massive.wav"
    ir_audio, ir_sr = sf.read(ir_file, always_2d=True)

    # Resample if needed
    if ir_sr != consts.BITRATE:
        from scipy.signal import resample_poly
        ir_left = resample_poly(ir_audio[:, 0], up=consts.BITRATE, down=ir_sr)
        ir_right = resample_poly(ir_audio[:, 1], up=consts.BITRATE, down=ir_sr)
        ir_audio = np.column_stack([ir_left, ir_right])

    # Create test signal (several frames of white noise)
    num_frames = 20
    test_signal = np.random.randn(num_frames * consts.BUFFER_SIZE) * 0.1

    # Process with your reverb
    reverb = IR_Reverb.IR(ir="1", dry_wet=1.0)  # Fully wet for comparison
    your_output = []
    for frame in range(num_frames):
        frame_input = test_signal[frame * consts.BUFFER_SIZE : (frame + 1) * consts.BUFFER_SIZE]
        output = reverb.use(frame_input)
        # Extract left channel (every other sample due to interleave)
        your_output.append(output[::2])

    your_output_mono = np.concatenate(your_output)

    # Reference: scipy's fftconvolve (use left channel of IR)
    reference_output = fftconvolve(test_signal, ir_audio[:, 0], mode='same')

    # Compare
    correlation = np.corrcoef(your_output_mono[:len(reference_output)], reference_output)[0, 1]

    print("Reference Comparison Test")
    print(f"Correlation with scipy.signal.fftconvolve: {correlation:.6f}")
    print(f"Test PASSED if correlation > 0.95" if correlation > 0.95 else f"Test FAILED")
    print(f"High correlation (>0.99) means nearly identical: {correlation > 0.99}")

    # If correlation is low, there's likely a bug in:
    # 1. Padding alignment
    # 2. History management
    # 3. Output extraction indices