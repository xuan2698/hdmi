def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        # Vary reset patterns: mostly low, with occasional high pulses
        r = rng.random()
        if r < 0.15:
            reset = 1
        else:
            reset = 0
        result.append({'reset': reset})
    return result
