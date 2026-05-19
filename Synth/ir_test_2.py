import numpy as np
from lib import consts
import IR_Reverb

def run():

    print ("\n\n================IR=TEST=02================")

    reverb = IR_Reverb.IR(ir="1")  # Real IR

    # Send silence
    silent_input = np.zeros(consts.BUFFER_SIZE)

    # Process for multiple frames to build up reverb
    outputs = []
    for frame in range(100):
        output = reverb.use(silent_input)
        outputs.append(output)

    # After processing silence, output should also be silence
    # (except for the reverb tail decay)

    final_output = outputs[-1]
    print("Silence Test")
    print(f"Output max after 100 frames of silence: {np.max(np.abs(final_output))}")
    print(f"Output should be very close to zero: {np.max(np.abs(final_output)) < 0.01}")