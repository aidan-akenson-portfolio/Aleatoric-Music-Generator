import numpy as np
from lib import consts
import IR_Reverb

def run():
    
    print ("\n\n================IR=TEST=04================")

    reverb = IR_Reverb.IR(ir="1")

    # Create a sine wave input
    freq = 1000  # Hz
    duration_frames = 10
    samples_total = duration_frames * consts.BUFFER_SIZE

    t = np.arange(samples_total) / consts.BITRATE
    test_signal = np.sin(2 * np.pi * freq * t) * 0.1

    # Process frame by frame
    outputs = []
    for frame in range(duration_frames):
        frame_input = test_signal[frame * consts.BUFFER_SIZE : (frame + 1) * consts.BUFFER_SIZE]
        output = reverb.use(frame_input)
        outputs.append(output)

    all_output = np.concatenate(outputs)

    print("Frequency Response Test")
    print(f"Input signal RMS: {np.sqrt(np.mean(test_signal**2)):.4f}")
    print(f"Output signal RMS: {np.sqrt(np.mean(all_output**2)):.4f}")
    print(f"Output max: {np.max(np.abs(all_output)):.4f}")
    print(f"Output is not zero: {np.max(np.abs(all_output)) > 0.01}")

    # The output should have more energy than the input due to reverb