import numpy as np
from lib import consts
import IR_Reverb

def run():

    print ("\n\n================IR=TEST=05================")

    # Test with dry_wet = 0 (fully dry)
    reverb_dry = IR_Reverb.IR(ir="1", dry_wet=0.0)

    # Test with dry_wet = 1 (fully wet)
    reverb_wet = IR_Reverb.IR(ir="1", dry_wet=1.0)

    # Test with dry_wet = 0.5 (50/50)
    reverb_mix = IR_Reverb.IR(ir="1", dry_wet=0.5)

    # Create test input
    test_input = np.random.randn(consts.BUFFER_SIZE) * 0.1

    # Process with all three
    output_dry = reverb_dry.use(test_input)
    output_wet = reverb_wet.use(test_input)
    output_mix = reverb_mix.use(test_input)

    print("Dry-Wet Mix Test")
    print(f"Dry output max: {np.max(np.abs(output_dry)):.4f}")
    print(f"Wet output max: {np.max(np.abs(output_wet)):.4f}")
    print(f"Mix output max: {np.max(np.abs(output_mix)):.4f}")

    # Dry should be roughly equal to input (no reverb)
    # Wet should be larger (reverb added)
    # Mix should be in between