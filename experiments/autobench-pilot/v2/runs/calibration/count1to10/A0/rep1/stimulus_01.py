def stimulus(rng, cycles):
    result = []
    state = 1
    for i in range(cycles):
        # Decide reset with some probability, but ensure coverage
        if i == 0:
            reset = 1
        elif i == 1:
            reset = 0
        elif i == 2:
            reset = 1
        elif i == 3:
            reset = 0
        else:
            # Occasionally reset, otherwise let it count
            if rng.random() < 0.1:
                reset = 1
            else:
                reset = 0
        result.append({'reset': reset})
    return result
