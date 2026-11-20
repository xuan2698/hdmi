def stimulus(rng, cycles):
    result = []
    # Start with reset asserted to trigger the 4-cycle shift_ena behavior
    reset = 1
    for i in range(cycles):
        result.append({'reset': reset})
        # Randomly toggle reset, but bias toward deasserted to exercise the counter
        if reset == 1:
            # After asserting reset, likely deassert to let counter run
            reset = 1 if rng.random() < 0.2 else 0
        else:
            # Occasionally re-assert reset to test synchronous reset behavior
            reset = 1 if rng.random() < 0.15 else 0
    return result
