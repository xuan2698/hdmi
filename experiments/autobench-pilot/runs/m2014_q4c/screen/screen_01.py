def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        d = rng.getrandbits(1)
        if i == 0:
            r = 1
        else:
            r = 1 if rng.randrange(8) == 0 else 0
        result.append({"d": d, "r": r})
    return result
