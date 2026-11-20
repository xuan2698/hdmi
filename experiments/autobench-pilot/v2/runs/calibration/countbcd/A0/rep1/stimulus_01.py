def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        # Mostly keep reset low; occasionally assert it
        if i == 0:
            reset = 1
        elif rng.random() < 0.05:
            reset = 1
        else:
            reset = 0
        result.append({'reset': reset})
    return result
