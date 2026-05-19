import numpy as np
from lib import consts
import IR_Reverb

def run():
    
    print ("\n\n================IR=TEST=03================")

    reverb = IR_Reverb.IR(ir="1")

    # Create test input (mono)
    test_input_mono = np.random.randn(consts.BUFFER_SIZE) * 0.1

    # Process
    output = reverb.use(test_input_mono)

    print("Shape and Type Test")
    print(f"Input shape: {test_input_mono.shape}")
    print(f"Input dtype: {test_input_mono.dtype}")
    print(f"Output shape: {output.shape}")  # Should be (BUFFER_SIZE * 2,)
    print(f"Output dtype: {output.dtype}")  # Should be float64

    # Verify output size
    expected_output_size = consts.BUFFER_SIZE * 2  # Stereo interleaved
    print(f"Output size correct: {len(output) == expected_output_size}")