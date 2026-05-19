import numpy as np
from lib import consts
import IR_Reverb

def run():

    print ("\n\n================IR=TEST=01================")

    # Create reverb with impulse IR (test mode)
    reverb = IR_Reverb.IR(dry_wet=1.0, ir="0")

    # Create impulse input (all zeros except first sample)
    test_input = np.zeros(consts.BUFFER_SIZE)
    test_input[0] = 1.0

    # Process the impulse
    output = reverb.use(test_input)

    # The output should be the impulse response itself
    # (convolution of impulse with IR gives the IR back)

    print("Impulse Response Test")
    print(f"Input max: {np.max(np.abs(test_input))}")
    print(f"Output max: {np.max(np.abs(output))}")
    print(f"Output shape: {output.shape}")
    print(f"First 10 samples: {output[:10]}")
    print(f"Last 10 samples: {output[-10:]}")

if __name__ == "__main__":
    run()