def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        # Vary 'a' to cover both values and transitions
        if i == 0:
            a = 1
        elif i < 4:
            a = 1
        elif i < 8:
            a = 0
        else:
            # Mix of patterns: runs, alternations, random
            mode = rng.randrange(4)
            if mode == 0:
                a = 1
            elif mode == 1:
                a = 0
            elif mode == 2:
                a = i % 2
            else:
                a = rng.getrandbits(1)
        result.append({'a': a})
    return result
