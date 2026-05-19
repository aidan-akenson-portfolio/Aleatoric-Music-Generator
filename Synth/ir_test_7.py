import numpy as np
from lib import consts
import IR_Reverb

def run():
    
    print ("\n\n================IR=TEST=07================")

    # Enable debug mode 3 for detailed timing
    consts.DEBUG_MODE = 3

    reverb = IR_Reverb.IR(ir="1")

    print("Processing single frame with DEBUG_MODE=3:")
    print("Look for the printed timing information")

    test_input = np.random.randn(consts.BUFFER_SIZE) * 0.1
    output = reverb.use(test_input)

    print(f"\nOutput max: {np.max(np.abs(output))}")
    print(f"Output contains NaN: {np.any(np.isnan(output))}")
    print(f"Output contains Inf: {np.any(np.isinf(output))}")